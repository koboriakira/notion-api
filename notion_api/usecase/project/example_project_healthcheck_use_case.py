from logging import Logger, getLogger

from slack_sdk import WebClient

from common.value.slack_channel_type import ChannelType
from notion_client_wrapper.client_wrapper import ClientWrapper
from project.domain import project_repository
from project.domain.project import Project
from project.domain.project_repository import ProjectRepository
from project.domain.project_status import ProjectStatusType
from task.domain.task import Task
from task.domain.task_kind import TaskKindType
from task.domain.task_repository import TaskRepository
from util.datetime import jst_today


class ExampleProjectHealthcheckUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
        slack_client: WebClient,
        logger: Logger | None = None,
    ) -> None:
        self._project_repository = project_repository
        self._task_repository = task_repository
        self._slack_client = slack_client
        self._logger = logger or getLogger(__name__)

    def execute(self) -> None:
        projects = self._project_repository.fetch_all()

        for project in projects:
            # TODO: Inboxステータスは一覧だけ通知する

            # 進行中のプロジェクトのみを分析対象とするため、その他はスキップ
            if project.project_status not in [ProjectStatusType.IN_PROGRESS]:
                continue

            tasks = self._task_repository.search(project_id=project.page_id)
            self._execute_project(project, tasks)

    def _execute_project(self, project: Project, tasks: list[Task]) -> None:  # noqa: C901
        project_title_link = project.title_for_slack()
        print(project_title_link)
        message_list = []

        # スケジュールのチェック
        schedule = project.schedule
        if schedule is None or schedule.start_date is None or schedule.end_date is None:
            message_list.append("開始日、終了日を設定してください")
        elif schedule.end_date <= jst_today():
            message_list.append("終了日が過ぎています")

        # ゴール、アクションプランの未設定チェック
        if project.definition_of_done in [None, ""]:
            message_list.append("完了定義を記入してください")
        if project.action_plan in [None, ""]:
            message_list.append("アクションプランを記入してください")

        # 目標とのひもづきチェック
        if project.goal_relation is None or len(project.goal_relation) == 0:
            message_list.append("目標とのひもづきを設定してください")

        # タスクのチェック
        # 未了の「次にとるべき行動リスト」があるかどうか
        next_action_tasks = [task for task in tasks if task.kind == TaskKindType.NEXT_ACTION]
        if len(next_action_tasks) == 0:
            message_list.append("次にとるべき行動をひとつ決めましょう")

        print("\n".join(message_list))
        print("====================================")
        self._slack_client.chat_postMessage(
            channel=ChannelType.TEST.value,
            text=f"{project_title_link}\n" + "\n".join(message_list),
        )


if __name__ == "__main__":
    # python -m notion_api.usecase.project.example_project_healthcheck_use_case
    import logging
    import os

    from project.infrastructure.project_repository_impl import ProjectRepositoryImpl
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    logging.basicConfig(level=logging.INFO)
    project_repository = ProjectRepositoryImpl(
        client=ClientWrapper.get_instance(),
        logger=logging.getLogger(__name__),
    )
    task_repository = TaskRepositoryImpl(
        notion_client_wrapper=ClientWrapper.get_instance(),
    )
    slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    use_case = ExampleProjectHealthcheckUseCase(
        project_repository=project_repository,
        task_repository=task_repository,
        slack_client=slack_client,
        logger=logging.getLogger(__name__),
    )

    use_case.execute()
