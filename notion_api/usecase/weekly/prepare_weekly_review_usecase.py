from logging import Logger

from lotion import Lotion
from lotion.block import BulletedListItem, Heading
from lotion.block.rich_text import RichTextBuilder
from lotion.properties import Title

from custom_logger import get_logger
from notion_databases.goal import Goal
from project.domain.project import Project
from project.domain.project_repository import ProjectRepository
from project.domain.project_status import ProjectStatusType
from task.domain.task import ToDoTask
from task.domain.task_kind import TaskKindType
from task.domain.task_repository import TaskRepository
from task.task_factory import TaskFactory
from util.datetime import jst_now, jst_today


class PrepareWeeklyReviewUsecase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
        logger: Logger | None = None,
    ) -> None:
        self._project_repository = project_repository
        self._task_repository = task_repository
        self._lotion = Lotion.get_instance()

        self._logger = logger or get_logger(__name__)

        # いったん開始時刻を、今日の12:00にする
        self._start_date = jst_now().replace(hour=12, minute=0, second=0, microsecond=0)

    def execute(
        self,
    ) -> None:
        # 週次レビュー用のプロジェクトをひとつ作成
        _, isoweeknum, _ = jst_today().isocalendar()
        review_project = self._project_repository.save(
            Project.generate(
                title="週次レビュー Week" + str(isoweeknum),
                project_status=ProjectStatusType.IN_PROGRESS,
            ),
        )

        # 進行中のプロジェクトを持つ目標をレビューする
        # 目標をレビューするので、自然とプロジェクトレビューにもなるはず
        projects = self._fetch_inprogress_projects()
        projects_as_goal = self._generate_projects_as_goal(projects)
        self._create_mention_in_each_goal(projects_as_goal, review_project)
        self._create_tasks_as_goal_review(review_project, list(projects_as_goal.keys()))

        # 目標のひも付きがないやつは、別途タスクとしてつくる
        nongoal_projects = [p for p in projects if len(p.goal.id_list) == 0]
        self._create_tasks_as_project_review(review_project, nongoal_projects)

    def _fetch_inprogress_projects(
        self,
    ) -> list[Project]:
        projects = self._project_repository.fetch_all()
        return [project for project in projects if project.is_inprogress()]

    def _create_tasks_as_project_review(self, review_project: Project, projects: list[Project]) -> None:
        for project in projects:
            task = TaskFactory.create_todo_task(
                title=Title.from_mentioned_page_id(page_id=project.id),  # type: ignore
                project_id=review_project.id,
                task_kind_type=TaskKindType.NEXT_ACTION,
            )
            self._create_task(task)

    def _create_tasks_as_goal_review(self, review_project: Project, goal_page_id_list: list[str]) -> None:
        for page_id in goal_page_id_list:
            task = TaskFactory.create_todo_task(
                title=Title.from_mentioned_page_id(page_id=page_id),  # type: ignore
                project_id=review_project.id,
                task_kind_type=TaskKindType.NEXT_ACTION,
            )
            self._create_task(task)

    def _generate_projects_as_goal(self, projects: list[Project]) -> dict[str, list[Project]]:
        """目標ごとのプロジェクトを整理する"""
        goals = self._lotion.retrieve_pages(Goal)
        projects_as_goal: dict[str, list[Project]] = {}
        for g in goals:
            projects_as_goal[g.id] = []

        for p in projects:
            for goal_page_id in p.goal.id_list:
                projects_as_goal[goal_page_id].append(p)

        return {g: projects for g, projects in projects_as_goal.items() if len(projects) > 0}

    def _create_mention_in_each_goal(
        self,
        projects_as_goal: dict[str, list[Project]],
        review_project: Project,
    ) -> None:
        """目標ページにメンション追加"""
        for goal_page_id, projects in projects_as_goal.items():
            rich_text = RichTextBuilder.create().add_date_mention(start=jst_today()).build()
            heading = Heading.from_rich_text(heading_size=2, rich_text=rich_text)
            self._lotion.append_block(goal_page_id, heading)
            for p in projects:
                rich_text = RichTextBuilder.create().add_page_mention(p.id).build()
                paragraph = BulletedListItem.from_rich_text(rich_text)
                self._lotion.append_block(goal_page_id, paragraph)
            task = TaskFactory.create_todo_task(
                title=Title.from_mentioned_page_id(page_id=goal_page_id),  # type: ignore
                project_id=review_project.id,
                task_kind_type=TaskKindType.NEXT_ACTION,
            )
            self._create_task(task)

    def _create_task(
        self,
        task: ToDoTask,
    ) -> None:
        """タスクを保存する"""
        self._task_repository.save(task)


if __name__ == "__main__":
    # python -m notion_api.usecase.weekly.prepare_weekly_review_usecase
    from project.infrastructure.project_repository_impl import ProjectRepositoryImpl
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    lotion = Lotion.get_instance()
    project_repository = ProjectRepositoryImpl()
    task_repository = TaskRepositoryImpl()
    usecase = PrepareWeeklyReviewUsecase(
        project_repository=project_repository,
        task_repository=task_repository,
    )
    usecase.execute()
