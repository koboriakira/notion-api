from slack_concierge.infrastructure.lambda_slack_concierge_api import LambdaSlackConciergeAPI


class AppendContextService:
    def __init__(self, slack_api: LambdaSlackConciergeAPI|None = None) -> None:
        self.slack_api = slack_api or LambdaSlackConciergeAPI()

    def append_page_id(self, channel: str, event_ts:str, page_id: str) -> None:
        context = {"page_id": page_id}
        self.slack_api.append_context_block(channel, event_ts, context)
