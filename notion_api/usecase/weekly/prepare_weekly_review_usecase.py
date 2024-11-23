from datetime import timedelta
from logging import Logger

from custom_logger import get_logger
from notion_client_wrapper.properties.title import Title
from project.domain.project import Project
from project.domain.project_repository import ProjectRepository
from project.domain.project_status import ProjectStatusType
from task.domain.task import ToDoTask
from task.domain.task_kind import TaskKindType
from task.domain.task_repository import TaskRepository
from task.task_factory import TaskFactory
from util.datetime import jst_now


class PrepareWeeklyReviewUsecase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
        logger: Logger | None = None,
    ) -> None:
        self._project_repository = project_repository
        self._task_repository = task_repository

        self._logger = logger or get_logger(__name__)

        # いったん開始時刻を、今日の12:00にする
        self._start_date = jst_now().replace(hour=12, minute=0, second=0, microsecond=0)

    def execute(
        self,
    ) -> None:
        # 週次レビュー用のプロジェクトをひとつ作成
        review_project = self._project_repository.save(
            Project.create(
                title="週次レビュー",
                project_status=ProjectStatusType.IN_PROGRESS,
            ),
        )

        # 進行中のプロジェクトをレビューするタスクを作成して、週次レビュープロジェクトに紐づける
        projects = self._project_repository.fetch_all()
        ongoing_projects = [project for project in projects if project.status.is_in_progress()]
        for project in ongoing_projects:
            task = TaskFactory.create_todo_task(
                title=Title.from_mentioned_page_id(page_id=project.id),  # type: ignore
                project_id=review_project.page_id,
                task_kind_type=TaskKindType.NEXT_ACTION,
            )
            self._create_task(task)

        # TODO: 他にやることがあれば、続ける

    def _create_task(
        self,
        task: ToDoTask,
    ) -> None:
        """スケジュールを設定してからタスクを保存する"""
        task_ = task.update_start_datetime(start_datetime=self._start_date)

        # 次のタスク作成に、start_dateを5分進める
        # この開始時刻がこのタスクの終了時刻になる
        self._start_date = self._start_date + timedelta(minutes=5)
        task_ = task_.update_start_end_datetime(end=self._start_date)

        self._task_repository.save(task_)


if __name__ == "__main__":
    # python -m notion_api.usecase.weekly.prepare_weekly_review_usecase
    from project.infrastructure.project_repository_impl import ProjectRepositoryImpl
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    usecase = PrepareWeeklyReviewUsecase(
        project_repository=ProjectRepositoryImpl(),
        task_repository=TaskRepositoryImpl(),
    )
    usecase.execute()
