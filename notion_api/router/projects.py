from datetime import date

from fastapi import APIRouter, Header

from interface import project
from router.response.projects_response import Project, ProjectResponse, ProjectsResponse
from util.access_token import valid_access_token

router = APIRouter()


@router.get("")
def get_projects(
    status: str | None = None,
    remind_date: date | None = None,
    is_thisweek: bool | None = None,
    access_token: str | None = Header(None),
) -> ProjectsResponse:
    valid_access_token(access_token)
    projects = project.get_projects(status, remind_date, is_thisweek)
    return ProjectsResponse(data=[Project.from_params(p) for p in projects])


@router.get("/{project_id}")
def find_project(project_id: str, access_token: str | None = Header(None)) -> ProjectResponse:
    valid_access_token(access_token)
    project_result = project.find_project(project_id)
    return ProjectResponse(data=Project.from_params(project_result))
