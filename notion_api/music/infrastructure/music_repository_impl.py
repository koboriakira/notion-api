from logging import Logger, getLogger

from common.value.database_type import DatabaseType
from music.domain.music_repository import MusicRepository
from notion_client_wrapper.client_wrapper import ClientWrapper


class MusicRepositoryImpl(MusicRepository):
    DATABASE_ID = DatabaseType.MUSIC.value

    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)
