from typing import Optional
from datetime import date as DateObject
import requests
import json
from usecase.add_book_usecase import AddBookUsecase
from custom_logger import get_logger

logger = get_logger(__name__)

def add_book_by_google_book_id(id: Optional[str] = None, title: Optional[str] = None):
    logger.debug(f"google_book_id: {id}")
    logger.debug(f"title: {title}")
    usecase = AddBookUsecase()
    if id is None:
        id = _get_google_book_id(title)
    params = _get_google_book_info(id)
    return usecase.execute(**params)


def _get_google_book_id(title: str) -> str:
    URL = "https://www.googleapis.com/books/v1/volumes"
    response = requests.get(URL, params={"q": title})
    data:dict = response.json()
    items: list[dict] = data["items"]
    logger.debug(items[0])
    return items[0]["id"]

def _get_google_book_info(id: str):
    URL = "https://www.googleapis.com/books/v1/volumes/"
    response = requests.get(f"{URL}{id}")
    data:dict = response.json()
    info: dict = data["volumeInfo"]
    logger.debug(json.dumps(info, ensure_ascii=False))
    published_date = None
    try:
        published_date = DateObject.fromisoformat(info["publishedDate"])
    except:
        logger.error(f"cannot parse publishedDate: {info.get('publishedDate')}")

    return {
        "title": info["title"],
        "authors": info["authors"],
        "publisher": info.get("publisher"),
        "published_date": published_date,
        "image_url": info["imageLinks"].get("medium"),
        "url": info["infoLink"],
    }

if __name__ == "__main__":
    # python -m interface.book
    # add_book_by_google_book_id(id="1wSDDwAAQBAJ")
    add_book_by_google_book_id(title="大切なことだけをやりなさい")
