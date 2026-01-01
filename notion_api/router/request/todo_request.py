from pydantic import BaseModel


class InterruptTodoRequest(BaseModel):
    title: str

class InsertTodoRequest(BaseModel):
    title: str
