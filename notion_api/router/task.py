from fastapi import APIRouter, Header
from typing import Optional
from interface import task
from util.access_token import valid_access_token
from router.response import TaskResponse, Task

router = APIRouter()


@router.get("/{task_id}", response_model=TaskResponse)
def find_task(task_id: str,
              access_token: Optional[str] = Header(None)):
    valid_access_token(access_token)
    task_result = task.find_task(id=task_id)
    return TaskResponse(data=Task.from_params(task_result))
