from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.box_bulk_get_response import BoxBulkGetResponse
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    plate_ids: Optional[List[str]] = None,
    barcodes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    url = "{}/plates:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    if plate_ids is None:
        json_plate_ids = None
    else:
        json_plate_ids = plate_ids

    if barcodes is None:
        json_barcodes = None
    else:
        json_barcodes = barcodes

    params: Dict[str, Any] = {}
    if plate_ids is not None:
        params["plateIds"] = json_plate_ids
    if barcodes is not None:
        params["barcodes"] = json_barcodes

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BoxBulkGetResponse, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        return BoxBulkGetResponse.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BoxBulkGetResponse, BadRequestError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    plate_ids: Optional[List[str]] = None,
    barcodes: Optional[List[str]] = None,
) -> Response[Union[BoxBulkGetResponse, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        plate_ids=plate_ids,
        barcodes=barcodes,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    plate_ids: Optional[List[str]] = None,
    barcodes: Optional[List[str]] = None,
) -> Optional[Union[BoxBulkGetResponse, BadRequestError, NotFoundError]]:
    """ BulkGet plates """

    return sync_detailed(
        client=client,
        plate_ids=plate_ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    plate_ids: Optional[List[str]] = None,
    barcodes: Optional[List[str]] = None,
) -> Response[Union[BoxBulkGetResponse, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        plate_ids=plate_ids,
        barcodes=barcodes,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    plate_ids: Optional[List[str]] = None,
    barcodes: Optional[List[str]] = None,
) -> Optional[Union[BoxBulkGetResponse, BadRequestError, NotFoundError]]:
    """ BulkGet plates """

    return (
        await asyncio_detailed(
            client=client,
            plate_ids=plate_ids,
            barcodes=barcodes,
        )
    ).parsed
