import logging
from util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event, context):
    pass
