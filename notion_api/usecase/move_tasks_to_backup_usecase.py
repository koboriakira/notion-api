from datetime import datetime, timedelta

from lotion import Lotion

from custom_logger import get_logger
from notion_databases.goal import Goal
from notion_databases.goal_backup import GoalBackup
from notion_databases.project import Project
from notion_databases.task_prop.task_status import TaskStatusType
from project.project_repository import ProjectRepository
from task.task_repository import TaskRepository
from util.datetime import JST, jst_now

logger = get_logger(__name__)


class MoveTasksToBackupUsecase:
    MIN_DATETIME = datetime(1970, 1, 1, tzinfo=JST)

    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
        lotion: Lotion | None = None,
    ) -> None:
        self._task_repository = task_repository
        self._project_repository = project_repository
        self._lotion = lotion or Lotion.get_instance()

    def execute(self) -> None:
        target_datetime = jst_now() - timedelta(days=14)
        self._proc_tasks(target_datetime)
        self._proc_projects(target_datetime)
        self._trash_projects()
        self._proc_goals(target_datetime)

    def _proc_tasks(self, target_datetime: datetime) -> None:
        # まず全てのタスクを集める
        tasks = self._task_repository.search(status_list=[TaskStatusType.DONE])

        # 直近更新されたものは無視
        tasks_moving_to_backup = [
            t
            for t in tasks
            if t.last_edited_time is not None and _is_between(t.last_edited_time, self.MIN_DATETIME, target_datetime)
        ]

        # バックアップ用のデータベースに移動
        for task in tasks_moving_to_backup:
            self._task_repository.move_to_backup(task)
            print(task.get_title().text + "をバックアップに移動しました。")

    def _proc_projects(self, target_datetime: datetime) -> None:
        # まず全てのプロジェクトを集める
        projects = self._project_repository.fetch_all()

        # Doneステータスのみに絞る
        projects = [t for t in projects if t.is_done()]

        # 直近更新されたものは無視するようにする
        projects = [
            p
            for p in projects
            if p.last_edited_time is not None and _is_between(p.last_edited_time, self.MIN_DATETIME, target_datetime)
        ]

        # バックアップ用のデータベースに移動
        for project in projects:
            self._project_repository.archive(project)
            print(project.get_title().text + "をバックアップに移動しました。")

    def _proc_goals(self, target_datetime: datetime) -> None:
        # まず全てのゴールを集める
        goals = self._lotion.retrieve_pages(Goal)

        # Doneステータスのみに絞る
        goals = [t for t in goals if t.is_done()]

        # 直近更新されたものは無視するようにする
        goals = [
            g
            for g in goals
            if g.last_edited_time is not None and _is_between(g.last_edited_time, self.MIN_DATETIME, target_datetime)
        ]

        # バックアップ用のデータベースに移動
        for goal in goals:
            self._archive_goal(goal)
            print(goal.title.text + "をバックアップに移動しました。")

    def _trash_projects(self) -> None:
        """Trashステータスのプロジェクトを削除する"""
        projects = self._lotion.retrieve_pages(Project)
        projects = [t for t in projects if t.is_trash()]
        for project in projects:
            tasks = self._task_repository.search(project_id=project.id)
            for task in tasks:
                self._task_repository.delete(task)
            self._project_repository.remove(project)
            print(project.title.text + "を削除しました。")

    def _archive_goal(self, goal: Goal) -> None:
        blocks = self._lotion.retrieve_page(page_id=goal.id, cls=Goal).block_children
        goal_backup = GoalBackup.generate(
            title=goal.title,
            vision_relation=goal.vision_relation,
            block_children=blocks,
            cover=goal.cover,
        )
        self._lotion.create_page(goal_backup)
        self._lotion.remove_page(goal.id)


def _is_between(target: datetime, start: datetime, end: datetime) -> bool:
    return start <= target <= end


if __name__ == "__main__":
    # python -m notion_api.usecase.move_tasks_to_backup_usecase
    from project.project_repository_impl import ProjectRepositoryImpl
    from task.task_repository_impl import TaskRepositoryImpl

    client = Lotion.get_instance()
    usecase = MoveTasksToBackupUsecase(
        task_repository=TaskRepositoryImpl(),
        project_repository=ProjectRepositoryImpl(client=client),
    )
    usecase.execute()
    # usecase._proc_goals(target_datetime=jst_now() - timedelta(days=14))
