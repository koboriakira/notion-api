from fastapi import APIRouter, Header
import logging

router = APIRouter()


@router.get("")
def healthcheck():
    """
    Return a greeting
    """
    logging.debug("healthcheck")
    logging.info("healthcheck")
    return {
        'status': 'ok',
    }
