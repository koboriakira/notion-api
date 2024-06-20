from logging import Logger, getLogger

from common.service.page_creator import PageCreator
from music.domain.song import Song
from music.infrastructure.music_repository_impl import MusicRepositoryImpl as MusicRepository


class MusicCreator(PageCreator):
    def __init__(
        self,
        music_repository: MusicRepository,
        logger: Logger | None = None,
    ) -> None:
        self._music_repository = music_repository
        self._logger = logger or getLogger(__name__)

    def execute(
        self,
        url: str,
        title: str | None = None,
        cover: str | None = None,
        params: dict | None = None,
    ) -> Song:
        if title is None:
            msg = "title is required"
            raise ValueError(msg)

        info_message = f"{self.__class__} execute: url={url}, title={title}, cover={cover}"
        self._logger.info(info_message)

        Music = self._Music_repository.find_by_title(title=title)
        if Music is not None:
            info_message = f"Music is already registered: {Music.Music_name}"
            self._logger.info(info_message)
            return Music

        info_message = "Create a Music"
        self._logger.info(info_message)

        # Musicを生成
        Music = Music.create(
            title=title,
            url=url,
            cover=cover,
        )

        return self._Music_repository.save(Music)


if __name__ == "__main__":
    # python -m notion_api.Music.service.Music_creator
    from notion_client_wrapper.client_wrapper import ClientWrapper

    client = ClientWrapper.get_instance()
    suite = MusicCreator(
        Music_repository=MusicRepository(client=client),
    )
    suite.execute(
        url="https://tabelog.com/tokyo/A1316/A131604/13020181/",
        title="焼肉・光陽 (大崎/焼肉)",
    )
