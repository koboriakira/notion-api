from datetime import datetime
from unittest import TestCase

import pytest
from notion_api.book.domain.book import Book
from notion_api.common.value.database_type import DatabaseType
from notion_api.notion_client_wrapper.base_page import BasePage
from notion_api.notion_client_wrapper.client_wrapper import Lotion
from notion_api.notion_client_wrapper.filter.condition.date_condition import DateCondition
from notion_api.notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_api.notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_api.notion_client_wrapper.properties.cover import Cover
from notion_api.notion_client_wrapper.properties.last_edited_time import LastEditedTime
from notion_api.notion_client_wrapper.properties.title import Title
from notion_api.notion_client_wrapper.properties.url import Url
from notion_api.task.domain.task import ToDoTask
from notion_api.util.datetime import JST

from daily_log.domain.daily_log import DailyLog


class TestLotion(TestCase):
    def setUp(self):
        self.suite = Lotion.get_instance()

    @pytest.mark.skip()
    def test_ページを取得してみる(self):
        # pipenv run pytest test/notion_client_wrapper/test_client_wrapper.py -k test_ページを取得してみる
        page_id = "5c38fd30714b4ce2bf2d25407f3cfc16"
        page_model = ToDoTask
        page = self.suite.retrieve_page(page_id=page_id, page_model=page_model)
        print(page)
        print(page.get_slack_text_in_block_children())
        self.fail("標準出力確認のためのエラー")

    @pytest.mark.use_genuine_api()
    def test_すべてのデータを取得できる(self):
        # 音楽のページを取得してみる
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.BOOK.value,
        )
        self.assertTrue(len(pages) > 0)

    @pytest.mark.use_genuine_api()
    def test_1つの条件で絞り込む(self):
        # Given
        url = Url.from_url(name="Spotify", url="https://open.spotify.com/track/6tPlPsvzSM74vRVn9O5v9K")
        filter_param = FilterBuilder().add_condition(StringCondition.equal(url)).build()

        # 音楽のページを取得してみる
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            filter_param=filter_param,
        )
        self.assertEqual(1, len(pages))
        self.assertEqual("タバコロード 20", pages[0].get_title().text)

    @pytest.mark.use_genuine_api()
    def test_タイトルを使って絞り込む_title引数(self):
        # Given
        title = "タバコロード 20"

        # 音楽のページを取得してみる
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            title=title,
        )
        self.assertEqual(1, len(pages))
        self.assertEqual("タバコロード 20", pages[0].get_title().text)

    @pytest.mark.use_genuine_api()
    def test_タイトルを使って絞り込む_titleをpropertyで(self):
        # Given
        title = Title.from_plain_text(name="名前", text="タバコロード 20")
        filter_param = FilterBuilder().add_condition(StringCondition.equal(title)).build()

        # 音楽のページを取得してみる
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            filter_param=filter_param,
        )
        self.assertEqual(1, len(pages))
        self.assertEqual("タバコロード 20", pages[0].get_title().text)

    @pytest.mark.use_genuine_api()
    def test_返却値のモデルを指定できるようにする(self):
        class OriginalBasePage(BasePage):
            pass

        # Given
        title = Title.from_plain_text(name="名前", text="タバコロード 20")
        filter_param = FilterBuilder().add_condition(StringCondition.equal(title)).build()

        # When: モデルを指定して取得
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.MUSIC.value, filter_param=filter_param, page_model=OriginalBasePage
        )
        self.assertIsInstance(pages[0], OriginalBasePage)

    @pytest.mark.use_genuine_api()
    def test_更新日時でしぼりこむ(self):
        class OriginalBasePage(BasePage):
            pass

        # Given
        date_property = LastEditedTime.create(value=datetime(2024, 3, 17, tzinfo=JST))
        date_property2 = LastEditedTime.create(value=datetime(2024, 3, 18, tzinfo=JST))
        filter_param = (
            FilterBuilder()
            .add_condition(DateCondition.on_or_after(date_property))
            .add_condition(DateCondition.on_or_before(date_property2))
            .build()
        )

        # When: モデルを指定して取得
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.WEBCLIP.value,
            filter_param=filter_param,
        )
        print(pages)
        print(len(pages))

    @pytest.mark.use_genuine_api()
    def test_ブロックもあわせてページをひとつ取得する(self):
        # pytest test/notion_client_wrapper/test_client_wrapper.py::TestLotion::test_ブロックもあわせてページをひとつ取得する

        # When
        task = self.suite.retrieve_page(
            page_id="21c664d6cc394d25accd77315c7a8a2e",
            page_model=DailyLog,
        )
        print(task)
        # self.fail()

    @pytest.mark.use_genuine_api()
    def test_現在のタスクを取得する(self):
        # pytest test/notion_client_wrapper/test_client_wrapper.py::TestLotion::test_現在のタスクを取得する
        from notion_api.task.domain.task import ToDoTask

        # Given
        filter_param = {
            "and": [
                {"property": "タスク種別", "select": {"does_not_equal": "ゴミ箱"}},
                {"property": "実施日", "date": {"equals": "2024-03-20"}},
                {
                    "or": [
                        {"property": "ステータス", "status": {"equals": "ToDo"}},
                        {"property": "ステータス", "status": {"equals": "InProgress"}},
                    ]
                },
            ]
        }
        # When
        pages = self.suite.retrieve_database(
            database_id=DatabaseType.TASK.value,
            filter_param=filter_param,
            page_model=ToDoTask,
        )
        print(pages)
        print(len(pages))
        # self.fail()

    @pytest.mark.skip()
    def test_select_kind_map(self):
        """Selectの選択肢を集めるためのテスト"""
        # pytest test/notion_client_wrapper/test_client_wrapper.py::TestLotion::test_select_kind_map
        target_database = DatabaseType.TASK_ROUTINE
        target_select_name = "周期"

        pages = self.suite.retrieve_database(
            database_id=target_database.value,
        )

        result = {}
        for page in pages:
            select_property = page.get_select(name=target_select_name)
            if select_property is None:
                continue
            if select_property.selected_id in result:
                continue
            result[select_property.selected_name] = {
                "selected_id": select_property.selected_id,
                "selected_color": select_property.selected_color,
            }
        # uniqueにする
        import json

        print(json.dumps(result, indent=2, ensure_ascii=False))

        # 内容を確認したいので、無理やりfailさせる
        self.fail("動作確認用。テストは失敗しても問題ありません。")

    @pytest.mark.skip()
    def test_multi_select_kind_map(self):
        """MultiSelectの選択肢を集めるためのテスト"""
        # pytest test/notion_client_wrapper/test_client_wrapper.py::TestLotion::test_multi_select_kind_map
        target_database = DatabaseType.RECIPE
        target_multi_select_name = "種類"

        pages = self.suite.retrieve_database(
            database_id=target_database.value,
        )

        result = []
        for page in pages:
            select_property = page.get_multi_select(name=target_multi_select_name)
            if select_property is None:
                continue
            values = select_property.values
            result.extend([{"name": value.name, "id": value.id} for value in values])
        # uniqueにする
        result = list({value["name"]: value for value in result}.values())
        import json

        print(json.dumps(result, ensure_ascii=False))

        # 内容を確認したいので、無理やりfailさせる
        self.fail("動作確認用。テストは失敗しても問題ありません。")

    @pytest.mark.skip("実際にページが作成されるので注意")
    def test_ページを作成してみる(self):
        # pytest test/notion_client_wrapper/test_client_wrapper.py::TestLotion::test_ページを作成してみる
        title = Title.from_plain_text(name="名前", text="テストページ")
        cover = Cover(type="external", external_url="https://i.ytimg.com/vi/82KT4FNyNdY/maxresdefault.jpg")
        page = self.suite.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            cover=cover,
            properties=[title],
        )
        print(page)

    @pytest.mark.use_genuine_api()
    def test_タイトルだけで検索する(self):
        # pytest test/notion_client_wrapper/test_client_wrapper.py::TestLotion::test_タイトルだけで検索する
        page = self.suite.find_page_by_title(
            database_id=DatabaseType.BOOK.value,
            title="ジェームズ・クリアー式 複利で伸びる1つの習慣",
            title_key_name="Title",
            page_model=Book,
        )
        self.assertIsNotNone(page)

    @pytest.mark.skip("実際にページが作成されるので注意")
    def test_ページを作成する(self):
        # pytest test/notion_client_wrapper/test_client_wrapper.py::TestLotion::test_ページを作成する
        title = Title.from_plain_text(name="名前", text="テストページ")
        page = self.suite.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=[title],
        )
        self.assertIsNotNone(page)
