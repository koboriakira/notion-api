import json
from datetime import datetime, time, timedelta
from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.properties import Select

from custom_logger import get_logger
from infrastructure.slack_bot_client import SlackBotClient
from task.domain import Task
from task.domain.task_repository import TaskRepository
from util.datetime import JST
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

    def execute(
        self,
        start_datetime: datetime,
    ) -> None:
        tasks = self._task_repository.search(
            start_datetime=start_datetime,
            start_datetime_end=start_datetime + timedelta(hours=3),
        )
        allday_tasks = [t for t in tasks if t.start_datetime.time() == time().min]
        allday_tasks_json = to_dict_list(allday_tasks)
        current_tasks = [t for t in tasks if t.start_datetime.time() != time().min]
        current_tasks_json = to_dict_list(current_tasks)
        past_tasks = self._task_repository.search(
            start_datetime=start_datetime.date(),
            start_datetime_end=start_datetime,
        )
        past_tasks = [t for t in past_tasks if t.start_datetime.time() != time().min]
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
        result = self._openai_executor.simple_chat(user_content=prompt)
        print(result)
        self._slack_client.send_message(
            channel="C05F6AASERZ",
            text=result,
            is_enabled_mention=True,
        )


def to_dict_list(tasks: list[Task]) -> list[dict]:
    return [
        {
            "title": t.title,
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
    start_datetime = datetime(2024, 12, 18, 12, tzinfo=JST)
    suite.execute(start_datetime=start_datetime)
