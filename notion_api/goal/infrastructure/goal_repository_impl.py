from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.properties import Property

from common.value.database_type import DatabaseType
from goal.domain.goal import Goal
from goal.domain.goal_repository import GoalRepository
from goal.domain.vision_relation import VisionRelation


class GoalRepositoryImpl(GoalRepository):
    DATABASE_ID = DatabaseType.GOAL.value
    BACKUP_DATABASE_ID = DatabaseType.GOAL_BK.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def fetch_all(self, include_children: bool | None = None) -> list[Goal]:
        base_pages = self._client.retrieve_database(database_id=self.DATABASE_ID, include_children=include_children)
        return [self._cast(base_page) for base_page in base_pages]

    def remove(self, goal: Goal) -> None:
        if goal.id is None:
            raise ValueError("Goal id is None")
        self._client.remove_page(page_id=goal.id)

    def archive(self, goal: Goal) -> None:
        if goal.id is None:
            raise ValueError("Goal id is None")

        properties: list[Property] = [
            goal.get_title(),
        ]
        if goal.get_relation(VisionRelation.NAME) is not None:
            properties.append(goal.get_relation(VisionRelation.NAME))

        blocks = self._client.retrieve_page(page_id=goal.id).block_children

        self._client.create_page_in_database(
            database_id=self.BACKUP_DATABASE_ID,
            properties=properties,
            blocks=blocks,
        )

        self.remove(goal)

    def _cast(self, base_page: BasePage) -> Goal:
        return Goal(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
