import logging
from pydoc import cli

from lotion import Lotion


from notion_api.notion_databases.task import Task, TaskKind
from notion_api.util.environment import Environment
from notion_databases.todo import Todo, TodoStatus

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)



if __name__ == "__main__":
    # python -m sample
    client = Lotion.get_instance()
    ip_todos = client.search_pages(
        cls=Todo,
        props=[
            TodoStatus.inprogress(),
        ],
    )
    print(ip_todos)
