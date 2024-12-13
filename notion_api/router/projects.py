from datetime import date

from fastapi import APIRouter, Header

from interface import project
from lotion import Lotion
from notion_client_wrapper.page.page_id import PageId
from project.infrastructure.project_repository_impl import ProjectRepositoryImpl
from router.request.notion_automation_request import NotionAutomationRequest
from router.response.base_response import BaseResponse
from router.response.projects_response import Project, ProjectResponse, ProjectsResponse
from task.infrastructure.task_repository_impl import TaskRepositoryImpl
from usecase.project.create_project_from_template_usecase import CreateProjectFromTemplateUsecase
from usecase.project.remove_project_service import RemoveProjectService
from util.access_token import valid_access_token

router = APIRouter()

client = Lotion.get_instance()


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


@router.post("/from_automation/")
def create_new_project(
    request: NotionAutomationRequest,
    access_token: str | None = Header(None),
) -> BaseResponse:
    valid_access_token(access_token)
    project_template_id = PageId(value=request.data.id)
    usecase = CreateProjectFromTemplateUsecase(
        client=client,
        project_repository=ProjectRepositoryImpl(client=client),
        task_repository=TaskRepositoryImpl(notion_client_wrapper=client),
    )
    project = usecase.execute(project_template_id=project_template_id)
    if project.page_id is None:
        raise Exception("Project page_id is None")
    return BaseResponse(data={"id": project.page_id.value, "url": project.url})


@router.delete("/{project_id}/")
def remove_project(
    project_id: str,
    access_token: str | None = Header(None),
) -> BaseResponse:
    valid_access_token(access_token)
    remove_project_service = RemoveProjectService(
        task_repository=TaskRepositoryImpl(notion_client_wrapper=client),
        project_repository=ProjectRepositoryImpl(client=client),
    )
    remove_project_service.execute(id_=PageId(value=project_id))
    return BaseResponse()
