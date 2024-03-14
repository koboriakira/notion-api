from datetime import date as DateObject

from domain.database_type import DatabaseType
from domain.project.project_status import ProjectStatus
from notion_client_wrapper.client_wrapper import BasePage, ClientWrapper


class ProjectListUseCase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def execute(self,
                status_list: list[ProjectStatus] = [],
                remind_date: DateObject | None = None,
                goal_id: str | None = None,
                detail_enabled: bool = True,
                thisweek_filter_enabled: bool = False,
                completed_at: DateObject | None = None,
                ):
        status_name_list = [status.value for status in status_list]
        # まずプロジェクトを検索する
        searched_projects = self.client.retrieve_database(database_id=DatabaseType.PROJECT.value)

        projects = []
        for searched_project in searched_projects:
            project = self._convert_project(searched_project)
            # バリデーション: 目標
            if goal_id is not None and goal_id not in project["goal_id_list"]:
                continue
            # バリデーション: 今週やる
            if thisweek_filter_enabled and not project["is_thisweek"]:
                continue
            # バリデーション: ステータス
            if len(status_name_list) > 0 and project["status"] not in status_name_list:
                continue
            # バリデーション: リマインド日
            if remind_date is not None:
                if project["remind_date"] != remind_date.isoformat():
                    continue
            # バリデーション: 終了日
            if completed_at is not None:
                completed_date = searched_project.get_date(name="終了日")
                if completed_date.start != completed_at.isoformat():
                    continue

            # プロジェクトの詳細を取得する設定がある場合はタスクを取得する
            # if detail_enabled:
            #     project["tasks"] = self._find_tasks(project_id=project["id"])
            projects.append(project)

        return projects

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
