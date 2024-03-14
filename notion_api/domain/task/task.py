from datetime import datetime

from notion_client_wrapper.base_page import BasePage
from util.datetime import JST

COLUMN_NAME_STATUS = "ステータス"
COLUMN_NAME_START_DATE = "実施日"
COLUMN_NAME_KIND = "タスク種別"

class Task(BasePage):
    @property
    def status(self) -> str:
        return self.get_status(name=COLUMN_NAME_STATUS).status_name

    @property
    def start_datetime(self) -> datetime|None:
        start_date_model = self.get_date(name=COLUMN_NAME_START_DATE)
        if start_date_model is None or start_date_model.start is None:
            return None
        return _convert_to_datetime(start_date_model.start)

    @property
    def kind(self) -> str|None:
        kind_model = self.get_select(name=COLUMN_NAME_KIND)
        if kind_model is None or kind_model.name is None:
            return None
        return kind_model.name

    def is_kind_trash(self) -> bool:
        return self.kind == "ゴミ箱"

    def has_start_datetime(self) -> bool:
        return self.start_datetime is not None

def _convert_to_datetime(value: str) -> datetime:
    from datetime import date
    if len(value) == 10:
        tmp_date = date.fromisoformat(value)
        return datetime(tmp_date.year, tmp_date.month, tmp_date.day, tzinfo=JST)
    return datetime.fromisoformat(value)
