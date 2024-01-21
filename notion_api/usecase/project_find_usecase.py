import os
from typing import Optional
from datetime import date as DateObject
from notion_client_wrapper.client_wrapper import ClientWrapper, BasePage
from domain.database_type import DatabaseType
from domain.project.project_status import ProjectStatus

class ProjectFindUsecase:
    def __init__(self):
        self.client = ClientWrapper(notion_secret=os.getenv("NOTION_SECRET"))

    def execute(self,
                project_id: str,
                ):
        project_page = self.client.retrieve_page(page_id=project_id)
        project = self._convert_project(project_page)
        # TODO: タスク取得も実装する
        # project["tasks"] = self._find_tasks(project_id=project["id"])
        return project


    def _convert_project(self, project: BasePage) -> dict:
        goal_relation = project.get_relation(name="目標")
        is_thisweek = project.get_checkbox(name="今週やる")
        status = project.get_status(name="ステータス")
        daily_log_relation = project.get_relation(name="デイリーログ")
        project_remind_date = project.get_date(name="リマインド")
        completed_at = project.get_date(name="終了日")
        recursive_conf = project.get_text(name="繰り返し設定")
        title = project.get_title()
        return {
            "id": project.id,
            "url": project.url,
            "daily_log_id": daily_log_relation.id_list,
            "goal_id_list": goal_relation.id_list,
            "status": status.status_name,
            "completed_at": completed_at.start,
            "recursive_conf": recursive_conf.text,
            "title": title.text,
            "remind_date": project_remind_date.start,
            "is_thisweek": is_thisweek.checked,
            "created_at": project.created_time.value,
            "updated_at": project.last_edited_time.value,
        }
