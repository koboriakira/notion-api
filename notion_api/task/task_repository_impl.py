from datetime import date, datetime, time, timedelta

from lotion import Lotion
from lotion.filter import Builder, Cond

from notion_databases.goal import ProjectRelation
from notion_databases.task import Task, TaskKind, TaskStartDate, TaskStatus
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType
from task.task_repository import TaskRepository
from util.datetime import JST


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
        last_edited_at: datetime | None = None,
    ) -> list[Task]:
        builder = Builder.create()
        trash_kind = TaskKind.trash()
        builder = builder.add(trash_kind, Cond.DOES_NOT_EQUAL)
        start_datetime_start = None
        if start_datetime is not None:
            start_datetime_start = (
                start_datetime
                if isinstance(start_datetime, datetime)
                else datetime.combine(start_datetime, time.min, tzinfo=JST)
            )
            # FIXME: add関数を使う
            builder = builder._add(
                "date",
                TaskStartDate.PROP_NAME,
                Cond.ON_OR_AFTER,
                start_datetime_start.isoformat(),
            )

        if start_datetime_end is not None:
            start_datetime_end = (
                start_datetime_end
                if isinstance(start_datetime_end, datetime)
                else datetime.combine(start_datetime_end, time.max, tzinfo=JST)
            )
            builder = builder._add("date", TaskStartDate.PROP_NAME, Cond.ON_OR_BEFORE, start_datetime_end.isoformat())
        elif start_datetime_start is not None:
            start_datetime_end = start_datetime_start + timedelta(days=1) - timedelta(seconds=1)
            builder = builder._add("date", TaskStartDate.PROP_NAME, Cond.ON_OR_BEFORE, start_datetime_end.isoformat())

        if project_id is not None:
            project_relation = ProjectRelation.from_id(project_id)
            builder = builder.add(project_relation, Cond.CONTAINS)

        if last_edited_at is not None:
            builder = builder.add_last_edited_at(Cond.ON_OR_AFTER, last_edited_at.isoformat())

        if kind_type_list is not None and len(kind_type_list) == 0:
            builder = builder.add(TaskKind, Cond.IS_EMPTY)

        # このあとor条件の追加をしていく

        if kind_type_list is not None and len(kind_type_list) > 0:
            or_builder = Builder.create()
            for kind_type in kind_type_list:
                or_builder = or_builder.add(TaskKind.from_name(kind_type.value), Cond.EQUALS)
                additional_conditions = or_builder.build("or")
            builder = builder.add_filter_param(additional_conditions)

        if status_list is not None and len(status_list) > 0:
            status_type_list = [s.value if isinstance(s, TaskStatusType) else s for s in status_list]
            or_builder = Builder.create()
            for status_type in status_type_list:
                or_builder = or_builder.add(TaskStatus.from_status_name(status_type), Cond.EQUALS)
                additional_conditions = or_builder.build("or")
            builder = builder.add_filter_param(additional_conditions)

        # print(json.dumps(builder.build(), ensure_ascii=False, indent=4))
        tasks = self.client.retrieve_pages(
            Task,
            filter_param=builder.build(),
        )
        # order昇順で並び替え
        tasks.sort(key=lambda x: x.order)
        return tasks

    def save(self, task: Task) -> Task:
        return self.client.update(task)

    def find_by_id(self, task_id: str) -> Task:
        return self.client.retrieve_page(task_id, Task)

    def move_to_backup(self, task: Task) -> None:
        # バックアップ用のデータベースにレコードを作成
        # タイトル、ステータス、実施日、タグ、プロジェクト、中身のみを移行
        if task.id is None:
            msg = "task.id が None です"
            raise ValueError(msg)

        # バックアップ用のデータベースに新規作成
        _ = self.client.create_page(task.to_backup_task())

        # タスクを削除
        self.client.remove_page(page_id=task.id)

    def delete(self, task: Task) -> None:
        self.client.remove_page(page_id=task.id)
