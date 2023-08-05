from typing import Any, Dict, List

import attr

from ..models.custom_entity_base_request import CustomEntityBaseRequest


@attr.s(auto_attribs=True)
class CustomEntityBulkUpdate:
    """  """

    custom_entities: List[CustomEntityBaseRequest]

    def to_dict(self) -> Dict[str, Any]:
        custom_entities = []
        for custom_entities_item_data in self.custom_entities:
            custom_entities_item = custom_entities_item_data.to_dict()

            custom_entities.append(custom_entities_item)

        return {
            "customEntities": custom_entities,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityBulkUpdate":
        custom_entities = []
        for custom_entities_item_data in d["customEntities"]:
            custom_entities_item = CustomEntityBaseRequest.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        return CustomEntityBulkUpdate(
            custom_entities=custom_entities,
        )
