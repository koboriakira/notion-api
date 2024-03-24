from datetime import date

from fastapi import APIRouter, Header

from interface import task
from router.response import Task, TasksResponse
from util.access_token import valid_access_token

router = APIRouter()


@router.get("", response_model=TasksResponse)
def get_tasks(start_date: date | None = None,
              status: str | None = None,
              access_token: str | None = Header(None)) -> TasksResponse:
    valid_access_token(access_token)
    status_list: list[str] = status.split(",") if status else []
    tasks = task.fetch_tasks(start_date=start_date,
                             status_list=status_list)
    return TasksResponse(data=[Task(t) for t in tasks])

@router.get("/current", response_model=TasksResponse)
def get_current_tasks(access_token: str | None = Header(None)) -> TasksResponse:
    valid_access_token(access_token)
    tasks = task.get_current_tasks()
    return TasksResponse(data=[Task.from_model(t) for t in tasks])
