from unittest import TestCase

import requests


class OpenbdCoverSearcher:
    def __init__(self):
        url = "https://api.openbd.jp/v1/coverage"
        response = requests.get(url, timeout=10)
        data = response.json()
        self.isbn_list = data

    def get_cover_image_url(self, isbn: str):
        if not self.has_data(isbn):
            return None

        # openBD APIのエンドポイントURL
        url = f"https://api.openbd.jp/v1/get?isbn={isbn}"

        try:
            # APIにリクエストを送信
            response = requests.get(url, timeout=10)
            data = response.json()
            if not data:
                return None
            return self.get_resource_link(data[0]) or self.cover_image_url(data[0])

        except requests.exceptions.RequestException as e:
            # リクエストエラーが発生した場合、エラーメッセージを表示してNoneを返す
            print(f"Error: {e}")
            return None

    def get_resource_link(self, data: dict) -> str | None:
        try:
            return data["onix"]["CollateralDetail"]["SupportingResource"]["ResourceVersion"]["ResourceLink"]
        except KeyError:
            print("KeyError: ResourceLink not found.")
            return None

    def cover_image_url(self, data: dict) -> str | None:
        try:
            return data["summary"]["cover"]
        except KeyError:
            print("KeyError: cover not found.")
            return None

    def has_data(self, isbn: list) -> bool:
        return isbn in self.isbn_list


class TestOpenbdCoverSearcher(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test(self):
        isbn = "9784775942154"  # 書籍のISBNを指定
        cover_image_url = OpenbdCoverSearcher().get_cover_image_url(isbn)

        if cover_image_url:
            print(f"表紙画像URL: {cover_image_url}")
        else:
            print("表紙画像が見つかりませんでした。")

        self.fail("not implemented")
