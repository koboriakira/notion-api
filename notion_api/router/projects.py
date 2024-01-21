from fastapi import APIRouter, Header
from typing import Optional
from datetime import date as Date
from interface import project

router = APIRouter()


@router.get("")
def get_projects(status: Optional[str] = None,
                 remind_date: Optional[Date] = None,
                 is_thisweek: Optional[bool] = None,
                 access_token: Optional[str] = Header(None)):
    # valid_saccess_token(access_token)
    return project.get_projects(status, remind_date, is_thisweek)
