from typing import Any, Dict, List

import attr

from ..models.request_fulfillment import RequestFulfillment


@attr.s(auto_attribs=True)
class RequstFulfillmentsEnvelope:
    """ An object containing an array of RequestFulfillments """

    request_fulfillments: List[RequestFulfillment]

    def to_dict(self) -> Dict[str, Any]:
        request_fulfillments = []
        for request_fulfillments_item_data in self.request_fulfillments:
            request_fulfillments_item = request_fulfillments_item_data.to_dict()

            request_fulfillments.append(request_fulfillments_item)

        return {
            "requestFulfillments": request_fulfillments,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequstFulfillmentsEnvelope":
        request_fulfillments = []
        for request_fulfillments_item_data in d["requestFulfillments"]:
            request_fulfillments_item = RequestFulfillment.from_dict(request_fulfillments_item_data)

            request_fulfillments.append(request_fulfillments_item)

        return RequstFulfillmentsEnvelope(
            request_fulfillments=request_fulfillments,
        )
