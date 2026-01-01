import logging
from pydoc import cli

from lotion import Lotion


from notion_api.notion_databases.task import Task, TaskKind
from notion_api.util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)



if __name__ == "__main__":
    # python -m sample
    client = Lotion.get_instance()
    tasks = client.search_pages(cls=Task, props=TaskKind.from_name("スケジュール"))
    for task in tasks:
        client.remove_page(task.id)
        logging.info(f"Removed task: {task.get_title_text()}")
