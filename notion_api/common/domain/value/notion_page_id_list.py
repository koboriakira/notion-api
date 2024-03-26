from dataclasses import dataclass

from common.domain.value.notion_page_id import NotionPageId


@dataclass(frozen=True)
class NotionPageIdList:
    values: list[NotionPageId]

    @staticmethod
    def from_str_list(id_list: list[str]) -> "NotionPageIdList":
        return NotionPageIdList(values=[NotionPageId(value=id_) for id_ in id_list])

    def to_str_list(self) -> list[str]:
        return [value.value for value in self.values]
