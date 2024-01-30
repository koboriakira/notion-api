from custom_logger import get_logger
from usecase.clean_empty_title_page import CleanEmptyTitlePageUsecase

logger = get_logger(__name__)

def clean_empty_title_page():
    usecase = CleanEmptyTitlePageUsecase()
    usecase.handle()
