from mangum import Mangum
from fastapi import FastAPI
import logging
from router import projects, healthcheck
from util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

# アプリ設定
app = FastAPI(
    title="My Notion API",
    version="0.0.1",
)
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(healthcheck.router, prefix="/healthcheck", tags=["healthcheck"])


handler = Mangum(app, lifespan="off")
