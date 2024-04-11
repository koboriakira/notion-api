from injector.injector import Injector
from util.error_reporter import ErrorReporter


def handler(event: dict, context: dict) -> dict:  # noqa: ARG001
    try:
        usecase = Injector.create_collect_updated_pages_usecase()
        usecase.execute()
        return {
            "statusCode": 200,
        }
    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    # python -m notion_api.collect_updated_pages
    handler({}, {})
