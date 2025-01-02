import json
from datetime import date

import requests

from book.book_api import BookApi, BookApiResult

URL = "https://api.openbd.jp/v1/get?isbn="


class BookOpenbdApi(BookApi):
    def find_by_title(self, title: str) -> BookApiResult:
        raise NotImplementedError

    def find_by_id(self, book_id: str) -> BookApiResult:
        raise NotImplementedError

    def find_by_isbn(self, isbn: str) -> BookApiResult:
        response = requests.get(URL + isbn, timeout=10)
        response_json = response.json()
        onix: dict = response_json[0].get("onix")

        descriptive_detail: dict = onix["DescriptiveDetail"]
        title_detail: dict = descriptive_detail["TitleDetail"]
        title_text: str = title_detail["TitleElement"]["TitleText"]
        contributers: list[dict] = descriptive_detail["Contributor"]
        print(json.dumps(descriptive_detail, indent=2, ensure_ascii=False))

        publishing_detail: dict = onix["PublishingDetail"]
        publishing_date: str = publishing_detail["PublishingDate"][0]["Date"]
        if len(publishing_date) == 8:
            publishing_date = publishing_date[:4] + "-" + publishing_date[4:6] + "-" + publishing_date[6:]
        elif len(publishing_date) == 6:
            publishing_date = publishing_date[:4] + "-" + publishing_date[4:] + "-01"
        return BookApiResult(
            title=title_detail["TitleElement"]["TitleText"]["content"],
            # authors=[contributer["PersonName"]["content"] for contributer in contributers],
            published_date=date.fromisoformat(publishing_date),
        )


if __name__ == "__main__":
    # python -m notion_api.book.book_openbd_api
    api = BookOpenbdApi()
    result = api.find_by_isbn("404896836X")
    print(result)
