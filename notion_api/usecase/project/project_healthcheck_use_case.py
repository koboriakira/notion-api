from logging import Logger, getLogger

from lotion import Lotion
from lotion.block.rich_text import RichTextBuilder

from common.value.slack_channel_type import ChannelType
from notion_databases.project import Project
from notion_databases.project_prop.project_name import ProjectName
from notion_databases.task import Task
from notion_databases.task_prop.task_status import TaskStatusType
from project import project_repository
from project.project_repository import ProjectRepository
from task.task_repository import TaskRepository
from util.datetime import jst_today
from util.slack.slack_client import SlackClient


class ProjectHealthcheckUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
        slack_client: SlackClient,
        logger: Logger | None = None,
    ) -> None:
        self._lotion = Lotion.get_instance()
        self._project_repository = project_repository
        self._task_repository = task_repository
        self._slack_client = slack_client
        self._logger = logger or getLogger(__name__)

    def execute(self) -> None:
        projects = self._project_repository.fetch_all()
        self._slack_client.chat_postMessage("プロジェクトのヘルスチェックを開始します")

        # 進行中のプロジェクトのみを分析対象とする
        inprogress_projects = [project for project in projects if project.is_inprogress()]
        for project in inprogress_projects:
            undone_tasks = self._task_repository.search(
                project_id=project.id,
                status_list=[TaskStatusType.TODO, TaskStatusType.IN_PROGRESS],
            )
            self._execute_project(project, undone_tasks)

        # Inboxステータスは一覧だけ通知する
        inbox_projects = [project for project in projects if project.is_inbox()]
        self._execute_inbox_project(inbox_projects)

    def _execute_project(self, project: Project, tasks: list[Task]) -> None:  # noqa: C901
        message_list = []

        if not project.get_title_text().startswith("P:"):
            rich_text = RichTextBuilder.create().add_text("P:").add_rich_text(project.title.rich_text).build()
            project.set_prop(ProjectName.from_rich_text(rich_text))
            self._lotion.update(project)

        # スケジュールのチェック
        schedule = project.schedule
        if schedule is None or schedule.start_date is None or schedule.end_date is None:
            message_list.append("開始日、終了日を設定してください")
        elif schedule.end_date <= jst_today():
            message_list.append("終了日が過ぎています")

        # ゴール、アクションプランの未設定チェック
        if project.definition_of_done in [None, ""]:
            message_list.append("完了定義を記入してください")
        if project.weekly_goal in [None, ""]:
            message_list.append("今週の目標を記入してください")

        # 目標とのひもづきチェック
        if project.goal.id_list is None or len(project.goal.id_list) == 0:
            message_list.append("目標とのひもづきを設定してください")

        # タスクのチェック
        # 未了の「次にとるべき行動リスト」があるかどうか
        next_action_tasks = [task for task in tasks if task.is_next_action()]
        if len(next_action_tasks) == 0:
            message_list.append("次にとるべき行動をひとつ決めましょう")
        elif len(next_action_tasks) > 3:
            message_list.append("次にとるべき行動は3つまでにしましょう")

        text = f"{project.title_for_slack()}\n" + "\n".join(message_list)
        self._slack_client.chat_postMessage(text)

    def _execute_inbox_project(self, projects: list[Project]) -> None:
        if len(projects) == 0:
            return

        project_title_list = [project.title_for_slack() for project in projects]
        self._slack_client.chat_postMessage("Inboxには以下のプロジェクトがあります\n" + "\n".join(project_title_list))


if __name__ == "__main__":
    # python -m notion_api.usecase.project.project_healthcheck_use_case
    import logging

    from project.project_repository_impl import ProjectRepositoryImpl
    from task.task_repository_impl import TaskRepositoryImpl

    logging.basicConfig(level=logging.INFO)
    project_repository = ProjectRepositoryImpl(
        client=Lotion.get_instance(),
        logger=logging.getLogger(__name__),
    )
    task_repository = TaskRepositoryImpl(
        notion_client_wrapper=Lotion.get_instance(),
    )
    slack_client = SlackClient.bot(ChannelType.TEST, thread_ts=None)
    use_case = ProjectHealthcheckUseCase(
        project_repository=project_repository,
        task_repository=task_repository,
        slack_client=slack_client,
        logger=logging.getLogger(__name__),
    )

    use_case.execute()
