from abc import ABCMeta, abstractmethod


class RichTextElement(metaclass=ABCMeta):
    annotations: dict[str, bool] | None
    plain_text: dict[str, bool] | None
    href: dict[str, bool] | None

    def __init__(
            self,
            annotations: dict[str, bool] | None = None,
            plain_text: dict[str, bool] | None = None,
            href: dict[str, bool] | None = None) -> None:
        self.annotations = annotations
        self.plain_text = plain_text
        self.href = href

    def to_dict(self) -> dict:
        result = {
            "type": self.get_type(),
        }
        if self.annotations is not None:
            result["annotations"] = self.annotations
        if self.plain_text is not None:
            result["plain_text"] = self.plain_text
        if self.href is not None:
            result["href"] = self.href
        result[self.get_type()] = self.to_dict_sub()
        return result

    @staticmethod
    def from_entity(rich_text_element: dict) -> "RichTextElement":
        """ dictからRichTextElementを生成する """
        type = rich_text_element["type"]
        if type == "text":
            text = rich_text_element["text"]
            return RichTextTextElement(
                content=text["content"],
                link_url=text["link"]["url"] if text.get("link") else None,
                annotations=rich_text_element["annotations"],
                plain_text=rich_text_element["plain_text"],
                href=rich_text_element["href"],
            )
        if type == "mention":
            mention = rich_text_element["mention"]
            mention_type = mention["type"]
            if mention_type in ["database", "page"]:
                return RichTextMentionElement(
                    mention_type=mention_type,
                    object_id=mention[mention_type]["id"],
                    annotations=rich_text_element["annotations"],
                    plain_text=rich_text_element["plain_text"],
                    href=rich_text_element["href"],
                )
            if mention_type == "date":
                return RichTextMentionElement(
                    mention_type=mention_type,
                    start_date=mention["date"]["start"],
                    end_date=mention["date"]["end"],
                    annotations=rich_text_element["annotations"],
                    plain_text=rich_text_element["plain_text"],
                    href=rich_text_element["href"],
                )
            if mention_type == "link_preview":
                return RichTextMentionElement(
                    mention_type=mention_type,
                    link_preview_url=mention["link_preview"]["url"],
                    annotations=rich_text_element["annotations"],
                    plain_text=rich_text_element["plain_text"],
                    href=rich_text_element["href"],
                )
            raise Exception("invalid mention type")
        if type == "equation":
            raise NotImplementedError("equation is not implemented yet")
        raise Exception("invalid type")

    @staticmethod
    def from_plain_text(text: str) -> "RichTextElement":
        """ plain_textからRichTextElementを生成する """
        return RichTextTextElement.of(content=text)

    def to_plain_text(self) -> str:
        """ plain_textに変換する """
        if isinstance(self, RichTextTextElement):
            return self.content
        raise NotImplementedError("not implemented yet")

    @ abstractmethod
    def get_type(self) -> str:
        """ text, mention, equationのどれかを返す """

    @ abstractmethod
    def to_dict_sub(self) -> str:
        """ Text, Mention, Equationのそれぞれで実装する """


class RichTextTextElement(RichTextElement):
    content: str
    link_url: str | None = None

    def __init__(
            self,
            content: str,
            link_url: str | None = None,
            annotations: dict[str, bool] | None = None,
            plain_text: dict[str, bool] | None = None,
            href: dict[str, bool] | None = None) -> None:
        self.content = content
        self.link_url = link_url
        super().__init__(annotations, plain_text, href)

    @ staticmethod
    def of(content: str, link_url: str | None = None) -> "RichTextTextElement":
        return RichTextTextElement(
            content=content,
            link_url=link_url,
        )

    def get_type(self) -> str:
        return "text"

    def to_dict_sub(self) -> str:
        result = {
            "content": self.content,
        }
        if self.link_url is not None:
            result["link"] = {
                "url": self.link_url,
            }
        return result


class RichTextMentionElement(RichTextElement):
    # TODO: 日付やリンクプレビューなどもあるみたい
    # refs: https://developers.notion.com/reference/rich-text#mention
    mention_type: str  # database, page, date, link_preview
    object_id: str | None  # database,pageのどちらかで利用。database_idまたはpage_id
    start_date: str | None = None  # dateのみ利用
    end_date: str | None = None  # dateのみ利用
    link_preview_url: str | None = None  # link_previewのみ利用

    def __init__(self,  # noqa: PLR0913
                 mention_type: str,
                 object_id: str | None = None,
                 start_date: str | None = None,
                 end_date: str | None = None,
                 link_preview_url: str | None = None,
                 annotations: dict[str, bool] | None = None,
                 plain_text: dict[str, bool] | None = None,
                 href: dict[str, bool] | None = None) -> None:
        self.mention_type = mention_type
        self.object_id = object_id
        self.start_date = start_date
        self.end_date = end_date
        self.link_preview_url = link_preview_url
        super().__init__(annotations, plain_text, href)

    @ staticmethod
    def of_database(database_id: str) -> "RichTextMentionElement":
        return RichTextMentionElement(
            mention_type="database",
            object_id=database_id,
        )

    @ staticmethod
    def of_page(page_id: str) -> "RichTextMentionElement":
        return RichTextMentionElement(
            mention_type="page",
            object_id=page_id,
        )

    def get_type(self) -> str:
        return "mention"

    def to_dict_sub(self) -> str:
        """ Text, Mention, Equationのそれぞれで実装する """
        result = {
            "type": self.mention_type,
        }
        if self.mention_type in ["database", "page"]:
            result[self.mention_type] = {
                "id": self.object_id,
            }

        return result


class RichTextEquationElement(RichTextElement):
    # TODO: not implemented yet
    pass
