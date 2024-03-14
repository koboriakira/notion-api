from dataclasses import dataclass

from notion_client_wrapper.properties.property import Property


@dataclass
class Title(Property):
    text: str
    value: list[dict]
    type: str = "title"
    mentioned_page_id: str | None = None

    def __init__(self, name: str, id: str | None = None, value: list[dict] = [], text: str | None = None, mentioned_page_id: str | None = None):
        self.name = name
        self.id = id
        self.value = value
        self.text = text
        self.mentioned_page_id = mentioned_page_id

    @classmethod
    def from_properties(cls, properties: dict) -> "Title":
        if "Name" in properties:
            return cls.__of("Name", properties["Name"])
        if "Title" in properties:
            return cls.__of("Title", properties["Title"])
        if "名前" in properties:
            return cls.__of("名前", properties["名前"])
        raise Exception(f"Title property not found. properties: {properties}")

    @classmethod
    def from_property(cls, key:str, property: dict) -> "Title":
        return cls.__of(key, property)

    def __dict__(self):
        values = []
        values.append({
            "type": "text",
            "text": {
                "content": self.text,
            },
        })
        if self.mentioned_page_id is not None:
            values.append({
                "type": "mention",
                "mention": {
                    "type": "page",
                    "page": {
                        "id": self.mentioned_page_id,
                    },
                },
                # "plain_text": self.text,
                # "href": f"https://www.notion.so/{self.mentioned_page_id}"
            })
        result = {
            "title": values,
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }

    @staticmethod
    def __of(name: str, param: dict) -> "Title":
        return Title(
            name=name,
            id=param["id"],
            value=param["title"],
            text="".join([item["plain_text"] for item in param["title"]]),
        )

    @ staticmethod
    def from_plain_text(name: str, text: str) -> "Title":
        return Title(
            name=name,
            text=text,
        )

    @ staticmethod
    def from_mentioned_page_id(name: str, page_id: str) -> "Title":
        return Title(
            name=name,
            text="",
            mentioned_page_id=page_id,
        )

    def value_for_filter(self) -> str:
        raise NotImplementedError
