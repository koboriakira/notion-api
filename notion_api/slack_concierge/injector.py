from notion_api.slack_concierge.service.append_context_service import AppendContextService
from slack_concierge.infrastructure.lambda_slack_concierge_api import LambdaSlackConciergeAPI


class SlackConciergeInjector:
    @staticmethod
    def create_append_context_service() -> AppendContextService:
        slack_api = LambdaSlackConciergeAPI()
        return AppendContextService(slack_api=slack_api)
