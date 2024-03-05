from datetime import date as DateObject
from custom_logger import get_logger
from usecase.clean_empty_title_page import CleanEmptyTitlePageUsecase
from usecase.move_tasks_to_backup_usecase import MoveTasksToBackupUsecase
from usecase.fetch_tasks_usecase import FetchTasksUsecase
from infrastructure.current_task_s3_repository import CurrentTaskS3Repository

logger = get_logger(__name__)

def clean_empty_title_page():
    usecase = CleanEmptyTitlePageUsecase()
    usecase.handle()

def update_current_tasks() -> None:
    """ いまやるタスクの一覧キャッシュを更新 """
    usecase = FetchTasksUsecase()
    current_task_repository = CurrentTaskS3Repository()

    tasks = usecase.execute(
        status_list=["ToDo", "InProgress"],
        start_date=DateObject.today())
    current_task_repository.save(tasks)

    return True

def move_completed_task_to_backup() -> None:
    """ 実施日が過去のタスクをバックアップ """
    usecase = MoveTasksToBackupUsecase()
    return usecase.execute()
