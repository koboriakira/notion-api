from custom_logger import get_logger
from usecase.append_block import AppendBlockUsecase
from usecase.append_feeling_usecase import AppendFeelingUsecase
from usecase.update_status_usecase import UpdateStatusUsecase

logger = get_logger(__name__)


def append_feeling(
    page_id: str,
    value: str,
) -> None:
    usecase = AppendFeelingUsecase()
    usecase.execute(page_id=page_id, value=value)


def update_status(
    page_id: str,
    value: str,
) -> None:
    usecase = UpdateStatusUsecase()
    usecase.execute(page_id=page_id, value=value)


def append_text_block(
    page_id: str,
    value: str,
) -> None:
    usecase = AppendBlockUsecase()
    usecase.append_text(page_id=page_id, value=value)
