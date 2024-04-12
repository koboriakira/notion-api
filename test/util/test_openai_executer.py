from unittest import TestCase

import pytest

from util.openai_executer import OpenaiExecuter


class TestOpenaiExecuter(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    @pytest.mark.skip("実際にOpenAIを実行してコストがかかるためスキップ。")
    def test_json_format形式のチャット(self):
        # pipenv run pytest test/util/test_openai_executer.py -k test_json_format形式のチャット
        suite = OpenaiExecuter()

        # Given
        system_prompt = """次の食材・工程で料理したときの、1人前に相当する量のPFC(protein, fat, carbohydrate)を計算してください。回答はJSON形式で、以下のフィールドを持ちます。
・protein: 1人前の量にふくまれるタンパク質。グラム単位の整数値
・fat: 1人前の量にふくまれる脂質。グラム単位の整数値
・carbohydrate: 1人前の量にふくまれる炭水化物。グラム単位の整数値
・description: どのように計算したかの説明。とくに全量のPFCがいくつかと、全量が何人前に相当すると推測したかを明記してください"""

        user_content = """【食材】
'鶏むね肉: 350g', 'キャベツ: 300g', 'にんにく: 10g', '水: 450cc', '酒: 大さじ3', '鶏ガラスープ: 小さじ1と1／2', 'ほんだし: 小さじ1／2', '塩: 小さじ1／3', '砂糖: 小さじ1', 'オイスターソース: 小さじ1', '黒コショウ: 適量'

【工程】
に鶏むね肉350g、キャベツ300g、にんにく10g水450cc、酒大さじ3、鶏ガラスープ小さじ1半、ほんだし小さじ1/2、塩小さじ1/3、砂糖小さじ1、オイスターソース小さじ1入れ沸かし蓋をし1時間煮込み、鶏むね肉を崩して黒胡椒"""

        # When
        actual = suite.simple_json_chat(system_prompt=system_prompt, user_content=user_content)

        # Then
        print(actual)
        self.fail("確認のためかならず失敗する")
