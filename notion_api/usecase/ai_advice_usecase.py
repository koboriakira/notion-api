import json
from datetime import datetime, time, timedelta
from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.properties import Select

from common.service.gmail.gmail_service import GmailService
from custom_logger import get_logger
from infrastructure.slack_bot_client import SlackBotClient
from task.domain import Task
from task.domain.task_repository import TaskRepository
from task.domain.task_status import TaskStatusType
from util.datetime import jst_now
from util.line.line_client import LineClient
from util.openai_executer import OpenaiExecuter

logger = get_logger(__name__)


def find_promotion(pages: list[BasePage], promotion_name: str) -> Select | None:
    for page in pages:
        status = page.get_select(name="団体")
        if status.selected_name == promotion_name:
            return status
    return None


class AiAdviceUsecase:
    def __init__(self, task_repository: TaskRepository, logger: Logger | None = None):
        self._logger = logger or getLogger(__name__)
        self._client = Lotion.get_instance()
        self._task_repository = task_repository
        self._openai_executor = OpenaiExecuter()
        self._slack_client = SlackBotClient()
        self._gmail_service = GmailService()
        self._line_client = LineClient.get_instance()

    def execute(
        self,
        start_datetime: datetime,
    ) -> None:
        text = ""

        tasks = self._task_repository.search(
            start_datetime=start_datetime,
            start_datetime_end=start_datetime + timedelta(hours=3),
        )
        # 終日の予定になっているタスク
        allday_tasks = [t for t in tasks if t.start_datetime is not None and t.start_datetime.time() == time().min]

        # 3時間以内に開始するタスク
        current_tasks = [t for t in tasks if t.start_datetime is not None and t.start_datetime.time() != time().min]

        # 現時刻より前のタスク
        past_tasks = self._task_repository.search(
            start_datetime=start_datetime.date(),
            start_datetime_end=start_datetime,
        )
        past_tasks = [t for t in past_tasks if t.start_datetime is not None and t.start_datetime.time() != time().min]

        # 進行中のタスク
        current_tasks = self._task_repository.search(status_list=[TaskStatusType.IN_PROGRESS])

        current_tasks_description: list[str] = []
        if not current_tasks:
            current_tasks_description.append("進行中のタスクが記録されていません")
        else:
            # 開始してから30分以上経過した進行中タスク
            behind_current_tasks = [
                t
                for t in current_tasks
                if t.start_datetime is not None and (start_datetime - t.start_datetime).total_seconds() > 60 * 30
            ]
            for task in behind_current_tasks:
                if task.start_datetime is not None:
                    time_ = (start_datetime - task.start_datetime).total_seconds() / 60
                    current_tasks_description.append(
                        f"「{task.get_title_text()}」は開始してから{int(time_)}秒経過しています",
                    )

        if len(current_tasks_description) > 0:
            text += "\n".join(current_tasks_description)
            text += "\n====================\n"

        gmail_list = self._gmail_service.fetch_by_ai()
        if gmail_list:
            text += "\n読むべきメールがあります。\n"
            text += "\n".join([f"- {gmail.subject}" for gmail in gmail_list])

        # result = self.make_advice(
        #     start_datetime=start_datetime,
        #     allday_tasks=allday_tasks,
        #     current_tasks=current_tasks,
        #     past_tasks=past_tasks,
        # )
        # print(result)

        if text:
            self._line_client.push_message(text)

        # self._slack_client.send_message(
        #     channel="C05F6AASERZ",
        #     text=text,
        #     is_enabled_mention=True,
        # )

    def make_advice(
        self,
        start_datetime: datetime,
        allday_tasks: list[Task],
        current_tasks: list[Task],
        past_tasks: list[Task],
    ) -> str:
        allday_tasks_json = to_dict_list(allday_tasks)
        current_tasks_json = to_dict_list(current_tasks)
        past_tasks_json = to_dict_list(past_tasks)
        json_str = json.dumps(
            {
                "now": start_datetime.isoformat(),
                "current_tasks": current_tasks_json,
                "allday_tasks": allday_tasks_json,
                "past_tasks": past_tasks_json,
            },
            ensure_ascii=False,
            # indent=2,
        )
        prompt = f"""
あなたは私の最高の秘書です。
下記の情報をもとに、なるべく端的に現状をまとめあげ、次の行動を検討して教えてください。

## 制約
・いまは{start_datetime.isoformat()}です。
・下記のJSONは次のような構造です。
　　・now: 現在時刻
　　・current_tasks: 直近3時間以内に開始するタスクです
　　・allday_tasks: 明確な時刻はスケジューリングされてないTODOタスク
・与えた入力(JSON)をすべて扱う必要はありません。重要だと思われることに絞って連絡してください
・出力はカジュアルにお願いします

## JSON

{json_str}

"""
        print(prompt)
        return self._openai_executor.simple_chat(user_content=prompt)


def to_dict_list(tasks: list[Task]) -> list[dict]:
    return [
        {
            "title": t.get_title_text(),
            "start": t.start_datetime.isoformat() if t.start_datetime is not None else "",
            "end": t.end_datetime.isoformat() if t.end_datetime is not None else "",
            "status": t.status.value,
        }
        for t in tasks
    ]


if __name__ == "__main__":
    # python -m notion_api.usecase.ai_advice_usecase
    from notion_api.task.infrastructure.task_repository_impl import TaskRepositoryImpl

    task_repository = TaskRepositoryImpl()
    suite = AiAdviceUsecase(
        task_repository=task_repository,
    )
    # start_datetime = datetime(2024, 12, 18, 12, tzinfo=JST)
    start_datetime = jst_now()
    suite.execute(start_datetime=start_datetime)
