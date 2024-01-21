from fastapi import APIRouter, Header
from typing import Optional
from datetime import date as Date
from interface import project
from util.access_token import valid_access_token

router = APIRouter()


@router.get("")
def get_projects(status: Optional[str] = None,
                 remind_date: Optional[Date] = None,
                 is_thisweek: Optional[bool] = None,
                 access_token: Optional[str] = Header(None)):
    valid_access_token(access_token)
    return project.get_projects(status, remind_date, is_thisweek)

@router.get("/{project_id}")
def find_project(project_id: str,
                 access_token: Optional[str] = Header(None)):
    valid_access_token(access_token)
    return project.find_project(project_id)
