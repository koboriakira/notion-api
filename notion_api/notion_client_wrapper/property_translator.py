from typing import Any

from lotion.properties import Button
from lotion.properties import Checkbox
from lotion.properties import CreatedTime
from lotion.properties import Date
from lotion.properties import LastEditedTime
from lotion.properties import MultiSelect
from lotion.properties import Number
from lotion.properties import Properties
from lotion.properties import Property
from lotion.properties import Relation
from lotion.properties import Rollup
from lotion.properties import Select
from lotion.properties import Status
from lotion.properties import Text
from lotion.properties import Title
from lotion.properties import Url


class PropertyTranslator:
    @classmethod
    def from_dict(cls: "PropertyTranslator", properties: dict[str, dict]) -> Properties:
        values = []
        for key, value in properties.items():
            values.append(cls.from_property_dict(key, value))
        return Properties(values=[value for value in values if value is not None])

    @classmethod
    def from_property_dict(cls: "PropertyTranslator", key: str, property_: dict[str, Any]) -> "Property":  # noqa: PLR0911
        type_ = property_["type"]
        match type_:
            case "title":
                return Title.from_property(key, property_)
            case "rich_text":
                return Text.from_dict(key, property_)
            case "multi_select":
                return MultiSelect.of(key, property_)
            case "select":
                return Select.of(key, property_)
            case "number":
                return Number.of(key, property_)
            case "checkbox":
                return Checkbox.of(key, property_)
            case "date":
                return Date.of(key, property_)
            case "status":
                return Status.of(key, property_)
            case "url":
                return Url.of(key, property_)
            case "relation":
                return Relation.of(key, property_)
            case "last_edited_time":
                return LastEditedTime.create(property_["last_edited_time"])
            case "created_time":
                return CreatedTime.create(property_["created_time"])
            case "rollup":
                return Rollup.of(key, property_)
            case "button":
                return Button.of(key, property_)
            case _:
                msg = f"Unsupported property type: {type_} {property_}"
                raise Exception(msg)
