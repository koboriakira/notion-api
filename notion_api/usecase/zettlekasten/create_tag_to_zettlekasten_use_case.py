from logging import Logger

from common.domain.tag_relation import TagRelation
from common.service.tag_creator.tag_creator import TagCreator
from notion_client_wrapper.client_wrapper import ClientWrapper
from util.tag_analyzer import TagAnalyzer
from zettlekasten.domain.zettlekasten import Zettlekasten
from zettlekasten.infrastructure.zettlekasten_repository_impl import (
    ZettlekastenRepositoryImpl as ZettlekastenRepository,
)


class CreateTagToZettlekastenUseCase:
    def __init__(
        self,
        zettlekasten_repository: ZettlekastenRepository,
        tag_analyzer: TagAnalyzer,
        tag_creator: TagCreator,
        logger: Logger,
    ) -> None:
        self._zettlekasten_repository = zettlekasten_repository
        self._tag_analyzer = tag_analyzer
        self._tag_creator = tag_creator
        self._logger = logger

    def execute(self) -> None:
        zettlekastens = self._zettlekasten_repository.search(is_tag_empty=True, include_children=True)

        for zettlekasten in zettlekastens:
            self._update_tag(zettlekasten)

    def _update_tag(self, zettlekasten: Zettlekasten) -> None:
        title = zettlekasten.get_title_text()
        self._logger.info(f"次のZettlekastenのタグを更新します: {title}")
        page_text = zettlekasten.get_slack_text_in_block_children()
        if page_text is None or page_text == "":
            # 本文をまだ書いてない場合はスキップ
            return
        text = f"【タイトル】\n{title}\n\n【本文】\n{page_text}"
        tags = self._tag_analyzer.handle(text=text)
        tag_page_id_list = self._tag_creator.execute(tag=tags)
        tag_relation = TagRelation.from_page_id_list(tag_page_id_list)
        zettlekasten.update_tag_relation(tag_relation)
        self._zettlekasten_repository.save(zettlekasten)


if __name__ == "__main__":
    # python -m notion_api.usecase.zettlekasten.create_tag_to_zettlekasten_use_case
    import logging

    logging.basicConfig(level=logging.INFO)
    client = ClientWrapper.get_instance()
    zettlekasten_repository = ZettlekastenRepository(
        client=client,
        logger=logging.getLogger(__name__),
    )
    tag_analyzer = TagAnalyzer(
        logger=logging.getLogger(__name__),
    )
    tag_creator = TagCreator()
    use_case = CreateTagToZettlekastenUseCase(
        zettlekasten_repository=zettlekasten_repository,
        tag_analyzer=tag_analyzer,
        tag_creator=tag_creator,
    )

    # zettlekasten = use_case._zettlekasten_repository.find_by_title("30分で学習する方法")
    # use_case._update_tag(zettlekasten)
    use_case.execute()
