from datetime import date, datetime, time

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
from util.datetime import JST


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, notion_client_wrapper: ClientWrapper | None = None) -> None:
        self.client = notion_client_wrapper or ClientWrapper.get_instance()

    def search(
        self,
        status_list: list[str | TaskStatusType] | None = None,
        kind_type_list: list[TaskKindType] | None = None,
        start_date: date | None = None,
    ) -> list[Task]:
        task_kind_trash = TaskKind.trash()
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(StringCondition.not_equal(property=task_kind_trash))
        if start_date is not None:
            target_date_after = datetime.combine(start_date, time.min, tzinfo=JST)
            target_date_before = datetime.combine(start_date, time.max, tzinfo=JST)
            task_start_date_after = TaskStartDate.create(target_date_after)
            task_start_date_before = TaskStartDate.create(target_date_before)
            filter_builder = filter_builder.add_condition(DateCondition.on_or_after(property=task_start_date_after))
            filter_builder = filter_builder.add_condition(DateCondition.before(property=task_start_date_before))

        if kind_type_list is not None and len(kind_type_list) > 0:
            task_kind_properties = [TaskKind.create(kind_type=kind_type) for kind_type in kind_type_list]
            task_kind_equal_conditions = [
                StringCondition.equal(property=task_kind) for task_kind in task_kind_properties
            ]
            or_condition = OrCondition(task_kind_equal_conditions)
            filter_builder = filter_builder.add_condition(or_condition)

        if status_list is not None and len(status_list) > 0:
            if isinstance(status_list[0], str):
                status_list = TaskStatusType.get_status_list(status_list)
            task_status_list = [TaskStatus.from_status_type(status_type) for status_type in status_list]
            task_status_equal_conditon = [
                StringCondition.equal(property=task_status) for task_status in task_status_list
            ]
            or_condition = OrCondition(task_status_equal_conditon)
            filter_builder = filter_builder.add_condition(or_condition)

        print(filter_builder.build())
        return self.client.retrieve_database(
            database_id=DatabaseType.TASK.value,
            filter_param=filter_builder.build(),
            page_model=Task,
        )

    def save(self, task: Task) -> Task:
        if task.id is not None:
            print(task.properties.values)
            _ = self.client.update_page(page_id=task.id, properties=task.properties.values)
            return task
        page = self.client.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=task.properties.values,
            blocks=task.block_children,
        )
        return self.client.retrieve_page(page_id=page["id"], page_model=Task)

    def find_by_id(self, task_id: str) -> Task:
        return self.client.retrieve_page(page_id=task_id, page_model=Task)
