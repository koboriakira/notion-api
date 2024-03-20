from dataclasses import dataclass, field
from datetime import datetime

from notion_client_wrapper.base_operator import BaseOperator
from notion_client_wrapper.block import Block
from notion_client_wrapper.properties.checkbox import Checkbox
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.created_time import CreatedTime
from notion_client_wrapper.properties.date import Date
from notion_client_wrapper.properties.icon import Icon
from notion_client_wrapper.properties.last_edited_time import LastEditedTime
from notion_client_wrapper.properties.multi_select import MultiSelect
from notion_client_wrapper.properties.number import Number
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.relation import Relation
from notion_client_wrapper.properties.select import Select
from notion_client_wrapper.properties.status import Status
from notion_client_wrapper.properties.text import Text
from notion_client_wrapper.properties.title import Title
from notion_client_wrapper.properties.url import Url


@dataclass(frozen=True)
class BasePage:
    id: str|None
    url: str|None
    created_time: CreatedTime|None
    last_edited_time: LastEditedTime|None
    created_by: BaseOperator|None
    last_edited_by: BaseOperator|None
    properties: Properties
    cover: Cover | None = None
    icon: Icon | None = None
    archived: bool|None = False
    parent: dict | None = None
    block_children: list[Block]|None = field(default_factory=list)
    object = "page"

    def get_title(self) -> Title:
        return self.properties.get_title()

    def get_title_text(self) -> str:
        return self.get_title().text

    def get_created_at(self) -> datetime:
        return self.created_time.value

    def get_updated_at(self) -> datetime:
        return self.last_edited_time.value

    def get_status(self, name: str) -> Status:
        return self.properties.get_property(name=name, instance_class=Status)

    def get_text(self, name: str) -> Text:
        return self.properties.get_property(name=name, instance_class=Text)

    def get_date(self, name: str) -> Date:
        return self.properties.get_property(name=name, instance_class=Date)

    def get_select(self, name: str) -> Select:
        return self.properties.get_property(name=name, instance_class=Select)

    def get_multi_select(self, name: str) -> MultiSelect:
        return self.properties.get_property(name=name, instance_class=MultiSelect)

    def get_relation(self, name: str) -> Relation:
        return self.properties.get_property(name=name, instance_class=Relation)

    def get_checkbox(self, name: str) -> Checkbox:
        return self.properties.get_property(name=name, instance_class=Checkbox)

    def get_url(self, name: str) -> Url:
        return self.properties.get_property(name=name, instance_class=Url)

    def get_number(self, name: str) -> Number:
        return self.properties.get_property(name=name, instance_class=Number)
