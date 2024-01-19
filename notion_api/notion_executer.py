from datetime import datetime, timedelta
from datetime import date as DateObject
from typing import Optional
from notion_client_wrapper.client_wrapper import ClientWrapper
import os

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

class NotionClient:
    def __init__(self):
        pass
        self.client = ClientWrapper(notion_secret=os.getenv("NOTION_SECRET"))

    def test(self):
        print("test")
        print(self.client.retrieve_page(page_id="6c3a861e6a6c405ba2472866a9fedfce"))
