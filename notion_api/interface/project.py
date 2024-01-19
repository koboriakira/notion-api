from typing import Optional
from datetime import date as DateObject
from usecase.project_list_usecase import ProjectListUseCase


async def get_projects(status: Optional[str] = None, remind_date: Optional[DateObject] = None, is_thisweek: bool = False):
    """ プロジェクト一覧を取得 """
    usecase = ProjectListUseCase()
    usecase.execute()
    return [{
        "dummy": "dummy"
    }]
