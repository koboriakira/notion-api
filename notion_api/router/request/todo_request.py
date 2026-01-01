from pydantic import BaseModel


class InterruptTodoRequest(BaseModel):
    title: str
