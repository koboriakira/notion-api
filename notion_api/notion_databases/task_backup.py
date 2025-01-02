from lotion import notion_database
from lotion.base_page import BasePage
from lotion.block import Block

from common.value.database_type import DatabaseType
from notion_databases.goal import ProjectRelation
from notion_databases.task_prop.task_name import TaskName
from notion_databases.task_prop.task_start_date import TaskStartDate


@notion_database(DatabaseType.TASK_BK.value)
class TaskBackup(BasePage):
    task_name: TaskName
    project_relation: ProjectRelation
    task_date: TaskStartDate

    @staticmethod
    def generate(
        task_name: TaskName,
        project_relation: ProjectRelation,
        task_date: TaskStartDate,
        block_children: list[Block],
    ) -> "TaskBackup":
        return TaskBackup.create([task_name, project_relation, task_date], block_children)
