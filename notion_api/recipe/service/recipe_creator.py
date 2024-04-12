import json
from dataclasses import dataclass
from logging import Logger, getLogger

from recipe.domain.meal_kind import MealKindType, MealKindTypes
from util.openai_executer import OpenaiExecuter


class RecipeCreateError(Exception):
    @staticmethod
    def required(field: str) -> "RecipeCreateError":
        return RecipeCreateError(f"{field} is required")


@dataclass(frozen=True)
class AnalyzeResult:
    title: str
    kind: MealKindTypes
    ingredients: list[str]
    process: list[str]

    @staticmethod
    def func(args: dict) -> "AnalyzeResult":
        params: dict = json.loads(args)

        title: str = params.get("title")
        if title is None:
            raise RecipeCreateError.required(field="title")
        kind: str = params.get("kind")
        if kind is None:
            raise RecipeCreateError.required(field="kind")
        ingredients: str = params.get("ingredients")
        if ingredients is None:
            raise RecipeCreateError.required(field="ingredients")
        process: str = params.get("process")
        if process is None:
            raise RecipeCreateError.required(field="process")

        return AnalyzeResult(
            title=title,
            kind=MealKindTypes([MealKindType.from_text(k) for k in kind.split(",")]),
            ingredients=ingredients.split("\n"),
            process=process.split("\n"),
        )


class RecipeCreator:
    def __init__(self, openai_executer: OpenaiExecuter, logger: Logger | None = None) -> None:
        self._openai_executer = openai_executer
        self._logger = logger or getLogger(__name__)

    def execute(self, description: str) -> AnalyzeResult:
        user_content = f"次の文章を解析して、タイトル、レシピの種類、材料、工程を出力してください。\n\n{description}"
        kind_type_name_list = [m.value for m in MealKindType]
        analyze_recipe_parameters = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "レシピのタイトル",
                },
                "kind": {
                    "type": "string",
                    "description": f"レシピの種類。以下のいずれかを指定。{','.join(kind_type_name_list)}。カンマ区切りで複数指定可能",
                },
                "ingredients": {
                    "type": "string",
                    "description": "食材とその量をあらわす。リスト形式で改行で区切る。\n例)\nじゃがいも: 2個\nにんじん: 1本",
                },
                "process": {
                    "type": "string",
                    "description": "工程をあらわす。リスト形式で改行で区切る。1行には50文字以内で記述すること。\n例)\nじゃがいもを洗って皮をむく\nにんじんを輪切りにする",
                },
            },
            "required": ["title", "kind", "ingredients", "process"],
        }
        result: AnalyzeResult = self._openai_executer.simple_function_calling(
            user_content=user_content,
            func=AnalyzeResult.func,
            func_description="レシピを分析する",
            parameters=analyze_recipe_parameters,
        )
        return result


class MockRecipeCreator(RecipeCreator):
    def __init__(self) -> None:
        pass

    def execute(self, description: str) -> AnalyzeResult:  # noqa: ARG002
        return AnalyzeResult(
            title="鶏むね肉とキャベツのとろ煮込み",
            kind=MealKindTypes(values=[MealKindType.SIDE_DISH]),
            ingredients=[
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
            process=[
                "鍋に鶏むね肉350g、キャベツ300g、にんにく10g水450cc、酒大さじ3、鶏ガラスープ小さじ1半、ほんだし小さじ1/2、塩小さじ1/3、砂糖小さじ1、オイスターソース小さじ1入れ沸かし蓋をし1時間煮込み、鶏むね肉を崩して黒胡椒",
            ],
        )
