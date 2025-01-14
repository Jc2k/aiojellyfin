"""Builder pattern for building Jellyfin API queries."""

import asyncio
import copy
from collections.abc import AsyncGenerator
from typing import Generic, Self

from mashumaro.codecs.basic import BasicDecoder

from .const import ItemFields, ItemFilter, ItemType, LocationType
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
        endpoint: str,
        params: dict[str, str],
    ):
        """Initialise the class."""
        self._decoder = decoder
        self._session = session
        self.endpoint = endpoint
        self._params = params

    @classmethod
    def create(cls, session: Session) -> Self:
        """Create a new query builder instance."""
        decoder = BasicDecoder(MediaItems[MediaItemT])
        return cls(session, decoder, cls.endpoint, {})

    def _clone(self) -> Self:
        return self.__class__(
            self._session,
            self._decoder,
            self.endpoint,
            copy.deepcopy(self._params),
        )

    def _clone_and_set(self, params: dict[str, str]) -> Self:
        result = self._clone()
        result._params.update(params)
        return result

    def user_id(self, user_id: str) -> Self:
        """Set the user_id for the query; this is required when not using an API key."""
        return self._clone_and_set({"userId": user_id})

    def parent(self, parent_id: str) -> Self:
        """Specify this to localize the search to a specific item or folder.

        Omit to use the root.
        """
        return self._clone_and_set({"parentId": parent_id})

    def search_term(self, search_term: str) -> Self:
        """Search for this term."""
        return self._clone_and_set({"searchTerm": search_term})

    def filters(self, *filters: ItemFilter) -> Self:
        """Specify additional filters to apply."""
        return self._clone_and_set({"filters": ",".join(f.value for f in filters)})

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

    def include_location_types(self, *args: LocationType) -> Self:
        """If specified, results will be filtered based on the LocationType."""
        return self._clone_and_set({"locationTypes": ",".join(arg.value for arg in args)})

    def exclude_location_types(self, *args: LocationType) -> Self:
        """If specified, results will be filtered based on the LocationType."""
        return self._clone_and_set({"excludeLocationTypes": ",".join(arg.value for arg in args)})

    def recursive(self, recursive: bool) -> Self:
        """Search parent folder and all child folders."""
        result = self._clone()
        result._params["recursive"] = "true" if recursive else "false"
        return result

    def max_official_rating(self, rating: str) -> Self:
        """Filter by maximum official rating (PG, PG-13, TV-MA, etc)."""
        return self._clone_and_set({"maxOfficialRating": rating})

    def has_theme_song(self, has_theme_song: bool) -> Self:
        """Filter by items with theme songs."""
        return self._clone_and_set({"hasThemeSong": "true" if has_theme_song else "false"})

    def has_theme_video(self, has_theme_video: bool) -> Self:
        """Filter by items with theme videos."""
        return self._clone_and_set({"hasThemeVideo": "true" if has_theme_video else "false"})

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
        """Stream all records matching this query with automatic greedy pagination."""
        request = self.limit(page_size)
        response = await request.request()
        offset = 0

        while offset < response["TotalRecordCount"]:
            offset += page_size
            next_response = asyncio.create_task(request.start_index(offset).request())

            for obj in response["Items"]:
                yield obj

            response = await next_response

        for obj in response["Items"]:
            yield obj


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
        return super().create(session).include_item_types(ItemType.Audio, ItemType.MusicVideo).recursive(True)

    def in_playlist(self, playlist_id: str) -> Self:
        """Only look inside the named playlist. Items are returned in the correct order."""
        result = self._clone()
        result.endpoint = f"/Playlists/{playlist_id}/Items"
        return result


class PlaylistQueryBuilder(ItemQueryBuilder[Playlist]):
    """Builder for searching playlist records."""

    @classmethod
    def setup(cls, session: Session) -> Self:
        """Initialise the builder with default search restrictions for playlists."""
        return super().create(session).include_item_types(ItemType.Playlist).recursive(True)
