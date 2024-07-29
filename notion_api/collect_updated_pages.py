from datetime import timedelta

from injector.injector import Injector
from util.date_range import DateRange
from util.datetime import jst_now
from util.error_reporter import ErrorReporter


def handler(event: dict, context: dict) -> dict:  # noqa: ARG001
    try:
        usecase = Injector.create_collect_updated_pages_usecase()
        end_datetime = jst_now()
        start_datetime = end_datetime - timedelta(hours=24)
        date_range = DateRange.from_datetime(start=start_datetime, end=end_datetime)
        usecase.execute(date_range=date_range)
        return {
            "statusCode": 200,
        }
    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    # python -m notion_api.collect_updated_pages
    handler({}, {})
