import logging
from interface import batch
from util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event, context):
    batch.move_completed_task_to_backup()

if __name__ == "__main__":
    handler({}, {})
