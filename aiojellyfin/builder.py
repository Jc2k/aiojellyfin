"""Builder pattern for building Jellyfin API queries."""

import copy
from collections.abc import AsyncGenerator
from typing import Generic, Self

from mashumaro.codecs.basic import BasicDecoder

from .const import ItemFields, ItemType
from .models import Album, Artist, MediaItems, MediaItemT, Playlist, Track
from .session import Session


class ItemQueryBuilder(Generic[MediaItemT]):
    """A query that can be performed against /Items or similar Jellyfin endpoint."""

    endpoint = "/Items"

    _params: dict[str, str]
    _decoder: BasicDecoder[MediaItems[MediaItemT]]

    def __init__(
        self,
        session: Session,
        decoder: BasicDecoder[MediaItems[MediaItemT]],
        params: dict[str, str],
    ):
        """Initialise the class."""
        self._decoder = decoder
        self._session = session
        self._params = params

    @classmethod
    def create(cls, session: Session) -> Self:
        """Create a new query builder instance."""
        decoder = BasicDecoder(MediaItems[MediaItemT])
        return cls(session, decoder, {})

    def _clone(self) -> Self:
        return self.__class__(
            self._session,
            self._decoder,
            copy.deepcopy(self._params),
        )

    def parent(self, parent_id: str) -> Self:
        """Specify this to localize the search to a specific item or folder.

        Omit to use the root.
        """
        result = self._clone()
        result._params["parentId"] = parent_id
        return result

    def search_term(self, search_term: str) -> Self:
        """Search for this term."""
        result = self._clone()
        result._params["searchTerm"] = search_term
        return result

    def include_item_types(self, *args: ItemType) -> Self:
        """Only include these item types."""
        result = self._clone()
        result._params["includeItemTypes"] = ",".join(arg.value for arg in args)
        return result

    def exclude_item_types(self, *args: ItemType) -> Self:
        """Exclude these item types."""
        result = self._clone()
        result._params["excludeItemTypes"] = ",".join(args)
        return result

    def recursive(self, recursive: bool) -> Self:
        """Search parent folder and all child folders."""
        result = self._clone()
        result._params["recursive"] = "true" if recursive else "false"
        return result

    def enable_userdata(self) -> Self:
        """Include per user metadata - does the logged in user like the content."""
        result = self._clone()
        result._params["enableUserData"] = "true"
        return result

    def fields(self, *args: ItemFields) -> Self:
        """Specify additional fields of information to return in the output."""
        result = self._clone()
        result._params["fields"] = ",".join(field.value for field in args)
        return result

    def start_index(self, start_index: int) -> Self:
        """Record index to start at.

        All items with a lower index will be dropped from the results.
        """
        result = self._clone()
        result._params["startIndex"] = str(start_index)
        return result

    def limit(self, limit: int) -> Self:
        """Maximum number of records to return."""
        result = self._clone()
        result._params["limit"] = str(limit)
        return result

    def to_params(self) -> dict[str, str]:
        """Build a dictionary of the query parameters for this search."""
        return copy.deepcopy(self._params)

    async def request(self) -> MediaItems[MediaItemT]:
        """Request a list of records matching this query."""
        response = await self._session.get_json(self.endpoint, params=self.to_params())
        return self._decoder.decode(response)

    async def stream(self, page_size: int = 100) -> AsyncGenerator[MediaItemT, None]:
        """Request all records matching this query, automatically paging."""
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


class ArtistQueryBuilder(ItemQueryBuilder[Artist]):
    """Builder for searching artist records."""

    endpoint = "/Artists"

    @classmethod
    def setup(cls, session: Session) -> Self:
        """Initialise the builder with default search restrictions for artists."""
        return super().create(session).recursive(True)


class AlbumQueryBuilder(ItemQueryBuilder[Album]):
    """Builder for searching album records."""

    @classmethod
    def setup(cls, session: Session) -> Self:
        """Initialise the builder with default search restrictions for albums."""
        return super().create(session).include_item_types(ItemType.MusicAlbum).recursive(True)


class TrackQueryBuilder(ItemQueryBuilder[Track]):
    """Builder for searching track records."""

    @classmethod
    def setup(cls, session: Session) -> Self:
        """Initialise the builder with default search restrictions for tracks."""
        return super().create(session).include_item_types(ItemType.Audio).recursive(True)


class PlaylistQueryBuilder(ItemQueryBuilder[Playlist]):
    """Builder for searching playlist records."""

    @classmethod
    def setup(cls, session: Session) -> Self:
        """Initialise the builder with default search restrictions for playlists."""
        return super().create(session).include_item_types(ItemType.Playlist).recursive(True)
