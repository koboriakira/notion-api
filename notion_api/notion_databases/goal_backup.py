from lotion import notion_database
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover

from common.value.database_type import DatabaseType
from notion_databases.goal_prop.goal_name import GoalName
from notion_databases.goal_prop.vision_relation import VisionRelation


@notion_database(DatabaseType.GOAL_BK.value)
class GoalBackup(BasePage):
    title: GoalName
    vision_relation: VisionRelation

    @staticmethod
    def generate(
        title: GoalName,
        vision_relation: VisionRelation,
        block_children: list[Block] | None = None,
        cover: Cover | None = None,
    ) -> "GoalBackup":
        return GoalBackup.create(
            [title, vision_relation],
            block_children,
            cover=cover,
        )
