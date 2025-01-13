from datetime import timedelta
from logging import Logger, getLogger

from lotion import Lotion
from lotion.block.rich_text import RichTextBuilder

from common.value.slack_channel_type import ChannelType
from notion_databases.goal import Goal
from notion_databases.goal_prop.goal_name import GoalName
from util.datetime import jst_today
from util.slack.slack_client import SlackClient


class GoalHealthcheckUseCase:
    def __init__(
        self,
        slack_client: SlackClient,
        logger: Logger | None = None,
        lotion: Lotion | None = None,
    ) -> None:
        self._slack_client = slack_client
        self._logger = logger or getLogger(__name__)
        self._lotion = lotion or Lotion.get_instance()

    def execute(self) -> None:
        goals = self._lotion.retrieve_pages(Goal)
        self._slack_client.chat_postMessage("目標のヘルスチェックを開始します")

        # Inboxステータスは一覧だけ通知する
        inbox_goals = [goal for goal in goals if goal.is_inbox()]
        self._execute_inbox_goal(inbox_goals)

        inprogress_goals = [goal for goal in goals if goal.is_in_progress()]
        for goal in inprogress_goals:
            self._execute_goal(goal)

    def _execute_goal(self, goal: Goal) -> None:
        message_list = []
        message_list.append(goal.title_for_slack())

        if not goal.get_title_text().startswith("G:"):
            # タイトルがG:から始まっていない場合は修正
            rich_text = RichTextBuilder.create().add_text("G:").add_rich_text(goal.title.rich_text).build()
            goal.set_prop(GoalName.from_rich_text(rich_text))
            self._lotion.update(goal)

        # スケジュールのチェック
        due_date = goal.due_date.start_date
        if due_date is None:
            message_list.append("期限を設定してください")
        elif due_date <= jst_today():
            message_list.append("期限を過ぎているため、期限を再設定するか、目標の達成度合いを振り返ってください")

        # ひもづくプロジェクトのチェック
        project_relation = goal.project_relation.id_list
        if project_relation is None or len(project_relation) == 0:
            message_list.append("関連プロジェクトが設定されていません")

        # 更新タイミングのチェック
        last_edited_time = goal.last_edited_time
        if last_edited_time is None:
            message_list.append("目標の更新日時が取得できませんでした")
        elif last_edited_time.date() < jst_today() - timedelta(days=14):
            message_list.append("目標の更新が2週間以上されていません")

        self._slack_client.chat_postMessage("\n".join(message_list))

    def _execute_inbox_goal(self, goals: list[Goal]) -> None:
        if len(goals) == 0:
            return

        goal_title_list = [goal.title_for_slack() for goal in goals]
        self._slack_client.chat_postMessage("Inboxには以下の目標があります\n" + "\n".join(goal_title_list))


if __name__ == "__main__":
    # python -m notion_api.usecase.goal.goal_healthcheck_use_case
    import logging

    logging.basicConfig(level=logging.INFO)
    # slack_client = MockSlackClient()
    slack_client = SlackClient.bot(ChannelType.TEST, thread_ts=None)
    use_case = GoalHealthcheckUseCase(
        slack_client=slack_client,
        logger=logging.getLogger(__name__),
    )

    use_case.execute()
