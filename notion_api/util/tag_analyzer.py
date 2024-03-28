import logging

from util.openai_executer import OpenaiExecuter


def analyze_tags(args: dict) -> list[str]:
    if "tags" not in args:
        return []
    tags: str = args["tags"]
    if tags is None:
        return []
    return [tag.strip() for tag in tags.split(",")]

class TagAnalyzer:
    def __init__(
            self,
            client: OpenaiExecuter | None = None,
            logger: logging.Logger | None = None,
            is_debug: bool|None = None) -> None:
        self.client = client or OpenaiExecuter(model="gpt-3.5-turbo-1106", logger=logger)
        self.logger = logger or logging.getLogger(__name__)
        self.is_debug = is_debug or False

    def handle(self, text: str) -> list[str]:
        if self.is_debug:
            return ["テスト"]
        user_content = f"次の文章を解析して、タグをつけてください。タグはたとえば人名や作品名、カテゴリ、特定の重要なキーワードのようなものを指します。\n\n{text}"
        analyze_tags_parameters = {
            "type": "object",
            "properties": {
                "tags": {
                    "type": "string",
                    "description": "タグのリスト。カンマ区切りで複数指定可能\n例) 文章術, プロレス, 資産運用",
                },
            },
            "required": ["tags"],
        }
        tags:list[str] = self.client.simple_function_calling(
            user_content=user_content,
            func=analyze_tags,
            func_description="タグをつける",
            parameters=analyze_tags_parameters,
        )
        return tags

if __name__ == "__main__":
    # python -m notion_api.util.tag_analyzer
    logging.basicConfig(level=logging.DEBUG)
    tag_analyzer = TagAnalyzer()
    print(tag_analyzer.handle("団体を引っ張る準備、できてます。練習量に裏付けされた確固たる自信!! デビュー前から続く現王者との歴史を振り返る。3.31両国国技館で王者・山下実優に挑む渡辺未詩にインタビュー"))
