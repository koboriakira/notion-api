from logging import Logger, getLogger

from common.value.database_type import DatabaseType
from goal.domain.goal import Goal
from goal.domain.goal_repository import GoalRepository
from notion_client_wrapper.client_wrapper import ClientWrapper


class GoalRepositoryImpl(GoalRepository):
    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def fetch_all(self) -> list[Goal]:
        return self._client.retrieve_database(database_id=DatabaseType.GOAL.value, page_model=Goal)
