from typing import Optional
from datetime import date as Date
from usecase.add_track_page_usecase import AddTrackPageUsecase
from custom_logger import get_logger

logger = get_logger(__name__)

def add_track_page(track_name: str,
                   artists: list[str],
                   spotify_url: Optional[str] = None,
                   cover_url: Optional[str] = None,
                   release_date: Optional[Date] = None,
                   ):
    logger.debug(f"track_name: {track_name}")
    logger.debug(f"artists: {artists}")
    logger.debug(f"spotify_url: {spotify_url}")
    logger.debug(f"cover_url: {cover_url}")
    logger.debug(f"release_date: {release_date}")
    usecase = AddTrackPageUsecase()
    result = usecase.execute(track_name=track_name,
                           artists=artists,
                           spotify_url=spotify_url,
                           cover_url=cover_url,
                           release_date=release_date,
                           )
    logger.debug(result)
    return result
