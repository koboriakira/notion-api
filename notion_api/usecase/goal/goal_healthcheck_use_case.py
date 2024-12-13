from logging import Logger, getLogger

from common.value.slack_channel_type import ChannelType
from goal.domain.goal import Goal
from goal.domain.goal_repository import GoalRepository
from lotion import Lotion
from util.datetime import jst_today
from util.slack.slack_client import SlackClient


class GoalHealthcheckUseCase:
    def __init__(
        self,
        goal_repository: GoalRepository,
        slack_client: SlackClient,
        logger: Logger | None = None,
    ) -> None:
        self._goal_repository = goal_repository
        self._slack_client = slack_client
        self._logger = logger or getLogger(__name__)

    def execute(self) -> None:
        goals = self._goal_repository.fetch_all()
        self._slack_client.chat_postMessage("目標のヘルスチェックを開始します")

        # Inboxステータスは一覧だけ通知する
        inbox_goals = [goal for goal in goals if goal.goal_status.is_inbox()]
        self._execute_inbox_goal(inbox_goals)

        inprogress_goals = [goal for goal in goals if goal.goal_status.is_in_progress()]
        for goal in inprogress_goals:
            self._execute_goal(goal)

    def _execute_goal(self, goal: Goal) -> None:
        message_list = []
        message_list.append(goal.title_for_slack())

        # スケジュールのチェック
        if goal is None or goal.due_date is None:
            message_list.append("期限を設定してください")
        elif goal.due_date <= jst_today():
            message_list.append("期限を過ぎているため、期限を再設定するか、目標の達成度合いを振り返ってください")
        self._slack_client.chat_postMessage("\n".join(message_list))

    def _execute_inbox_goal(self, goals: list[Goal]) -> None:
        if len(goals) == 0:
            return

        goal_title_list = [goal.title_for_slack() for goal in goals]
        self._slack_client.chat_postMessage("Inboxには以下の目標があります\n" + "\n".join(goal_title_list))


if __name__ == "__main__":
    # python -m notion_api.usecase.goal.goal_healthcheck_use_case
    import logging

    from goal.infrastructure.goal_repository_impl import GoalRepositoryImpl

    logging.basicConfig(level=logging.INFO)
    goal_repository = GoalRepositoryImpl(
        client=Lotion.get_instance(),
        logger=logging.getLogger(__name__),
    )
    # slack_client = MockSlackClient()
    slack_client = SlackClient.bot(ChannelType.TEST, thread_ts=None)
    use_case = GoalHealthcheckUseCase(
        goal_repository=goal_repository,
        slack_client=slack_client,
        logger=logging.getLogger(__name__),
    )

    use_case.execute()
