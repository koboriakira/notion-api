import logging


from lotion import Lotion


from notion_api.util.environment import Environment
from notion_databases.todo import Todo

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)



if __name__ == "__main__":
    # python -m sample
    client = Lotion.get_instance()
    ip_todos = client.retrieve_pages(cls=Todo)
    for ip_todo in ip_todos:
        if (ip_todo.is_sub_task()):
            logging.info(f"Sub Task: {ip_todo.get_title_text()}")
