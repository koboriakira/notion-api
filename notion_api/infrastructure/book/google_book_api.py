from logging import Logger, getLogger

import requests

from book.book_api import BookApi, BookApiResult, BookApiResultConverter, NotFoundApiError


class GoogleBookApi(BookApi):
    def __init__(self, logger: Logger | None = None) -> None:
        self._logger = logger or getLogger(__name__)

    def find_by_id(self, book_id: str) -> BookApiResult:
        data = self.__get(path=f"volumes/{book_id}")
        if "volumeInfo" not in data:
            raise NotFoundApiError(param=book_id)
        volume_info: dict = data["volumeInfo"]
        return BookApiResultConverter.of(volume_info)

    def find_by_title(self, title: str) -> BookApiResult:
        params = {"q": title}
        data = self.__get(path="volumes", params=params)
        if "items" not in data or len(data["items"]) == 0:
            raise NotFoundApiError(param=title)
        item_id = data["items"][0]["id"]
        return self.find_by_id(book_id=item_id)

    def find_by_isbn(self, isbn: str) -> BookApiResult:
        # title検索と同じでいけるっぽい
        return self.find_by_title(title=isbn)

    def __get(self, path: str, params: dict | None = None) -> dict:
        url = "https://www.googleapis.com/books/v1/" + path
        response = requests.get(url, params, timeout=10)
        response.raise_for_status()
        return response.json()
