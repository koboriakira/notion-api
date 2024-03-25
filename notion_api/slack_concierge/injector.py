from slack_concierge.infrastructure.lambda_slack_concierge_api import LambdaSlackConciergeAPI
from slack_concierge.service.append_context_service import AppendContextService


class SlackConciergeInjector:
    @staticmethod
    def create_append_context_service() -> AppendContextService:
        slack_api = LambdaSlackConciergeAPI()
        return AppendContextService(slack_api=slack_api)
