"""Helpers for testing users of aiojellyfin."""

import copy
import json
from collections import defaultdict
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from aiojellyfin import Connection, NotFound, session
from aiojellyfin.models import (
    Album,
    Artist,
    MediaItems,
    MediaLibraries,
    Playlist,
    Track,
)
from aiojellyfin.session import SessionConfiguration

MUSIC_FOLDER = "8aeb9430-b1d5-420e-9847-3217ac2120c3"


class FixtureBuilder:
    """A set of test data for testing against."""

    def __init__(self) -> None:
        """Init the class."""
        self.objects: dict[str, Any] = {}
        self.objects_parents: dict[str, set[str]] = defaultdict(set)

    def add_json_bytes(self, data: str | bytes) -> None:
        """Add an artist to this fixture."""
        fixture = json.loads(data)
        fixture_id = fixture["Id"]
        self.objects[fixture_id] = fixture
        self.objects_parents[fixture_id].add(MUSIC_FOLDER)

        if parents := fixture.get("AlbumArtists"):
            for artist in parents:
                self.objects_parents[fixture_id].add(artist["Id"])
        if parents := fixture.get("ArtistItems"):
            for artist in parents:
                self.objects_parents[fixture_id].add(artist["Id"])
        if album_id := fixture.get("AlbumId"):
            self.objects_parents[fixture_id].add(album_id)

    def to_authenticate_by_name(
        self,
    ) -> Callable[[SessionConfiguration, str, str], Awaitable[Connection]]:
        """Prepare a monkeypatch."""

        async def authenticate_by_name(
            session_config: SessionConfiguration, _username: str, _password: str
        ) -> Connection:
            return TestConnection(session_config, "TestUserId", "TestAccessToken", self)

        return authenticate_by_name


class Session(session.Session):
    """A fake session for testing only."""

    def __init__(
        self,
        session_config: SessionConfiguration,
        user_id: str,
        access_token: str,
        fixture: FixtureBuilder,
    ):
        """Init the fake session."""
        self.session_config = session_config
        self.user_id = user_id
        self.access_token = access_token
        self.fixture = fixture

    async def get_json(self, url: str, params: Mapping[str, str]) -> dict[str, Any]:
        """Generate a fake response from fixtures."""
        if url in ("/Items", "/Artists"):
            results = []

            for record_id, record in self.fixture.objects.items():
                if url == "/Artists" and record.get("Type") != "MusicArtist":
                    continue

                if parent_id := params.get("parentId"):
                    if parent_id not in self.fixture.objects_parents[record_id]:
                        continue

                if search_term := params.get("searchTerm"):
                    if search_term.lower() not in record["Name"].lower():
                        continue

                if item_types_raw := params.get("includeItemTypes"):
                    item_types = item_types_raw.split(",")
                    if record["Type"] not in item_types:
                        continue

                record_copy = copy.deepcopy(record)

                if not params.get("enableUserData"):
                    record_copy.pop("UserData", None)

                # if fields:

                results.append(record)

            total_record_count = len(results)

            if start_index := params.get("startIndex"):
                results = results[int(start_index) :]

            if limit := params.get("limit"):
                results = results[: int(limit)]

            return {
                "Items": results,
                "StartIndex": start_index or 0,
                "TotalRecordCount": total_record_count,
            }

        raise RuntimeError("Unfaked http request detected")


class TestConnection(Connection):
    """A fake implementation of Connection."""

    def __init__(
        self,
        session_config: SessionConfiguration,
        user_id: str,
        access_token: str,
        fixture: FixtureBuilder,
    ) -> None:
        """Init the class."""
        super().__init__(session_config, user_id, access_token)
        self._fixture = fixture
        self._session = Session(session_config, user_id, access_token, fixture)
        self.artists._session = self._session
        self.albums._session = self._session
        self.tracks._session = self._session
        self.playlists._session = self._session

    async def get_media_folders(self, fields: str | None = None) -> MediaLibraries:
        """Fetch a list of media libraries."""
        return {
            "Items": [
                {
                    "Id": MUSIC_FOLDER,
                    "Name": "Music",
                    "CollectionType": "music",
                }
            ],
            "TotalRecordCount": 1,
            "StartIndex": 0,
        }

    async def get_artist(self, artist_id: str) -> Artist:
        """Fetch all data for a single artist."""
        try:
            return self._fixture.objects[artist_id]
        except KeyError:
            raise NotFound(artist_id)

    async def get_album(self, album_id: str) -> Album:
        """Fetch all data for a single album."""
        try:
            return self._fixture.objects[album_id]
        except KeyError:
            raise NotFound(album_id)

    async def get_track(self, track_id: str) -> Track:
        """Fetch all data for a single track."""
        try:
            return self._fixture.objects[track_id]
        except KeyError:
            raise NotFound(track_id)

    async def get_playlist(self, playlist_id: str) -> Playlist:
        """Fetch all data for a single playlist."""
        try:
            return self._fixture.objects[playlist_id]
        except KeyError:
            raise NotFound(playlist_id)

    async def get_suggested_tracks(self) -> MediaItems[Track]:
        """Return suggested tracks."""
        return {
            "Items": [next(iter(self._fixture.tracks.values()))],
            "StartIndex": 0,
            "TotalRecordCount": 1,
        }

    async def get_similar_tracks(
        self,
        track_id: str,
        limit: int | None = None,
        fields: list[str] | None = None,
    ) -> MediaItems[Track]:
        """Return similar tracks."""
        return {
            "Items": [next(iter(self._fixture.tracks.values()))],
            "StartIndex": 0,
            "TotalRecordCount": 1,
        }
