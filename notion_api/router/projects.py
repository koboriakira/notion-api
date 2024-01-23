from fastapi import APIRouter, Header
from typing import Optional
from datetime import date as Date
from interface import project
from util.access_token import valid_access_token
from router.response.projects_response import ProjectsResponse, Project

router = APIRouter()


@router.get("", response_model=ProjectsResponse)
def get_projects(status: Optional[str] = None,
                 remind_date: Optional[Date] = None,
                 is_thisweek: Optional[bool] = None,
                 access_token: Optional[str] = Header(None)):
    valid_access_token(access_token)
    projects = project.get_projects(status, remind_date, is_thisweek)
    return ProjectsResponse(data=[Project.from_params(p) for p in projects])

@router.get("/{project_id}")
def find_project(project_id: str,
                 access_token: Optional[str] = Header(None)):
    valid_access_token(access_token)
    return project.find_project(project_id)
