from dataclasses import dataclass, field
from datetime import datetime

from notion_client_wrapper.base_operator import BaseOperator
from notion_client_wrapper.block import Block
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties.checkbox import Checkbox
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.created_time import CreatedTime
from notion_client_wrapper.properties.date import Date
from notion_client_wrapper.properties.icon import Icon
from notion_client_wrapper.properties.last_edited_time import LastEditedTime
from notion_client_wrapper.properties.multi_select import MultiSelect
from notion_client_wrapper.properties.number import Number
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.properties.relation import Relation
from notion_client_wrapper.properties.select import Select
from notion_client_wrapper.properties.status import Status
from notion_client_wrapper.properties.text import Text
from notion_client_wrapper.properties.title import Title
from notion_client_wrapper.properties.url import Url
from util.datetime import jst_now


@dataclass
class BasePage:
    properties: Properties
    block_children: list[Block] = field(default_factory=list)
    id_: PageId | str | None = None
    url: str | None = None
    created_time: CreatedTime | None = None
    last_edited_time: LastEditedTime | None = None
    created_by: BaseOperator | None = None
    last_edited_by: BaseOperator | None = None
    cover: Cover | None = None
    icon: Icon | None = None
    archived: bool | None = False
    parent: dict | None = None
    object = "page"

    @staticmethod
    def create(properties: list[Property] | None = None, blocks: list[Block] | None = None) -> "BasePage":
        return BasePage(
            id_=None,
            url=None,
            created_time=None,
            last_edited_time=None,
            created_by=None,
            last_edited_by=None,
            properties=Properties(values=properties or []),
            cover=None,
            icon=None,
            archived=False,
            parent=None,
            block_children=blocks or [],
        )

    def get_slack_text_in_block_children(self) -> str:
        # FIXME: block_childrenをBlocks型にしたうえで、メソッドをBlocksに移動する
        if not self.block_children or len(self.block_children) == 0:
            return ""
        return "\n".join([block.to_slack_text() for block in self.block_children])

    def get_title(self) -> Title:
        return self.properties.get_title()

    def get_title_text(self) -> str:
        return self.get_title().text

    @property
    def title(self) -> str:
        return self.get_title_text()

    def get_created_at(self) -> datetime:
        if self.created_time is None:
            return jst_now()
        return self.created_time.start_time

    def get_updated_at(self) -> datetime:
        if self.last_edited_time is None:
            return jst_now()
        return self.last_edited_time.start_time

    def get_status(self, name: str) -> Status:
        return self.properties.get_property(name=name, instance_class=Status)

    def get_text(self, name: str) -> Text:
        return self.properties.get_property(name=name, instance_class=Text)

    def get_date(self, name: str | None = None) -> Date:
        _name = name or Date.DEFAULT_NAME
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

    def get_number(self, name: str) -> Number | None:
        return self.properties.get_property(name=name, instance_class=Number)

    def get_parant_database_id(self) -> str | None:
        """未実装。削除すべきかも"""
        if self.parent is None or "database_id" not in self.parent:
            return None
        return self.parent["database_id"]

    def update_id_and_url(self, page_id: str, url: str) -> None:
        self.id_ = page_id
        self.url = url

    def title_for_slack(self) -> str:
        """Slackでの表示用のリンクつきタイトルを返す"""
        return f"<{self.url}|{self.get_title_text()}>"

    def title_for_markdown(self) -> str:
        """Markdownでの表示用のリンクつきタイトルを返す"""
        return f"[{self.get_title_text()}]({self.url})"

    @property
    def id(self) -> str | None:
        if isinstance(self.id_, str):
            return self.id_
        return self.id_.value if self.id_ is not None else None

    @property
    def page_id(self) -> PageId | None:
        if isinstance(self.id_, str):
            return PageId(self.id_)
        return self.id_

    def get_id_and_url(self) -> dict[str, str]:
        if self.id is None or self.url is None:
            raise ValueError("id or url is None")
        return {
            "id": self.id,
            "url": self.url,
        }
