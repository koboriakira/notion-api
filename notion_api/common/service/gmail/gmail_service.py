import os

import requests


class GmailService:
    def __init__(self, gas_gmail_url: str | None = None) -> None:
        self._url = os.environ["GAS_GMAIL_URL"]
        lambda_gas_gmail_secret = os.getenv("LAMBDA_GAS_GMAIL_SECRET")
        if not lambda_gas_gmail_secret:
            lambda_gas_gmail_secret = ""
        self._headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + lambda_gas_gmail_secret,
        }

    def fetch(self) -> None:
        # params = {
        #     "start_date": date_.isoformat(),
        #     "end_date": date_.isoformat(),
        # }

        response = requests.get(url=self._url, headers=self._headers, timeout=30)
        response.raise_for_status()
        # self._logger.debug(f"get_gas_calendar: status_code={response.status_code}")
        print(response.json())


if __name__ == "__main__":
    # python -m notion_api.common.service.gmail.gmail_service

    suite = GmailService()
    print(suite.fetch())
