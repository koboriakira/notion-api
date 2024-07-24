import json
import logging

from util.openai_executer import OpenaiExecuter


def prittier(tags: list[str]) -> list[str]:
    # 先頭・末尾の空白を削除
    tags = [tag.strip() for tag in tags]
    # 重複を削除
    tags = list(set(tags))
    # Noneと空文字を削除
    return [tag for tag in tags if tag is not None and tag != ""]


def analyze_tags(args: str) -> list[str]:
    json_dict = json.loads(args)
    if "tags" not in json_dict or json_dict["tags"] is None:
        return []
    tags_str: str = json_dict["tags"]
    return prittier(tags_str.split(","))


class TagAnalyzer:
    def __init__(
        self,
        client: OpenaiExecuter | None = None,
        logger: logging.Logger | None = None,
        is_debug: bool | None = None,
    ) -> None:
        self.client = client or OpenaiExecuter(logger=logger)
        self.logger = logger or logging.getLogger(__name__)
        self.is_debug = is_debug or False

    def handle(self, text: str) -> list[str]:
        assert isinstance(text, str)
        if self.is_debug:
            return ["テスト"]
        user_content = f"次の文章を解析して、タグをつけてください。タグはたとえば人名や作品名、サービス名、具体的なキーワード、抽象化されたカテゴリ名のようなものを指します。\n\n{text}"
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
        tags: list[str] = self.client.simple_function_calling(
            user_content=user_content,
            func=analyze_tags,
            func_description="タグをつける",
            parameters=analyze_tags_parameters,
        )
        return tags
