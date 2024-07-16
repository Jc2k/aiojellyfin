"""Builder pattern for building Jellyfin API queries."""

import copy
from collections.abc import AsyncGenerator
from typing import Generic, Self, TypeVar

from mashumaro.codecs.basic import BasicDecoder

from aiojellyfin import Connection, MediaItem, MediaItems

MediaItemT = TypeVar("MediaItemT", bound=MediaItem)


class ItemQueryBuilder(Generic[MediaItemT]):
    _params: dict[str, str]
    _decoder: BasicDecoder[MediaItems[MediaItemT]]

    def __init__(self, cls: MediaItemT, client: Connection):
        self._decoder = BasicDecoder(cls)
        self._client = client
        self._params = {}

    def _clone(self) -> Self:
        return copy.deepcopy(self)

    def parent(self, parent_id: str) -> Self:
        result = self._clone()
        result._params["searchTerm"] = parent_id
        return result

    def enable_userdata(self) -> Self:
        result = self._clone()
        result._params["enableUserData"] = "true"
        return result

    def fields(self, fields: list[str]) -> Self:
        result = self._clone()
        result._params["fields"] = ",".join(fields)
        return result

    def start_index(self, start_index: int) -> Self:
        result = self._clone()
        result._params["startIndex"] = str(start_index)
        return result

    def limit(self, limit: int) -> Self:
        result = self._clone()
        result._params["limit"] = str(limit)
        return result

    def to_params(self) -> dict[str, str]:
        return copy.deepcopy(self._params)

    async def request(self) -> MediaItems[MediaItemT]:
        response = await self._client._get_json("/Items", params=self.to_params())
        return self._decoder.decode(response)

    async def stream(self, page_size: int = 100) -> AsyncGenerator[MediaItemT, None]:
        request = self.limit(page_size)
        response = await request.request()
        for obj in response["Items"]:
            yield obj

        offset = page_size

        while offset < response["TotalRecordCount"]:
            response = await request.start_index(offset).request()
            for obj in response["Items"]:
                yield obj
            offset += page_size
