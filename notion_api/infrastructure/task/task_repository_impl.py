from datetime import date

from domain.database_type import DatabaseType
from domain.task.task import Task
from domain.task.task_kind import TaskKind
from domain.task.task_repository import TaskRepository
from domain.task.task_start_date import TaskStartDate
from domain.task.task_status import TaskStatus
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.date_condition import DateCondition
from notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_client_wrapper.filter.filter_builder import FilterBuilder


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, notion_client_wrapper: ClientWrapper|None=None) -> None:
        self.client = notion_client_wrapper or ClientWrapper.get_instance()


    def search(
            self,
            status_list: list[str]|None=None,
            start_date: date | None = None) -> list[Task]:
        status_cond_list = TaskStatus.get_status_list(status_list)
        status_cond_name_list = [s.value for s in status_cond_list]

        # FIXME: 最終的にはretrieve_databaseのなかで検索が終わるようにする
        task_kind = TaskKind.trash()
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(StringCondition.not_equal(property=task_kind))
        if start_date is not None:
            task_start_date = TaskStartDate.create(start_date)
            filter_builder = filter_builder.add_condition(DateCondition.equal(property=task_start_date))
        all_tasks:list[Task] = self.client.retrieve_database(
            database_id=DatabaseType.TASK.value,
            filter_param=filter_builder.build(),
            page_model=Task)
        tasks = []
        for task in all_tasks:
            if len(status_cond_list) > 0 and task.status not in status_cond_name_list:
                continue
            tasks.append(task)

        return tasks
