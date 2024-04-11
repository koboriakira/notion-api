import os

import requests


class UnsplashPhoto:
    BASE_URL = "https://api.unsplash.com/photos"

    def __init__(self) -> None:
        unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY")
        if unsplash_access_key is None:
            msg = "UNSPLASH_ACCESS_KEYが設定されていません"
            raise ValueError(msg)
        self._unsplash_access_key = unsplash_access_key

    def get_random_photo_url(self, query_words: list[str]) -> str:
        """
        Get a random photo URL based on the given query words.

        Args:
            query_words (list[str]): The list of query words to search for.

        Returns:
            str: The URL of the random photo.

        Raises:
            requests.HTTPError: If the request to the Unsplash API fails.
        """
        url = self.__get_random_api_url(query_words)
        data = self.__get(url)
        return data["urls"]["full"]

    def __get(self, url: str) -> dict:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()

    def __get_random_api_url(self, query_words: list[str]) -> str | None:
        query = ",".join(query_words)
        return f"{self.BASE_URL}/random/?client_id={self._unsplash_access_key}&query={query}"
