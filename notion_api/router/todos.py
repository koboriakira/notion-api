from fastapi import APIRouter, Header
from lotion import Lotion
from notion_databases.todo import Todo, TodoName, TodoStatus
from router.request.todo_request import InterruptTodoRequest
from router.response.todo_response import TodoPageModel, TodoResponse, TodosResponse
from util.access_token import valid_access_token

router = APIRouter()



@router.post("/interrupt/", response_model=TodosResponse)
def interrupt(
    request: InterruptTodoRequest,
    access_token: str | None = Header(None),
) -> TodoResponse:
    valid_access_token(access_token)
    client = Lotion.get_instance()

    # InProgressのタスクを取得する
    ip_todos = client.search_pages(
        cls=Todo,
        props=[
            TodoStatus.inprogress(),
        ],
    )
    print(ip_todos)
    # if ip_todos:
    #     ip_todo = ip_todos[0]

    #     # 完了扱いにして更新
    #     client.update(ip_todo.complete())

    #     # コピーして未実施状態にしたものを新規保存
    #     client.create_page(ip_todo.copy().todo())


    # あたらしい差し込みタスクを追加
    new_todo = client.create_page(
        Todo.create(properties=[TodoName.from_plain_text(request.title)])
        .inprogress()
    )

    return TodoResponse(data=TodoPageModel.from_entity(new_todo))
