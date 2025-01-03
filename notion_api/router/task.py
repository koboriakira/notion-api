from fastapi import APIRouter, Header
from lotion import Lotion

from router.request.task_request import CreateNewTaskRequest, UpdateTaskRequest
from router.response import BaseResponse, TaskResponse
from router.response import Task as TaskDto
from task.task_repository_impl import TaskRepositoryImpl
from usecase.create_new_task_usecase import CreateNewTaskUsecase
from usecase.find_task_usecase import FindTaskUsecase
from usecase.task.complete_task_usecase import CompleteTaskUsecase
from usecase.task.find_latest_inprogress_task_usecase import FindLatestInprogressTaskUsecase
from usecase.task.start_task_usecase import StartTaskUsecase
from usecase.update_task_use_case import UpdateTaskUsecase
from util.access_token import valid_access_token
from util.error_reporter import ErrorReporter

router = APIRouter()

client = Lotion.get_instance()
task_repository = TaskRepositoryImpl(notion_client_wrapper=client)


@router.get("/{task_id}")
def find_task(task_id: str, access_token: str | None = Header(None)) -> TaskResponse:
    """タスクを取得"""
    valid_access_token(access_token)
    usecase = FindTaskUsecase(task_repository=task_repository)
    task = usecase.execute(task_id=task_id)
    return TaskResponse(data=TaskDto.from_model(task))


@router.get("/inprogress/")
def get_inprogress(access_token: str | None = Header(None)) -> TaskResponse:
    """タスクを取得"""
    valid_access_token(access_token)
    usecase = FindLatestInprogressTaskUsecase(task_repository=task_repository)
    task = usecase.execute()
    return TaskResponse(data=TaskDto.from_model(task) if task is not None else None)


@router.post("/{task_id}")
def upadate_task(task_id: str, request: UpdateTaskRequest, access_token: str | None = Header(None)) -> TaskResponse:
    """タスクを取得"""
    valid_access_token(access_token)
    usecase = UpdateTaskUsecase(task_repository=task_repository)
    task = usecase.execute(task_id=task_id, status=request.status)
    return TaskResponse(data=TaskDto.from_model(task))


@router.post("/{task_id}/complete/")
def complete_task(task_id: str, access_token: str | None = Header(None)) -> TaskResponse:
    try:
        valid_access_token(access_token)
        usecase = CompleteTaskUsecase(
            task_repository=task_repository,
        )
        task = usecase.execute(page_id=task_id)
        return TaskResponse(data=TaskDto.from_model(task))
    except:
        ErrorReporter().execute()
        raise


@router.post("/{task_id}/start/")
def start_task(task_id: str, access_token: str | None = Header(None)) -> TaskResponse:
    try:
        valid_access_token(access_token)
        usecase = StartTaskUsecase(
            task_repository=task_repository,
        )
        task = usecase.execute(page_id=task_id)
        return TaskResponse(data=TaskDto.from_model(task))
    except:
        ErrorReporter().execute()
        raise


@router.post("/")
def create_task(request: CreateNewTaskRequest, access_token: str | None = Header(None)) -> BaseResponse:
    try:
        valid_access_token(access_token)
        usecase = CreateNewTaskUsecase(
            task_repository=task_repository,
        )
        result = usecase.execute(
            title=request.title,
            mentioned_page_id=request.mentioned_page_id,
            start_date=request.start_date,
            end_date=request.end_date,
            status=request.status,
            task_kind=request.task_kind,
        )
        return BaseResponse(data=result)
    except:
        ErrorReporter().execute()
        raise
