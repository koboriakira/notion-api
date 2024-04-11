from unittest import TestCase

from notion_api.util.datetime import jst_today
from notion_api.util.weather.weather_fetcher import WeatherFetcher


class TestWeatherFetcher(TestCase):
    def setUp(self) -> None:
        self.suite = WeatherFetcher()
        return super().setUp()

    def test_今日の天気を取得する(self):
        # When
        actual = self.suite.fetch_today_weather()

        # Then
        print(actual.date)
        print(actual.telop)
        print(actual.detail)
        print(actual.tempature)
        print(actual.chancre_of_rain)
        print(actual.icon_svg_url)
        self.assertEqual(jst_today(), actual.date)
