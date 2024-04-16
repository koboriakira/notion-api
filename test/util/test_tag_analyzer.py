import json
from unittest import TestCase

import pytest
from notion_api.util.tag_analyzer import TagAnalyzer, analyze_tags


def test_analyze_tags():
    input = {"tags": "test1, test2, test3, test1"}

    actual = analyze_tags(args=json.dumps(input))
    assert len(actual) == 3
    assert "test1" in actual
    assert "test2" in actual
    assert "test3" in actual


class TestTagAnalyzer(TestCase):
    @pytest.mark.skip(reason="実際にOpenAIを実行してコストがかかるためスキップ。")
    def test_analyze_tags_actually(self):
        suite = TagAnalyzer()

        actual = suite.handle(
            "団体を引っ張る準備、できてます。練習量に裏付けされた確固たる自信!! デビュー前から続く現王者との歴史を振り返る。3.31両国国技館で王者・山下実優に挑む渡辺未詩にインタビュー"
        )
        self.assertTrue(len(actual) > 0)
