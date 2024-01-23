from pydantic import Field
import json
from typing import Optional
from router.response.base_response import BaseResponse
from router.response.base_notion_page_model import BaseNotionPageModel
from domain.project.project_status import ProjectStatus
from custom_logger import get_logger

logger = get_logger(__name__)

class Project(BaseNotionPageModel):
    goal_id_list: list[str] = Field(default=[])
    status: Optional[ProjectStatus]
    completed_at: Optional[str]
    recursive_conf: Optional[str]
    remind_date: Optional[str]
    is_thisweek: bool

    @staticmethod
    def from_params(params: dict) -> "Project":
        logger.debug(f"params:")
        logger.debug(params)
        return Project(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
            goal_id_list=params["goal_id_list"],
            status=ProjectStatus(params["status"]),
            completed_at=params["completed_at"],
            recursive_conf=params["recursive_conf"],
            remind_date=params["remind_date"],
            is_thisweek=params["is_thisweek"],
        )


class ProjectsResponse(BaseResponse):
    data: list[Project] = Field(default=[])
