from typing import Optional
from datetime import date as Date
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title, Text, Relation, Url, Date, Cover
from usecase.service.tag_create_service import TagCreateService
from custom_logger import get_logger

logger = get_logger(__name__)

class AddBookUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()
        self.tag_create_service = TagCreateService()

    def execute(self,
                title: str,
                authors: list[str],
                publisher: Optional[str] = None,
                published_date: Optional[Date] = None,
                image_url: Optional[str] = None,
                url: Optional[str] = None,
                ) -> dict:
        logger.info("execute")
        logger.info(f"title: {title}")
        logger.info(f"authors: {authors}")
        logger.info(f"publisher: {publisher}")
        logger.info(f"published_date: {published_date}")
        logger.info(f"image_url: {image_url}")
        logger.info(f"url: {url}")

        # データベースの取得
        searched_books = self.client.retrieve_database(
            database_id=DatabaseType.BOOK.value,
            title=title,
        )
        if len(searched_books) > 0:
            logger.info("The book is already registered")
            book = searched_books[0]
            return {
                "id": book.id,
                "url": book.url
            }
        logger.info("Create a book page")

        # 著者のタグページを作成
        tag_page_ids:list[str] = []
        for author in authors:
            page_id = self.tag_create_service.add_tag(name=author)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        properties=[Title.from_plain_text(name="Title", text=title)]
        if len(tag_page_ids) > 0:
            properties.append(Relation.from_id_list(name="著者", id_list=tag_page_ids))
        if publisher is not None:
            properties.append(Text.from_plain_text(name="出版社", text=publisher))
        if published_date is not None:
            properties.append(Date.from_start_date(name="出版日", start_date=published_date))
        if url is not None:
            properties.append(Url.from_url(name="URL", url=url))

        result = self.client.create_page_in_database(
            database_id=DatabaseType.BOOK.value,
            properties=properties
        )
        page_id = result["id"]
        page_url = result["url"]

        return {
            "id": page_id,
            "url": page_url
        }
