from datetime import datetime

from pydantic import Field

from custom_logger import get_logger
from notion_databases.todo import Todo
from router.response.base_notion_page_model import BaseNotionPageModel
from router.response.base_response import BaseResponse


logger = get_logger(__name__)




class TodoPageModel(BaseNotionPageModel):
    status: str
    section: str
    kind: str
    log_start_datetime: datetime | None
    log_end_datetime: datetime | None

    @staticmethod
    def from_entity(entity: Todo) -> "TodoPageModel":
        return TodoPageModel(
            id=entity.id,
            url=entity.url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            title=entity.get_title_text(),
            status=entity.status.status_name,
            section=entity.section.selected_name,
            kind=entity.kind.selected_name,
            log_start_datetime=entity.log_date.start_datetime,
            log_end_datetime=entity.log_date.end_datetime,
        )

class TodoResponse(BaseResponse):
    data: TodoPageModel | None = Field(default=None)


class TodosResponse(BaseResponse):
    data: list[TodoPageModel] = Field(default=[])
