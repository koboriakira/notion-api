from datetime import datetime, timedelta
from logging import Logger

from lotion import Lotion
from lotion.block import BulletedListItem
from lotion.block.rich_text import RichTextBuilder
from lotion.filter import Builder, Cond

from custom_logger import get_logger
from notion_databases.daily_log import DailyLog, DailyLogTitle
from notion_databases.task import Task, TaskKind, TaskStatus
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_start_date import TaskStartDate
from notion_databases.task_prop.task_status import TaskStatusType
from util.datetime import jst_now
from util.line.line_client import LineClient


class MaintainTasksUsecase:
    def __init__(self, logger: Logger | None = None) -> None:
        self._logger = logger or get_logger(__name__)
        self._line_client = LineClient.get_instance()
        self._lotion = Lotion.get_instance(logger=self._logger)

    def execute(self) -> None:
        now = jst_now()

        # スケジュールされたタスクの開始
        # 一時的に無効化する
        # self._execute_scheduled(now)

        # 最終編集されたタスクのチェックマークをつける
        # および習慣トラッカーの更新
        self._execute_last_edited(now)

    def _execute_scheduled(self, now: datetime) -> None:
        filter_builder = Builder.create()
        status_prop = TaskStatus.from_status_type(TaskStatusType.TODO)
        filter_builder = filter_builder.add(status_prop, Cond.EQUALS)
        kind_prop = TaskKind.from_name(TaskKindType.SCHEDULE.value)
        filter_builder = filter_builder.add(kind_prop, Cond.EQUALS)
        start = TaskStartDate.from_start_date(now)
        filter_builder = filter_builder.add(start, Cond.ON_OR_AFTER)
        end = TaskStartDate.from_start_date(now + timedelta(minutes=3))
        filter_builder = filter_builder.add(end, Cond.ON_OR_BEFORE)
        filter_param = filter_builder.build()

        tasks = self._lotion.retrieve_pages(Task, filter_param)
        for task in tasks:
            self._lotion.update(task.start())
            self._line_client.push_message(f"タスク「{task.get_title_text()}」を開始しました")

    def _execute_last_edited(self, now: datetime) -> None:
        latest_edited_at = now - timedelta(minutes=10)
        tasks = self._lotion.search_page_by_last_edited_at(Task, start=latest_edited_at)
        daily_log = self._lotion.find_page(DailyLog, DailyLogTitle.from_date(now.date()))
        if daily_log is None:
            raise ValueError("DailyLog not found.")

        for task in tasks:
            if task.is_completed:
                if not task.get_title_text().startswith("✔️"):
                    self._logger.info(f"チェックマークをつける: {task.get_title_text()}")
                    self._lotion.update(task.add_check_prefix())
                if len(task.habit_relation.id_list) > 0:
                    self._logger.info(f"習慣トラッカーを更新: {task.get_title_text()}")
                    habit_page_id = task.habit_relation.id_list[0]
                    bulleted_list = BulletedListItem.from_rich_text(
                        RichTextBuilder.create().add_date_mention(now.date()).add_text(":◯").build(),
                    )
                    habit = self._lotion.append_block(habit_page_id, bulleted_list)
                    daily_log.append_habit(habit_page_id)

        self._lotion.update(daily_log)


if __name__ == "__main__":
    # python -m notion_api.usecase.task.maintain_tasks_usecase

    usecase = MaintainTasksUsecase()
    # usecase._execute_last_edited()
    usecase._execute_scheduled(jst_now())
