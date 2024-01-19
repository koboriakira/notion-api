from typing import Optional
from datetime import date as DateObject


async def get_projects(status: Optional[str] = None, remind_date: Optional[DateObject] = None, is_thisweek: bool = False):
    """ プロジェクト一覧を取得 """
    return [{
        "dummy": "dummy"
    }]
