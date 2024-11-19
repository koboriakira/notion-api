from datetime import datetime, timedelta

from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from project.domain.project_repository import ProjectRepository
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from util.datetime import JST, jst_now

logger = get_logger(__name__)


class MoveTasksToBackupUsecase:
    MIN_DATETIME = datetime(1970, 1, 1, tzinfo=JST)

    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository) -> None:
        self._task_repository = task_repository
        self._project_repository = project_repository

    def execute(self) -> None:
        target_datetime = jst_now() - timedelta(days=14)
        self._proc_tasks(target_datetime)
        self._proc_projects(target_datetime)
        self._trash_projects()

    def _proc_tasks(self, target_datetime: datetime) -> None:
        # まず全てのタスクを集める
        tasks = self._task_repository.search(status_list=[TaskStatusType.DONE])

        # 直近更新されたものは無視
        tasks_moving_to_backup = [
            t
            for t in tasks
            if t.last_edited_time is not None and t.last_edited_time.is_between(self.MIN_DATETIME, target_datetime)
        ]

        # バックアップ用のデータベースに移動
        for task in tasks_moving_to_backup:
            self._task_repository.move_to_backup(task)
            print(task.get_title().text + "をバックアップに移動しました。")

    def _proc_projects(self, target_datetime: datetime) -> None:
        # まず全てのプロジェクトを集める
        projects = self._project_repository.fetch_all()

        # Doneステータスのみに絞る
        projects = [t for t in projects if t.project_status.is_done()]

        # 直近更新されたものは無視するようにする
        projects = [
            p
            for p in projects
            if p.last_edited_time is not None and p.last_edited_time.is_between(self.MIN_DATETIME, target_datetime)
        ]

        # バックアップ用のデータベースに移動
        for project in projects:
            self._project_repository.archive(project)
            print(project.get_title().text + "をバックアップに移動しました。")

    def _trash_projects(self) -> None:
        """ Trashステータスのプロジェクトを削除する """
        projects = self._project_repository.fetch_all()
        projects = [t for t in projects if t.project_status.is_trash()]
        for project in projects:
            tasks = self._task_repository.search(project_id=project.page_id)
            for task in tasks:
                self._task_repository.delete(task)
            self._project_repository.remove(project)
            print(project.get_title().text + "を削除しました。")

if __name__ == "__main__":
    # python -m notion_api.usecase.move_tasks_to_backup_usecase
    from project.infrastructure.project_repository_impl import ProjectRepositoryImpl
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl
    usecase = MoveTasksToBackupUsecase(
        task_repository=TaskRepositoryImpl(),
        project_repository=ProjectRepositoryImpl(client=ClientWrapper.get_instance()),
    )
    usecase.execute()
