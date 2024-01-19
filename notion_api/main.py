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

logger = get_logger(__name__)
logger.info("start")
logger.debug("debug: ON")

NOTION_SECRET = os.environ.get("NOTION_SECRET")

def valid_saccess_token(secret: str) -> None:
    # NOTION_SECRETを使って、アクセストークンを検証する
    if secret != NOTION_SECRET:
        raise Exception("invalid secret: " + secret)


app = FastAPI(
    title="Example Test API",
    description="Describe API documentation to be served; types come from "
    "pydantic, routes from the decorators, and docs from the fastapi internal",
    version="0.0.1",
)

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
