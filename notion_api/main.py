from mangum import Mangum
from fastapi import FastAPI
import logging
from router import projects, healthcheck, recipes, music, webclip, video, prowrestling, tasks
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
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
app.include_router(healthcheck.router, prefix="/healthcheck", tags=["healthcheck"])
app.include_router(music.router, prefix="/music", tags=["music"])
app.include_router(webclip.router, prefix="/webclip", tags=["webclip"])
app.include_router(video.router, prefix="/video", tags=["video"])
app.include_router(prowrestling.router, prefix="/prowrestling", tags=["prowrestling"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


handler = Mangum(app, lifespan="off")
