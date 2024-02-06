import logging
from interface import batch
from util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event, context):
    batch.update_current_tasks()

if __name__ == "__main__":
    handler({}, {})
