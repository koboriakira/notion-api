from dataclasses import dataclass
from datetime import date

import requests

from util.dataclass.type_safe_object import TypeSafeFrozenObject
from util.datetime import jst_today


@dataclass(frozen=True)
class Detail(TypeSafeFrozenObject):
    weather: str
    wind: str
    wave: str


@dataclass(frozen=True)
class Tempature(TypeSafeFrozenObject):
    min_cecius: int
    max_cecius: int


@dataclass(frozen=True)
class ChanceOfRain(TypeSafeFrozenObject):
    morning: int
    afternoon: int
    evening: int
    late_night: int


@dataclass(frozen=True)
class WeatherFetchResult(TypeSafeFrozenObject):
    date: date
    telop: str  # 概要
    detail: Detail  # 詳細
    tempature: Tempature  # 気温
    chancre_of_rain: ChanceOfRain  # 降水確率
    icon_svg_url: str  # 天気画像のURL


class WeatherFetcher:
    API_URL = "https://weather.tsukumijima.net/api/forecast/city/130010"

    def fetch_today_weather(self) -> WeatherFetchResult:
        return self.fetch_forecast(date_=jst_today())

    def fetch_forecast(self, date_: date) -> WeatherFetchResult:
        response = requests.get(self.API_URL, timeout=10)
        response.raise_for_status()
        forecasts = response.json()["forecasts"]
        for forecast in forecasts:
            if forecast["date"] == date_.isoformat():
                return self.__convert(forecast)
        msg = f"Forecast for {date_} is not found"
        raise ValueError(msg)

    def __convert(self, forecast: dict) -> WeatherFetchResult:
        detail = Detail(
            # \u3000 を半角スペースに変換する
            weather=forecast["detail"]["weather"].replace("\u3000", " "),
            wind=forecast["detail"]["wind"],
            wave=forecast["detail"]["wave"],
        )
        tempature = Tempature(
            min_cecius=int(forecast["temperature"]["min"]["celsius"]),
            max_cecius=int(forecast["temperature"]["max"]["celsius"]),
        )
        chancre_of_rain = ChanceOfRain(
            # "%"を削除してintに変換する
            morning=int(forecast["chanceOfRain"]["T06_12"].replace("%", "")),
            afternoon=int(forecast["chanceOfRain"]["T12_18"].replace("%", "")),
            evening=int(forecast["chanceOfRain"]["T18_24"].replace("%", "")),
            late_night=int(forecast["chanceOfRain"]["T00_06"].replace("%", "")),
        )
        return WeatherFetchResult(
            date=date.fromisoformat(forecast["date"]),
            telop=forecast["telop"],
            detail=detail,
            tempature=tempature,
            chancre_of_rain=chancre_of_rain,
            icon_svg_url=forecast["image"]["url"],
        )
