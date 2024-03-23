
from custom_logger import get_logger
from usecase.clean_empty_title_page import CleanEmptyTitlePageUsecase
from usecase.move_tasks_to_backup_usecase import MoveTasksToBackupUsecase

logger = get_logger(__name__)

def clean_empty_title_page():
    usecase = CleanEmptyTitlePageUsecase()
    usecase.handle()


def move_completed_task_to_backup() -> None:
    """ 実施日が過去のタスクをバックアップ """
    usecase = MoveTasksToBackupUsecase()
    return usecase.execute()
