from domain.slack.slack_concierge_api import SlackConciergeAPI


class AppendPageIdToSlackContext:
    def __init__(self, slack_api: SlackConciergeAPI | None = None) -> None:
        from infrastructure.slack.lambda_slack_concierge_api import LambdaSlackConciergeAPI

        self.slack_api = slack_api or LambdaSlackConciergeAPI()

    def execute(self, channel: str, event_ts: str, page_id: str) -> None:
        context = {
            "page_id": page_id,
        }
        self.slack_api.append_context_block(channel=channel, event_ts=event_ts, context=context)
