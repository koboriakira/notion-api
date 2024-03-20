from datetime import date

from domain.database_type import DatabaseType
from domain.task.task import Task
from domain.task.task_kind import TaskKind, TaskKindType
from domain.task.task_repository import TaskRepository
from domain.task.task_start_date import TaskStartDate
from domain.task.task_status import TaskStatus, TaskStatusType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.date_condition import DateCondition
from notion_client_wrapper.filter.condition.or_condition import OrCondition
from notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_client_wrapper.filter.filter_builder import FilterBuilder


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, notion_client_wrapper: ClientWrapper|None=None) -> None:
        self.client = notion_client_wrapper or ClientWrapper.get_instance()


    def search(
            self,
            status_list: list[str]|None=None,
            task_kind: TaskKindType|None=None,
            start_date: date | None = None) -> list[Task]:
        task_kind_trash = TaskKind.trash()
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(StringCondition.not_equal(property=task_kind_trash))
        if start_date is not None:
            task_start_date = TaskStartDate.create(start_date)
            filter_builder = filter_builder.add_condition(DateCondition.equal(property=task_start_date))

        if task_kind is not None:
            task_kind_property = TaskKind.create(task_kind)
            filter_builder = filter_builder.add_condition(StringCondition.equal(property=task_kind_property))

        if status_list is not None and len(status_list) > 0:
            status_cond_list = TaskStatusType.get_status_list(status_list)
            task_status_list = [TaskStatus.from_status_type(status_type) for status_type in status_cond_list]
            task_status_equal_conditon = [StringCondition.equal(property=task_status) for task_status in task_status_list]
            or_condition = OrCondition(task_status_equal_conditon)
            filter_builder = filter_builder.add_condition(or_condition)

        return self.client.retrieve_database(
            database_id=DatabaseType.TASK.value,
            filter_param=filter_builder.build(),
            page_model=Task,
        )

    def save(
            self,
            task: Task) -> Task:
        if task.id is not None:
            _ = self.client.update_page(
                page_id=task.id,
                properties=task.properties.values)
            return task
        page = self.client.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=task.properties.values)
        return self.client.retrieve_page(page_id=page["id"], page_model=Task)
