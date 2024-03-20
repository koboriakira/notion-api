
from fastapi import APIRouter, Header

from infrastructure.task.task_repository_impl import TaskRepositoryImpl
from router.request import CreateNewTaskRequest
from router.response import BaseResponse, Task, TaskResponse
from usecase.create_new_task_usecase import CreateNewTaskUsecase
from usecase.find_task_usecase import FindTaskUsecase
from util.access_token import valid_access_token
from util.error_reporter import ErrorReporter

router = APIRouter()


@router.get("/{task_id}", response_model=TaskResponse)
def find_task(
        task_id: str,
        access_token: str | None = Header(None)) -> TaskResponse:
    """ タスクを取得 """
    valid_access_token(access_token)
    usecase = FindTaskUsecase(task_repository=TaskRepositoryImpl())
    task = usecase.execute(task_id=task_id)
    return TaskResponse(data=Task.from_params(task))

@router.post("", response_model=BaseResponse)
def create_task(
        request: CreateNewTaskRequest,
        access_token: str | None = Header(None)) -> BaseResponse:
    try:
        valid_access_token(access_token)
        usecase = CreateNewTaskUsecase(
            task_repository=TaskRepositoryImpl(),
        )
        result = usecase.execute(
            title=request.title,
            mentioned_page_id=request.mentioned_page_id,
            start_date=request.start_date,
            status=request.status,
            task_kind=request.task_kind)
        return BaseResponse(data=result)
    except:
        ErrorReporter.report_error()
        raise
