import json
import os
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

import requests

from util.openai_executer import OpenaiExecuter


@dataclass
class Gmail:
    _id: str
    subject: str
    from_mailaddress: str
    recieved_at: datetime
    body: str

    @staticmethod
    def from_dict(params: dict) -> "Gmail":
        subject = params["subject"]
        from_mailaddress: str = params["from"]
        from_mailaddress = from_mailaddress.split(" ")[1].replace("<", "").replace(">", "")
        datetime_: str = params["date"]
        recieved_at = datetime.fromisoformat(datetime_.replace("/", "-").replace(" ", "T").replace("0900", "09:00"))
        body = params["body"]
        return Gmail(
            _id=uuid4().urn,
            subject=subject,
            from_mailaddress=from_mailaddress,
            recieved_at=recieved_at,
            body=body,
        )

    @property
    def id(self) -> str:
        return self._id


class GmailService:
    def __init__(self) -> None:
        self._url = os.environ["GAS_GMAIL_URL"] + "?secret=" + os.environ["GAS_GMAIL_SECRET"]
        self._openai_executor = OpenaiExecuter()

    def fetch(self) -> list[Gmail]:
        response = requests.get(url=self._url, timeout=30)
        response.raise_for_status()
        response_json: list[dict] = response.json()
        return [Gmail.from_dict(params) for params in response_json]

    def fetch_by_ai(self) -> str:
        gmail_list = self.fetch()
        json_dict = [{"id": m.id, "subject": m.subject} for m in gmail_list]
        json_str = json.dumps(json_dict, ensure_ascii=False)
        system_prompt = """下記のメールについて、件名をもとに「返信が必要」「必ず読むべき」「どれでもない」の3つのラベルのどれかをつけて出力してください。
## 出力形式
id: こちらが与えたユニークID
label: 上述の3つのどれかを選択

## 入力形式
id: メールのユニークID
subject: メールの件名
"""
        response = self._openai_executor.simple_json_chat(system_prompt=system_prompt, user_content=json_str)
        print(response)
        return ""


if __name__ == "__main__":
    # python -m notion_api.common.service.gmail.gmail_service

    suite = GmailService()
    print(suite.fetch_by_ai())
