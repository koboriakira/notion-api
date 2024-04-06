from pydantic import Field

from custom_logger import get_logger
from router.response.base_notion_page_model import BaseNotionPageModel
from router.response.base_response import BaseResponse

logger = get_logger(__name__)


class Project(BaseNotionPageModel):
    goal_id_list: list[str] = Field(default=[])
    status: str | None
    completed_at: str | None
    recursive_conf: str | None
    remind_date: str | None
    is_thisweek: bool

    @staticmethod
    def from_params(params: dict) -> "Project":
        logger.debug("params:")
        logger.debug(params)
        return Project(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
            goal_id_list=params["goal_id_list"],
            status=params["status"],
            completed_at=params["completed_at"],
            recursive_conf=params["recursive_conf"],
            remind_date=params["remind_date"],
            is_thisweek=params["is_thisweek"],
        )


class ProjectResponse(BaseResponse):
    data: Project | None


class ProjectsResponse(BaseResponse):
    data: list[Project] = Field(default=[])
