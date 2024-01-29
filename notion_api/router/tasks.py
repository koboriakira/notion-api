from fastapi import APIRouter, Header
from typing import Optional
from datetime import date as Date
from interface import task
from util.access_token import valid_access_token
from router.response import TasksResponse, Task

router = APIRouter()


@router.get("", response_model=TasksResponse)
def get_tasks(start_date: Optional[Date] = None,
              status: Optional[str] = None,
              access_token: Optional[str] = Header(None)):
    valid_access_token(access_token)
    status_list: list[str] = status.split(",") if status else []
    tasks = task.fetch_tasks(start_date=start_date,
                             status_list=status_list)
    return TasksResponse(data=[Task.from_params(t) for t in tasks])