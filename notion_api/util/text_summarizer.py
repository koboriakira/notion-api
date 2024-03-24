from logging import Logger, getLogger

from util.openai_executer import OpenaiExecuter

TEMPLATE = """「仕様」に則って「入力」に記載した文章の要約をしてください。

\"\"\"仕様
・最大文字数は500文字です
・指示に対する返答や補足など、文章の要約結果以外の出力は不要です

\"\"\"入力
{context}"""

class TextSummarizer:
    def __init__(
            self,
            client: OpenaiExecuter|None = None,
            logger: Logger|None = None,
            is_debug: bool|None = None) -> None:
        self._client = client or OpenaiExecuter()
        self._logger = logger or getLogger(__name__)
        self._is_debug = is_debug or False

    def handle(self, text: str) -> str:
        self._logger.debug("TextSummarizer: " + text)
        if self._is_debug:
            return "要約テスト"
        user_content = TEMPLATE.format(context=text)
        return self._client.simple_chat(user_content=user_content)

if __name__ == "__main__":
    # python -m notion_api.usecase.service.text_summarizer
    from injector.injector import Injector
    usecase = Injector.create_text_summarizer()
    text = """うまみや栄養がぎゅっと凝縮された「切り干し大根」。お醤油味の煮物もいいですが、サラダにしたりかき揚げにしたりと実は自由に楽しめる食材です。味付けもピリ辛やエスニック風味でパンチを効かせてお酒のよき相棒に！ 水でもどす工程なしのレシピなので、思い立ったらすぐ作れます。 """
    summary = usecase.handle(text)
    print(type(summary))
    print(summary)
