import os
from util.environment import Environment

NOTION_SECRET = os.environ.get("NOTION_SECRET")

def valid_access_token(secret: str) -> None:
    # NOTION_SECRETを使って、アクセストークンを検証する
    if secret != NOTION_SECRET and not Environment.is_dev():
        raise Exception("invalid secret: " + secret)
