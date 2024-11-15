from abc import ABCMeta, abstractmethod

from util.date_range import DateRange
from webclip.domain.webclip import Webclip


class WebclipRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_title(self, title: str) -> Webclip | None:
        """タイトルからWebclipを取得する

        Args:
            title (str): タイトル

        Returns:
            Webclip|None: Webclip
        """

    @abstractmethod
    def save(self, webclip: Webclip) -> Webclip:
        """Webclipを保存する

        Args:
            webclip (Webclip): Webclip

        Returns:
            Webclip: Webclip
        """

    @abstractmethod
    def search(self, date_range: DateRange) -> list[Webclip]:
        """指定された日付範囲内のWebclipを取得する

        Args:
            date_range (DateRange): 日付範囲

        Returns:
            list[Webclip]: Webclipリスト
        """
