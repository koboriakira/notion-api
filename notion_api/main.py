from mangum import Mangum
from fastapi import FastAPI, Header
from datetime import date as DateObject
from datetime import datetime as DateTimeObject
from datetime import time as TimeObject
from datetime import timedelta
from typing import Optional
import requests
import os
import json
import yaml
from custom_logger import get_logger
from notion_executer import NotionClient

logger = get_logger(__name__)
logger.info("start")
logger.debug("debug: ON")

NOTION_SECRET = os.environ.get("NOTION_SECRET")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

def valid_saccess_token(secret: str) -> None:
    if ENVIRONMENT == "dev":
        return
    # NOTION_SECRETを使って、アクセストークンを検証する
    if secret != NOTION_SECRET:
        raise Exception("invalid secret: " + secret)


app = FastAPI(
    title="Example Test API",
    description="Describe API documentation to be served; types come from "
    "pydantic, routes from the decorators, and docs from the fastapi internal",
    version="0.0.1",
)

@app.get("/projects/")
async def get_projects(status: Optional[str] = None, remind_date: Optional[DateObject] = None, is_thisweek: Optional[bool] = None):
    """ NotionのZettlekastenに新しいページを追加する """
    notion_client = NotionClient()
    notion_client.test()

    return {
        'status': 'ok',
    }

    # status_list = _get_status_list(status)
    # get_detail_flag = True if status is not None else False
    # projects = notion_client.retrieve_projects(status_list=status_list,
    #                                            get_detail=get_detail_flag,
    #                                            remind_date=remind_date,
    #                                            filter_thisweek=is_thisweek)
    # return convert_to_project_model(projects)

@app.get("/hello")
def hello():
    """
    Return a greeting
    """
    logger.info("hello")
    return {
        'status': 'ok',
    }


handler = Mangum(app, lifespan="off")
