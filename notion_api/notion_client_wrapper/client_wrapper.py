import logging
import os

from notion_client import Client
from notion_client.errors import APIResponseError

from notion_client_wrapper.base_operator import BaseOperator
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block import Block, BlockFactory
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.created_time import CreatedTime
from notion_client_wrapper.properties.icon import Icon
from notion_client_wrapper.properties.last_edited_time import LastEditedTime
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.property_translator import PropertyTranslator

logger = logging.getLogger(__name__)

class UpdatePageError(Exception):
    pass

class ClientWrapper:
    def __init__(self, client: Client) -> None:
        self.client = client

    @staticmethod
    def get_instance() -> "ClientWrapper":
        client = Client(auth=os.getenv("NOTION_SECRET"))
        return ClientWrapper(client)


    def retrieve_page(self, page_id: str, page_model: BasePage|None = None) -> BasePage:
        """ 指定されたページを取得する """
        page_entity = self.__retrieve_page(page_id=page_id)
        return self.__convert_page_model(page_entity=page_entity, include_children=True, page_model=page_model)

    def update_page(self, page_id: str, properties: list[Property]|None = None) -> dict:
        """ 指定されたページを更新する """
        update_properties = Properties(values=properties or []).exclude_button()
        try:
            return self.client.pages.update(
                page_id=page_id,
                properties=update_properties.__dict__(),
            )
        except APIResponseError as e:
            exception_message = f"page_id: {page_id}, error: {e}, properties: {update_properties.__dict__()}"
            raise UpdatePageError(exception_message) from e

    def retrieve_comments(self, page_id: str) -> list[dict]:
        """ 指定されたページのコメントを取得する """
        comments = self.client.comments.list(
            block_id=page_id,
        )
        return comments["results"]

    def create_page_in_database(
            self,
            database_id: str,
            cover: Cover | None = None,
            properties: list[Property]|None = None,
            blocks: list[Block]|None = None) -> dict:
        """ データベース上にページを新規作成する """
        properties = properties or []
        result = self.client.pages.create(
            parent={
                "type": "database_id",
                "database_id": database_id,
            },
            cover=cover.__dict__() if cover is not None else None,
            properties=Properties(values=properties).__dict__() if len(
                properties) > 0 else None,
        )
        if blocks is not None:
            self.append_blocks(block_id=result["id"], blocks=blocks)
        return result

    def retrieve_database(  # noqa: PLR0913
            self,
            database_id: str,
            title: str | None = None,
            filter_param: dict|None = None,
            page_model: BasePage|None = None,
            include_children: bool|None=None) -> list[BasePage]:
        """ 指定されたデータベースのページを取得する """
        results = self._database_query(database_id=database_id, filter_param=filter_param)
        pages: list[BasePage] = []
        for page_entity in results:
            page = self.__convert_page_model(
                page_entity=page_entity,
                include_children=include_children,
                page_model=page_model)
            pages.append(page)
        if title is not None:
            pages = list(filter(lambda p: p.properties.get_title().text == title, pages))
        return pages

    def _database_query(self, database_id: str, filter_param: dict|None=None, start_cursor: str | None = None) -> dict:
        if filter_param is None:
            return self._database_query_without_filter(database_id=database_id, start_cursor=start_cursor)
        results = []
        while True:
            data:dict = self.client.databases.query(
                database_id=database_id,
                start_cursor=start_cursor,
                filter=filter_param,
            )
            results += data.get("results")
            if not data.get("has_more"):
                return results
            start_cursor = data.get("next_cursor")

    def _database_query_without_filter(self, database_id: str, start_cursor: str | None = None ) -> dict:
        results = []
        while True:
            data:dict = self.client.databases.query(
                database_id=database_id,
                start_cursor=start_cursor,
            )
            results += data.get("results")
            if not data.get("has_more"):
                return results
            start_cursor = data.get("next_cursor")

    def find_page(self, database_id: str, title: str) -> BasePage | None:
        """ 指定されたデータベースのページを取得する。1ページのみ取得する。複数ある場合は最初に見つかったページを返す """
        data = self.client.databases.query(database_id=database_id)
        for page_entity in data["results"]:
            page = self.__convert_page_model(page_entity=page_entity, include_children=False)
            if page.properties.get_title().text == title:
                return page
        return None

    def list_blocks(self, block_id: str) -> list[Block]:
        """ 指定されたブロックの子ブロックを取得する """
        return self.__get_block_children(page_id=block_id)

    def append_block(self, block_id: str, block: Block) -> dict:
        """ 指定されたブロックに子ブロックを追加する """
        return self.append_blocks(block_id=block_id, blocks=[block])

    def append_blocks(self, block_id: str, blocks: list[Block]) -> dict:
        """ 指定されたブロックに子ブロックを追加する """
        return self.__append_block_children(
            block_id=block_id,
            children=[b.to_dict(for_create=True) for b in blocks],
        )

    def append_comment(self, page_id: str, text: str):
        """ 指定されたページにコメントを追加する """
        return self.client.comments.create(
            parent={ "page_id": page_id },
            rich_text=[{"text": {"content": text}}],
        )

    def remove_page(self, page_id: str) -> None:
        """ 指定されたページを削除する """
        self.client.pages.update(
            page_id=page_id,
            archived=True,
        )

    def __append_block_children(self, block_id: str, children=list[dict]) -> dict:
        return self.client.blocks.children.append(
            block_id=block_id, children=children)

    def __convert_page_model(
            self,
            page_entity: dict,
            include_children: bool = True,
            page_model: BasePage|None = None) -> BasePage:
        id = page_entity["id"]
        url = page_entity["url"]
        created_time = CreatedTime.create(page_entity["created_time"])
        last_edited_time = LastEditedTime.create(page_entity["last_edited_time"])
        created_by = BaseOperator.of(page_entity["created_by"])
        last_edited_by = BaseOperator.of(page_entity["last_edited_by"])
        cover = Cover.of(page_entity["cover"]) if page_entity["cover"] is not None else None
        icon = Icon.of(page_entity["icon"]) if page_entity["icon"] is not None else None
        archived = page_entity["archived"]
        properties=PropertyTranslator.from_dict(page_entity["properties"])
        block_children = self.__get_block_children(page_id=id) if include_children else []

        page_model_cls = page_model or BasePage
        return page_model_cls(
            id=id,
            url=url,
            created_time=created_time,
            last_edited_time=last_edited_time,
            created_by=created_by,
            last_edited_by=last_edited_by,
            cover=cover,
            icon=icon,
            archived=archived,
            properties=properties,
            block_children=block_children)

    def __retrieve_page(self, page_id: str) -> dict:
        return self.client.pages.retrieve(page_id=page_id)

    def __get_block_children(self, page_id: str) -> list[Block]:
        block_entities = self.__list_blocks(block_id=page_id)[
            "results"]
        return list(map(lambda b: BlockFactory.create(b), block_entities))

    def __list_blocks(self, block_id: str) -> dict:
        return self.client.blocks.children.list(block_id=block_id)

if __name__ == "__main__":
    # python -m notion_client_wrapper.client_wrapper
    client = ClientWrapper(client=Client(auth=os.getenv("NOTION_SECRET")))

    # page = client.retrieve_page(page_id="b7576fbdde9b476f913924c1bd90b250")
    # print(page)
    # pages = client.retrieve_database(database_id="986876c2e7f8457abd4437334835d0db", title="テストA")
    # print(pages)
    # blocks = client.list_blocks(block_id="b7576fbdde9b476f913924c1bd90b250")
    # print(blocks)
    # result = client.append_blocks(block_id="b7576fbdde9b476f913924c1bd90b250", blocks=[Paragraph.from_plain_text("test")])
    # print(result)
    print(client.retrieve_page(page_id="56049c410c1748b9b035584cf576744f"))
