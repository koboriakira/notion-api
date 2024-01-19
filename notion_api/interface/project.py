from typing import Optional
from datetime import date as DateObject
from usecase.project_list_usecase import ProjectListUseCase
from model.project.project_status import ProjectStatus
from custom_logger import get_logger

logger = get_logger(__name__)

async def get_projects(status: Optional[str] = None, remind_date: Optional[DateObject] = None, is_thisweek: bool = False):
    """ プロジェクト一覧を取得 """
    status_list = ProjectStatus.get_status_list(status)
    logger.debug(status_list)
    detail_enabled = True if status is not None else False
    logger.debug(detail_enabled)
    usecase = ProjectListUseCase()
    result = usecase.execute(status_list=status_list,
                    remind_date=remind_date,
                    detail_enabled=detail_enabled,
                    thisweek_filter_enabled=is_thisweek)
    return result
