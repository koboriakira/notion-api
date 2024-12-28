from logging import Logger, getLogger

from lotion import Lotion
from slack_sdk import WebClient

from common.value.slack_channel_type import ChannelType
from recipe.domain.recipe import MealKind, Recipe, RecipeKind
from recipe.domain.recipe_builder import RecipeBuilder
from recipe.domain.recipe_kind import RecipeKindType
from recipe.service.recipe_creator import AnalyzeResult, MockRecipeCreator, RecipeCreator
from util.openai_executer import OpenaiExecuter


class AddRecipeUseCase:
    def __init__(
        self,
        recipe_creator: RecipeCreator,
        slack_client: WebClient,
        logger: Logger | None = None,
        lotion: Lotion | None = None,
    ) -> None:
        self._recipe_creator = recipe_creator
        self._slack_client = slack_client
        self._logger = logger or getLogger(__name__)
        self._lotion = lotion or Lotion.get_instance()

    def execute(
        self,
        description: str,
        reference_url: str | None,
        slack_channel: str | None = None,
        slack_thread_ts: str | None = None,
    ) -> Recipe:
        self._logger.info("レシピを追加します")
        # レシピを分析
        analyze_result = self._recipe_creator.execute(description=description)
        pfc_dict = self._recipe_creator.calculate_pfc(
            ingredients=analyze_result.ingredients,
            process=analyze_result.process,
        )

        # ページインスタンスを生成、保存
        recipe = self._generate_recipe(analyze_result=analyze_result, reference_url=reference_url, pfc_dict=pfc_dict)
        recipe = self._lotion.update(recipe)

        # Slackに通知
        self._slack_client.chat_postMessage(
            channel=slack_channel or ChannelType.DIARY.value,
            text=f"レシピを登録しました!\n{recipe.title_for_slack()}",
            thread_ts=slack_thread_ts,
        )

        return recipe

    def _generate_recipe(self, analyze_result: AnalyzeResult, reference_url: str | None, pfc_dict: dict) -> Recipe:
        recipe_kind = self._lotion.fetch_select(Recipe, RecipeKind, value=RecipeKindType.AUTO.value)
        meal_kind = self._lotion.fetch_multi_select(
            Recipe,
            MealKind,
            value=[k.value for k in analyze_result.kind.values],
        )
        builder = (
            RecipeBuilder.of(title=analyze_result.title)
            .add_recipe_kind(recipe_kind)
            .add_meal_kind(meal_kind)
            .add_bulletlist_block(heading="材料", texts=analyze_result.ingredients)
            .add_bulletlist_block(heading="工程", texts=analyze_result.process)
        )
        if reference_url is not None:
            builder = builder.add_reference_url(url=reference_url)
        if (
            pfc_dict.get("protein") is not None
            and pfc_dict.get("fat") is not None
            and pfc_dict.get("carbohydrate") is not None
        ):
            builder = builder.add_pfc(
                protein=int(pfc_dict["protein"]),
                fat=int(pfc_dict["fat"]),
                carbohydrate=int(pfc_dict["carbohydrate"]),
            )
        if pfc_dict.get("description") is not None:
            builder = builder.add_bulletlist_block(heading="栄養素計算の背景", texts=[pfc_dict["description"]])

        return builder.build()


if __name__ == "__main__":
    # python -m notion_api.usecase.recipe.add_recipe_use_case
    import logging
    import os

    from slack_sdk import WebClient

    from recipe.service.recipe_creator import RecipeCreator

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    openai_executer = OpenaiExecuter(logger=logger)
    # recipe_creator = RecipeCreator(openai_executer=openai_executer, logger=logger)
    slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    usecase = AddRecipeUseCase(
        recipe_creator=MockRecipeCreator(),
        slack_client=slack_client,
        logger=logger,
    )
    usecase.execute(
        reference_url="https://www.youtube.com/watch?v=_-pW7D3a8Ps",
        description="""【鶏むね肉とキャベツのとろ煮込み】
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

鍋に鶏むね肉350g、キャベツ300g、にんにく10g水450cc、酒大さじ3、鶏ガラスープ小さじ1半、ほんだし小さじ1/2、塩小さじ1/3、砂糖小さじ1、オイスターソース小さじ1入れ沸かし蓋をし1時間煮込み、鶏むね肉を崩して黒胡椒""",
    )
