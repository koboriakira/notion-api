from datetime import date

from custom_logger import get_logger

logger = get_logger(__name__)


def get_projects(status: str | None = None, remind_date: date | None = None, is_thisweek: bool = False):
    raise NotImplementedError


def find_project(project_id: str):
    """プロジェクト一覧を取得"""
    raise NotImplementedError
