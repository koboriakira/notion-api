import json
from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

import pytest

from notion_databases.recipe_prop.meal_kind import MealKindType, MealKindTypes
from recipe.recipe_creator import AnalyzeResult, RecipeCreator
from util.openai_executer import OpenaiExecuter


class TestRecipeCreator(TestCase):
    @pytest.mark.skip(reason="実際にOpenAIを実行してコストがかかるためスキップ。")
    def test_分析する(self):
        # pipenv run pytest test/recipe/service/test_recipe_creator.py -k test_分析する
        suite = RecipeCreator(openai_executer=OpenaiExecuter(), logger=Mock(spec=Logger))

        # Given
        description = """【鶏むね肉とキャベツのとろ煮込み】
鶏むね肉…350g
キャベツ…300g
にんにく…10g
水…450cc
酒…大さじ3
鶏ガラスープ…小さじ1と1／2
ほんだし…小さじ1／2
塩…小さじ1／3
砂糖…小さじ1
オイスターソース…小さじ1
黒コショウ…適量

鍋に鶏むね肉350g、キャベツ300g、にんにく10g水450cc、酒大さじ3、鶏ガラスープ小さじ1半、ほんだし小さじ1/2、塩小さじ1/3、砂糖小さじ1、オイスターソース小さじ1入れ沸かし蓋をし1時間煮込み、鶏むね肉を崩して黒胡椒"""

        # When
        actual = suite.execute(description=description)

        # Then
        print(actual)
        self.fail("標準出力確認のため失敗とする")

    def test_analyze_resultの変換(self):
        # Given
        input = {
            "title": "鶏むね肉とキャベツのとろ煮込み",
            "kind": "主菜",
            "ingredients": "鶏むね肉: 350g\nキャベツ: 300g\nにんにく: 10g\n水: 450cc\n酒: 大さじ3\n鶏ガラスープ: 小さじ1と1／2\nほんだし: 小さじ1／2\n塩: 小さじ1／3\n砂糖: 小さじ1\nオイスターソース: 小さじ1\n黒コショウ: 適量",
            "process": "鍋に鶏むね肉350g、キャベツ300g、にんにく10g水450cc、酒大さじ3、鶏ガラスープ小さじ1半、ほんだし小さじ1/2、塩小さじ1/3、砂糖小さじ1、オイスターソース小さじ1入れ沸かし蓋をし1時間煮込み、鶏むね肉を崩して黒胡椒",
        }

        # When
        actual = AnalyzeResult.func(json.dumps(input))

        # Then
        self.assertEqual(actual.title, "鶏むね肉とキャベツのとろ煮込み")
        self.assertEqual(actual.kind, MealKindTypes(values=[MealKindType.MAIN_DISH]))
        self.assertEqual(
            actual.ingredients,
            [
                "鶏むね肉: 350g",
                "キャベツ: 300g",
                "にんにく: 10g",
                "水: 450cc",
                "酒: 大さじ3",
                "鶏ガラスープ: 小さじ1と1／2",
                "ほんだし: 小さじ1／2",
                "塩: 小さじ1／3",
                "砂糖: 小さじ1",
                "オイスターソース: 小さじ1",
                "黒コショウ: 適量",
            ],
        )
        self.assertEqual(
            actual.process,
            [
                "鍋に鶏むね肉350g、キャベツ300g、にんにく10g水450cc、酒大さじ3、鶏ガラスープ小さじ1半、ほんだし小さじ1/2、塩小さじ1/3、砂糖小さじ1、オイスターソース小さじ1入れ沸かし蓋をし1時間煮込み、鶏むね肉を崩して黒胡椒"
            ],
        )
