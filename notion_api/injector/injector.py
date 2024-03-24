from slack_sdk.web import WebClient

from usecase.service.inbox_service import InboxService


class Injector:
    @staticmethod
    def create_inbox_service() -> InboxService:
        slack_client = WebClient()
        return InboxService(slack_client=slack_client)
