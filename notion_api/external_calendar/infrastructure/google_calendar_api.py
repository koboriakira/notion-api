import os
from datetime import date
from logging import Logger

import requests

import custom_logger
from external_calendar.domain.event import Events
from external_calendar.domain.event_converter import EventConverter
from external_calendar.domain.external_calendar_api import ExternalCalendarAPI


class GoogleCalendarApi(ExternalCalendarAPI):
    def __init__(self, logger: Logger | None = None) -> None:
        self._logger = logger or custom_logger.get_logger(__name__)
        self.domain = os.environ["LAMBDA_GOOGLE_CALENDAR_API_DOMAIN"]
        self.headers = {
            "Accept": "application/json",
            "access-token": "Bearer "
            + os.environ["LAMBDA_GOOGLE_CALENDAR_API_ACCESS_TOKEN"],
        }

    def fetch(self, date_: date) -> Events:
        url = self.domain + "/list"
        params = {
            "start_date": date_.isoformat(),
            "end_date": date_.isoformat(),
        }

        response = requests.get(url=url, params=params, headers=self.headers, timeout=30)
        response.raise_for_status()
        self._logger.debug(f"get_gas_calendar: status_code={response.status_code}")
        return EventConverter.to_objects(response.json())

    # def get_current_schedules(self) -> list[dict]:
    #     """直近のスケジュールを取得する。デフォルトで5分先"""
    #     url = self.domain + "next_schedules"
    #     headers = {
    #         "Accept": "application/json",
    #         "access-token": self.access_token,
    #     }
    #     response = requests.get(url=url, headers=headers)
    #     self._logger.debug(f"post_gas_calendar: status_code={response.status_code}")
    #     response_json = response.json()
    #     if isinstance(response_json, str):
    #         response_json = json.loads(response_json)
    #     self._logger.debug(f"post_gas_calendar: response={response_json}")
    #     return response_json

    # def get(self, path: str, params: dict) -> list[dict]:
    #     url = f"{self.domain}{path}"
    #     headers = {
    #         "Accept": "application/json",
    #         "access-token": self.access_token,
    #     }
    #     response = requests.get(url=url, headers=headers, params=params, timeout=30)
    #     if response.status_code != 200:
    #         error_message = f"GET: {response.text} {url} params={json.dumps(params, ensure_ascii=False)} status_code={response.status_code} headers={headers}"
    #         self._logger.exception(error_message)
    #         raise ValueError(error_message)

    #     response_json = response.json()
    #     if isinstance(response_json, str):
    #         response_json = json.loads(response_json)
    #     debug_message = f"GET: {url} response={response_json}"
    #     self._logger.debug(debug_message)
    #     return response_json

    # def get_gas_calendar_achievements(self, date: date) -> list[dict]:
    #     raise NotImplementedError
    #     # params = {
    #     #     "start_date": date.isoformat(),
    #     #     "end_date": date.isoformat(),
    #     #     "achievement": True,
    #     # }
    #     # response = requests.get(url=self.domain, params=params)
    #     # logging.debug(f"get_gas_calendar_achievements: status_code={response.status_code}")
    #     # return response.json()

    # def post_schedule(self, schedule: Any) -> bool:
    #     return self.post_gas_calendar(
    #         start=schedule.start,
    #         end=schedule.end,
    #         category=schedule.category,
    #         title=schedule.title,
    #         detail=(
    #             schedule.detail.to_yaml_str() if schedule.detail is not None else None
    #         ),
    #     )

    # def delete_gas_calendar(self, date: date, category: str, title: str) -> dict:
    #     return {}
    #     params = {
    #         "date": date.isoformat(),
    #         "category": category,
    #         "title": title,
    #     }
    #     return requests.delete(url=self.domain, params=params).json()

    # def post_gas_calendar(
    #     self,
    #     start: datetime,
    #     end: datetime,
    #     category: str,
    #     title: str,
    #     detail: str | None = None,
    # ) -> bool:
    #     """カレンダーを追加する"""
    #     url = self.domain + "schedule"
    #     data = {
    #         "category": category,
    #         "title": title,
    #         "start": start.isoformat(),
    #         "end": end.isoformat(),
    #         "detail": detail,
    #     }
    #     headers = {
    #         "Accept": "application/json",
    #         "Content-Type": "application/json",
    #         "access-token": self.access_token,
    #     }
    #     self._logger.debug("post_gas_calendar: post", extra=data)

    #     response = requests.post(url=url, json=data, headers=headers, timeout=10)
    #     response_json = response.json()
    #     if isinstance(response_json, str):
    #         response_json = json.loads(response_json)
    #     self._logger.debug("post_gas_calendar: response", extra=response_json)
    #     return "status" in response_json and response_json["status"] == "success"


# def dump_yaml(value: dict) -> str:
#     return yaml.dump(value, allow_unicode=True)


if __name__ == "__main__":
    # python -m notion_api.external_calendar.infrastructure.google_calendar_api

    suite = GoogleCalendarApi()
    print(suite.fetch(date.today()))
