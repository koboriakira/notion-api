from task.domain.task_repository import TaskRepository


class DoTommorowUsecase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self) -> None:
        tasks = self._task_repository.search(do_tomorrow_flag=True)
        for task in tasks:
            self._task_repository.save(task=task.do_tomorrow())


if __name__ == "__main__":
    # python -m notion_api.usecase.task.do_tomorrow_usecase
    from custom_logger import get_logger
    from task.infrastructure.task_repository_impl import TaskRepositoryImpl

    logger = get_logger(__name__)

    task_repository = TaskRepositoryImpl()
    usecase = DoTommorowUsecase(task_repository=task_repository)
    usecase.execute()
