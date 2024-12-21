from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.filter import Builder, Cond, Prop

from common.value.database_type import DatabaseType
from task.domain.do_tomorrow_flag import DoTommorowFlag
from task.domain.important_flag import ImportantFlag
from task.domain.is_started import IsStarted
from task.domain.project_relation import ProjectRelation
from task.domain.task import ImportantToDoTask, RoutineToDoTask, ScheduledTask, Task, ToDoTask
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_repository import TaskRepository
from task.domain.task_start_date import TaskStartDate
from task.domain.task_status import TaskStatus, TaskStatusType
from util.datetime import JST

if TYPE_CHECKING:
    from lotion.properties import Property


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, notion_client_wrapper: Lotion | None = None) -> None:
        self.client = notion_client_wrapper or Lotion.get_instance()

    def search(  # noqa: PLR0913
        self,
        status_list: list[str | TaskStatusType] | None = None,
        kind_type_list: list[TaskKindType] | None = None,
        start_datetime: date | datetime | None = None,
        start_datetime_end: date | datetime | None = None,
        project_id: str | None = None,
        do_tomorrow_flag: bool | None = None,
        is_started: bool | None = None,
        last_edited_at: datetime | None = None,
    ) -> list[Task]:
        builder = Builder.create()
        builder = builder.add(Prop.SELECT, TaskKind.NAME, Cond.DOES_NOT_EQUAL, TaskKindType.TRASH.value)
        if start_datetime is not None:
            start_datetime = (
                start_datetime
                if isinstance(start_datetime, datetime)
                else datetime.combine(start_datetime, time.min, tzinfo=JST)
            )
            builder = builder.add(Prop.DATE, TaskStartDate.NAME, Cond.ON_OR_AFTER, start_datetime.isoformat())

        if start_datetime_end is not None:
            start_datetime_end = (
                start_datetime_end
                if isinstance(start_datetime_end, datetime)
                else datetime.combine(start_datetime_end, time.max, tzinfo=JST)
            )
            builder = builder.add(Prop.DATE, TaskStartDate.NAME, Cond.ON_OR_BEFORE, start_datetime_end.isoformat())
        elif start_datetime is not None:
            start_datetime_end = start_datetime + timedelta(days=1) - timedelta(seconds=1)
            builder = builder.add(Prop.DATE, TaskStartDate.NAME, Cond.ON_OR_BEFORE, start_datetime_end.isoformat())

        if project_id is not None:
            builder = builder.add(Prop.RELATION, ProjectRelation.NAME, Cond.EQUALS, project_id)

        if do_tomorrow_flag is not None:
            builder = builder.add(Prop.CHECKBOX, DoTommorowFlag.NAME, Cond.EQUALS, do_tomorrow_flag)

        if is_started is not None:
            builder = builder.add(Prop.CHECKBOX, IsStarted.NAME, Cond.EQUALS, is_started)

        if last_edited_at is not None:
            builder = builder.add_last_edited_at(Cond.ON_OR_AFTER, last_edited_at.isoformat())

        if kind_type_list is not None and len(kind_type_list) == 0:
            builder = builder.add(Prop.SELECT, TaskKind.NAME, Cond.IS_EMPTY, True)  # noqa: FBT003

        # このあとor条件の追加をしていく

        if kind_type_list is not None and len(kind_type_list) > 0:
            values = [kind_type.value for kind_type in kind_type_list]
            builder = Builder(
                conditions=[
                    *builder.conditions,
                    {
                        "or": [
                            Builder.create().add(Prop.SELECT, TaskKind.NAME, Cond.EQUALS, v).build() for v in values
                        ],
                    },
                ],
            )

        if status_list is not None and len(status_list) > 0:
            status_type_list = [s.value if isinstance(s, TaskStatusType) else s for s in status_list]
            builder = Builder(
                conditions=[
                    *builder.conditions,
                    {
                        "or": [
                            Builder.create().add(Prop.STATUS, TaskStatus.NAME, Cond.EQUALS, v).build()
                            for v in status_type_list
                        ],
                    },
                ],
            )

        # print(json.dumps(builder.build(), ensure_ascii=False, indent=4))
        base_pages = self.client.retrieve_database(
            database_id=DatabaseType.TASK.value,
            filter_param=builder.build(),
        )
        tasks: list[Task] = []
        for base_page in base_pages:
            task = self._cast(base_page)
            tasks.append(task)
        # order昇順で並び替え
        tasks.sort(key=lambda x: x.order)
        return tasks

    def save(self, task: Task) -> Task:
        if task.is_created():
            _ = self.client.update_page(page_id=task.id, properties=task.properties.values)
            return task
        page = self.client.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=task.properties.values,
            blocks=task.block_children,
        )
        return self.find_by_id(task_id=page.id)

    def find_by_id(self, task_id: str) -> Task:
        base_page = self.client.retrieve_page(page_id=task_id)
        return self._cast(base_page)

    def move_to_backup(self, task: Task) -> None:
        # バックアップ用のデータベースにレコードを作成
        # タイトル、ステータス、実施日、タグ、プロジェクト、中身のみを移行
        if task.id is None:
            msg = "task.id が None です"
            raise ValueError(msg)
        properties: list[Property] = [
            task.get_title(),
        ]
        if task.get_date("実施日").start is not None:
            properties.append(task.get_date("実施日"))
        if task.get_relation("タグ") is not None:
            properties.append(task.get_relation("タグ"))
        if task.get_relation("プロジェクト") is not None:
            properties.append(task.get_relation("プロジェクト"))

        self.client.create_page_in_database(
            database_id=DatabaseType.TASK_BK.value,
            properties=properties,
            blocks=task.block_children,
        )

        # タスクを削除
        self.client.remove_page(page_id=task.id)

    def delete(self, task: Task) -> None:
        self.client.remove_page(page_id=task.id)

    def _cast(self, base_page: BasePage) -> Task:
        cls = ToDoTask
        important_flag = base_page.get_checkbox(ImportantFlag.NAME)
        if important_flag is not None and important_flag.checked:
            cls = ImportantToDoTask
        kind_model = base_page.get_select(name=TaskKind.NAME)
        if kind_model is not None and kind_model.selected_name != "":
            task_type = TaskKindType(kind_model.selected_name)
            if task_type == TaskKindType.SCHEDULE:
                cls = ScheduledTask
            if task_type == TaskKindType.ROUTINE:
                cls = RoutineToDoTask
        return cls(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url_=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
