from mangum import Mangum
from fastapi import FastAPI, Header
from starlette.middleware.cors import CORSMiddleware
from datetime import date as DateObject
from datetime import datetime as DateTimeObject
from datetime import time as TimeObject
from datetime import timedelta
from typing import Optional
import os
from custom_logger import get_logger
from interface import project

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
    title="My Notion API",
    version="0.0.1",
)


@app.get("/projects")
def get_projects(status: Optional[str] = None,
                 remind_date: Optional[DateObject] = None,
                 is_thisweek: Optional[bool] = None,
                 access_token: Optional[str] = Header(None)):
    valid_saccess_token(access_token)
    return project.get_projects(status, remind_date, is_thisweek)


@app.get("/healthcheck")
def hello():
    """
    Return a greeting
    """
    logger.debug("healthcheck")
    logger.info("healthcheck")
    return {
        'status': 'ok',
    }


handler = Mangum(app, lifespan="off")
