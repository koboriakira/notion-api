from dataclasses import dataclass

from notion_client_wrapper.base_page import BasePage


@dataclass
class AccountBook(BasePage):
    """家計簿クラス"""
