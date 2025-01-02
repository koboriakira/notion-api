from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Date

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType
from notion_databases.project_prop.goal_relation import GoalRelation
from notion_databases.project_prop.project_name import ProjectName


@notion_prop("完了日")
class CompletedAt(Date):
    pass


@notion_database(DatabaseType.PROJECT_BK.value)
class ProjectBackup(BasePage):
    title: ProjectName
    completed_at: CompletedAt
    tags: TagRelation
    goal: GoalRelation

    @staticmethod
    def generate(  # noqa: PLR0913
        title: ProjectName,
        completed_at: CompletedAt,
        tags: TagRelation,
        goal: GoalRelation,
        block_children: list[Block] | None = None,
        cover: Cover | None = None,
    ) -> "ProjectBackup":
        return ProjectBackup.create(
            [title, completed_at, tags, goal],
            block_children,
            cover=cover,
        )
