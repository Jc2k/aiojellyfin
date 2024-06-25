"""Helpers for testing users of aiojellyfin."""

import copy
from collections import defaultdict
from collections.abc import Awaitable, Callable

from mashumaro.codecs.json import JSONDecoder

from aiojellyfin import (
    Album,
    Albums,
    Artist,
    Artists,
    Connection,
    MediaLibraries,
    NotFound,
    Playlist,
    Playlists,
    SessionConfiguration,
    Track,
    Tracks,
)

MUSIC_FOLDER = "8aeb9430-b1d5-420e-9847-3217ac2120c3"


class FixtureBuilder:
    """A set of test data for testing against."""

    def __init__(self) -> None:
        """Init the class."""
        self.artists: dict[str, Artist] = {}
        self.artists_parents: dict[str, set[str]] = defaultdict(set)

        self.albums: dict[str, Album] = {}
        self.albums_parents: dict[str, set[str]] = defaultdict(set)

        self.tracks: dict[str, Track] = {}
        self.tracks_parents: dict[str, set[str]] = defaultdict(set)

        self.playlists: dict[str, Playlist] = {}
        self.playlists_parents: dict[str, set[str]] = defaultdict(set)

    def add_artist(self, artist: Artist) -> None:
        """Add an artist to this fixture."""
        artist_id = artist["Id"]

        self.artists[artist_id] = artist
        self.artists_parents[artist_id].add(MUSIC_FOLDER)

    def add_artist_bytes(self, data: str | bytes) -> None:
        """Add an artist to this fixture."""
        artist = JSONDecoder(Artist).decode(data)
        self.add_artist(artist)

    def add_album(self, album: Album) -> None:
        """Add an album to this fixture."""
        album_id = album["Id"]

        self.albums[album_id] = album
        self.albums_parents[album_id].add(MUSIC_FOLDER)
        for artist in album["AlbumArtists"]:
            self.albums_parents[album_id].add(artist["Id"])

    def add_album_bytes(self, data: str | bytes) -> None:
        """Add an album to this fixture."""
        album = JSONDecoder(Album).decode(data)
        self.add_album(album)

    def add_track(self, track: Track) -> None:
        """Add an track to this fixture."""
        track_id = track["Id"]

        self.tracks[track_id] = track
        self.tracks_parents[track_id].add(MUSIC_FOLDER)
        for artist in track["AlbumArtists"]:
            self.tracks_parents[track_id].add(artist["Id"])
        for artist in track["ArtistItems"]:
            self.tracks_parents[track_id].add(artist["Id"])
        if album_id := track.get("AlbumId"):
            self.tracks_parents[track_id].add(album_id)

    def add_track_bytes(self, data: str | bytes) -> None:
        """Add an track to this fixture."""
        track = JSONDecoder(Track).decode(data)
        self.add_track(track)

    def to_authenticate_by_name(
        self,
    ) -> Callable[[SessionConfiguration, str, str], Awaitable[Connection]]:
        """Prepare a monkeypatch."""

        async def authenticate_by_name(
            session_config: SessionConfiguration, _username: str, _password: str
        ) -> Connection:
            return TestConnection(session_config, "TestUserId", "TestAccessToken", self)

        return authenticate_by_name


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

    async def artists(
        self,
        library_id: str | None = None,
        search_term: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[str] | None = None,
        enable_user_data: bool = False,
    ) -> Artists:
        """Fetch a list of artists."""
        results: list[Artist] = []

        for artist_id, artist in self._fixture.artists.items():
            if library_id:
                if library_id not in self._fixture.artists_parents[artist_id]:
                    continue

            if search_term:
                if search_term.lower() not in artist["Name"].lower():
                    continue

            artist_copy = copy.deepcopy(artist)

            if not enable_user_data:
                artist_copy.pop("UserData", None)

            # if fields:

            results.append(artist_copy)

        total_record_count = len(results)

        if start_index:
            results = results[start_index:]

        if limit:
            results = results[:limit]

        return {
            "Items": results,
            "StartIndex": start_index or 0,
            "TotalRecordCount": total_record_count,
        }

    async def albums(
        self,
        library_id: str | None = None,
        search_term: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[str] | None = None,
        enable_user_data: bool = False,
    ) -> Albums:
        """Return all library matching query."""
        results: list[Album] = []

        for album_id, album in self._fixture.albums.items():
            if library_id:
                if library_id not in self._fixture.albums_parents[album_id]:
                    continue

            if search_term:
                if search_term.lower() not in album["Name"].lower():
                    continue

            album_copy = copy.deepcopy(album)

            if not enable_user_data:
                album_copy.pop("UserData", None)

            # if fields:

            results.append(album_copy)

        total_record_count = len(results)

        if start_index:
            results = results[start_index:]

        if limit:
            results = results[:limit]

        return {
            "Items": results,
            "StartIndex": start_index or 0,
            "TotalRecordCount": total_record_count,
        }

    async def tracks(
        self,
        library_id: str | None = None,
        search_term: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[str] | None = None,
        enable_user_data: bool = False,
    ) -> Tracks:
        """Return all library matching query."""
        results: list[Track] = []

        for track_id, track in self._fixture.tracks.items():
            if library_id:
                if library_id not in self._fixture.tracks_parents[track_id]:
                    continue

            if search_term:
                if search_term.lower() not in track["Name"].lower():
                    continue

            track_copy = copy.deepcopy(track)

            if not enable_user_data:
                track_copy.pop("UserData", None)

            # if fields:

            results.append(track_copy)

        total_record_count = len(results)

        if start_index:
            results = results[start_index:]

        if limit:
            results = results[:limit]

        return {
            "Items": results,
            "StartIndex": start_index or 0,
            "TotalRecordCount": total_record_count,
        }

    async def playlists(
        self,
        library_id: str | None = None,
        search_term: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[str] | None = None,
        enable_user_data: bool = False,
    ) -> Playlists:
        """Return all library matching query."""
        results: list[Playlist] = []

        for playlist_id, playlist in self._fixture.playlists.items():
            if library_id:
                if library_id not in self._fixture.playlists_parents[playlist_id]:
                    continue

            if search_term:
                if search_term.lower() not in playlist["Name"].lower():
                    continue

            playlist_copy = copy.deepcopy(playlist)

            if not enable_user_data:
                playlist_copy.pop("UserData", None)

            # if fields:

            results.append(playlist_copy)

        total_record_count = len(results)

        if start_index:
            results = results[start_index:]

        if limit:
            results = results[:limit]

        return {
            "Items": results,
            "StartIndex": start_index or 0,
            "TotalRecordCount": total_record_count,
        }

    async def get_artist(self, artist_id: str) -> Artist:
        """Fetch all data for a single artist."""
        try:
            return self._fixture.artists[artist_id]
        except KeyError:
            raise NotFound(artist_id)

    async def get_album(self, album_id: str) -> Album:
        """Fetch all data for a single album."""
        try:
            return self._fixture.albums[album_id]
        except KeyError:
            raise NotFound(album_id)

    async def get_track(self, track_id: str) -> Track:
        """Fetch all data for a single track."""
        try:
            return self._fixture.tracks[track_id]
        except KeyError:
            raise NotFound(track_id)

    async def get_playlist(self, playlist_id: str) -> Playlist:
        """Fetch all data for a single playlist."""
        try:
            return self._fixture.playlists[playlist_id]
        except KeyError:
            raise NotFound(playlist_id)

    async def get_suggested_tracks(self) -> Tracks:
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
    ) -> Tracks:
        """Return similar tracks."""
        return {
            "Items": [next(iter(self._fixture.tracks.values()))],
            "StartIndex": 0,
            "TotalRecordCount": 1,
        }
