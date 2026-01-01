from pydantic import BaseModel


class InterruptTodoRequest(BaseModel):
    title: str

class InsertSubTodoRequest(BaseModel):
    title: str
