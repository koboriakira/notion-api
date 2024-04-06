from dataclasses import dataclass
from enum import Enum

from notion_client_wrapper.filter.condition.or_condition import OrCondition
from notion_client_wrapper.properties.relation import Relation

from .condition import Condition


class RelationConditionType(Enum):
    CONTAINS = "contains"


@dataclass(frozen=True)
class RelationCondition(Condition):
    property_name: str
    property_type: str
    value: str
    condition_type: RelationConditionType

    @classmethod
    def contains(cls: "RelationCondition", relation: Relation) -> OrCondition:
        id_list = relation.id_list
        relation_condition_list = [
            RelationCondition(
                property_name=relation.name,
                property_type=relation.type,
                value=id_,
                condition_type=RelationConditionType.CONTAINS,
            )
            for id_ in id_list
        ]
        return OrCondition(relation_condition_list)

    def __dict__(self) -> dict:
        return {
            "property": self.property_name,
            self.property_type: {
                self.condition_type.value: self.value,
            },
        }
