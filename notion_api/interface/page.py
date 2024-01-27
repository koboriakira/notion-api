from typing import Optional
from datetime import date as Date
from usecase.append_feeling_usecase import AppendFeelingUsecase
from usecase.add_pomodoro_count_usecase import AddPomodoroCountUsecase
from custom_logger import get_logger

logger = get_logger(__name__)

def append_feeling(page_id: str,
                   value: str,
                   ) -> None:

    usecase = AppendFeelingUsecase()
    usecase.execute(page_id=page_id, value=value)

def add_pomodoro_count(page_id: str) -> None:
    usecase = AddPomodoroCountUsecase()
    usecase.execute(page_id=page_id)
