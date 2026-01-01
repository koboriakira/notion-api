from fastapi import APIRouter, Header
from lotion import Lotion
from notion_databases.todo import Todo, TodoKind, TodoKindEnum, TodoName, TodoParentTask, TodoStatus
from router.request.todo_request import InsertSubTodoRequest, InsertTodoRequest, InterruptTodoRequest
from router.response.todo_response import TodoPageModel, TodoResponse, TodosResponse
from util.access_token import valid_access_token

router = APIRouter()

@router.post("/{page_id}/complete/", response_model=TodosResponse)
def complete(
    page_id: str,
    access_token: str | None = Header(None),
) -> TodoResponse:
    valid_access_token(access_token)
    client = Lotion.get_instance()

    todo = client.retrieve_page(page_id=page_id, cls=Todo).complete()
    client.update(todo)
    return TodoResponse(data=TodoPageModel.from_entity(todo))



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

    if ip_todos:
        for ip_todo in ip_todos:
            # 完了扱いにして更新
            client.update(ip_todo.complete())

            # コピーして未実施状態にしたものを新規保存
            client.create_page(ip_todo.copy().todo())


    # あたらしい差し込みタスクを追加
    new_todo = client.create_page(
        Todo.create(properties=[TodoName.from_plain_text(request.title)])
        .inprogress()
    )

    return TodoResponse(data=TodoPageModel.from_entity(new_todo))



@router.post("/sub/", response_model=TodoResponse)
def create_subtodo(
    request: InsertTodoRequest,
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

    if not ip_todos:
        raise ValueError("進行中のタスクが存在しません。")

    parent_todo = None
    for ip_todo in ip_todos:
        if not ip_todo.is_sub_task():
            parent_todo = ip_todo
            break

    if not parent_todo:
        raise ValueError("進行中の親タスクが存在しません。")

    # あたらしいサブタスクを追加
    new_todo = client.create_page(
        Todo.create(properties=[
            TodoName.from_plain_text(request.title),
            TodoKind.from_enum(TodoKindEnum.SUBTASK),
            TodoParentTask.from_id(parent_todo.id)
        ])
        .inprogress()
    )

    return TodoResponse(data=TodoPageModel.from_entity(new_todo))


@router.post("/", response_model=TodoResponse)
def create(
    request: InsertTodoRequest,
    access_token: str | None = Header(None),
) -> TodoResponse:
    valid_access_token(access_token)
    client = Lotion.get_instance()

    # あたらしい差し込みタスクを追加
    new_todo = client.create_page(
        Todo.create(properties=[
            TodoName.from_plain_text(request.title),
            TodoKind.from_enum(TodoKindEnum.INTERRUPTION)
        ])
        .inprogress()
    )

    return TodoResponse(data=TodoPageModel.from_entity(new_todo))
