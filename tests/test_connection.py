"""Test the connection object."""

import pathlib
from collections.abc import AsyncGenerator

import aiohttp
import pytest

from aiojellyfin import Connection
from aiojellyfin.session import SessionConfiguration
from aiojellyfin.testing import FixtureBuilder

FIXTURES_ROOT = pathlib.Path(__file__).parent / "fixtures"
FIXTURES_ARTISTS = FIXTURES_ROOT / "artists"
FIXTURES_ALBUMS = FIXTURES_ROOT / "albums"
FIXTURES_TRACKS = FIXTURES_ROOT / "tracks"
# FIXTURES_PLAYLISTS = FIXTURES_ROOT / "playlist"


@pytest.fixture
async def connection() -> AsyncGenerator[Connection, None]:
    """Configure an aiojellyfin test fixture."""
    f = FixtureBuilder()

    for path in (FIXTURES_ARTISTS, FIXTURES_ALBUMS, FIXTURES_TRACKS):
        for child in path.glob("*.json"):
            f.add_json_bytes(child.read_bytes())

    authenticate_by_name = f.to_authenticate_by_name()

    async with aiohttp.ClientSession() as session:
        session_config = SessionConfiguration(
            session, "http://localhost", "test", "1.0", "test", "test"
        )
        connection = await authenticate_by_name(session_config, "test_user_id", "test_api_key")
        yield connection


async def test_get_folders(connection: Connection) -> None:
    """Make sure we can get folders."""
    folders = await connection.get_media_folders()
    assert folders["Items"][0]["Name"] == "Music"


async def test_get_artist(connection: Connection) -> None:
    """Make sure we can get artists."""
    artist = await connection.get_artist("dd954bbf54398e247d803186d3585b79")
    assert artist["Name"] == "Ash"


async def test_list_artists(connection: Connection) -> None:
    """Make sure we can list artists."""
    artists = set()
    async for artist in connection.artists.stream():
        artists.add(artist["Name"])
    assert artists == {"Ash"}


async def test_search_artists(connection: Connection) -> None:
    """Make sure we can search artists."""
    artists = set()
    async for artist in connection.artists.search_term("B").stream():
        artists.add(artist["Name"])
    assert artists == set()
    async for artist in connection.artists.search_term("A").stream():
        artists.add(artist["Name"])
    assert artists == {"Ash"}


async def test_get_album(connection: Connection) -> None:
    """Make sure we can get albums."""
    artist = await connection.get_album("70b7288088b42d318f75dbcc41fd0091")
    assert artist["Name"] == "Infest"


async def test_list_albums(connection: Connection) -> None:
    """Make sure we can list albums."""
    albums = set()
    async for artist in connection.albums.stream():
        albums.add(artist["Name"])
    assert albums == {
        "Infest",
        "This Is Christmas",
        "Yesterday, When I Was Mad [Disc 2]",
    }


async def test_search_albums(connection: Connection) -> None:
    """Make sure we can search albums."""
    albums = set()
    async for artist in connection.albums.search_term("B").stream():
        albums.add(artist["Name"])
    assert albums == set()
    async for artist in connection.albums.search_term("A").stream():
        albums.add(artist["Name"])
    assert albums == {
        "This Is Christmas",
        "Yesterday, When I Was Mad [Disc 2]",
    }


async def test_get_tracks(connection: Connection) -> None:
    """Make sure we can get tracks."""
    artist = await connection.get_track("54918f75ee8f6c8b8dc5efd680644f29")
    assert artist["Name"] == "Where the Bands Are (2018 Version)"


async def test_list_tracks(connection: Connection) -> None:
    """Make sure we can list tracks."""
    tracks = set()
    async for track in connection.tracks.stream():
        tracks.add(track["Name"])
    assert tracks == {
        "11 Thrown Away",
        "Where the Bands Are (2018 Version)",
        "Zombie Christmas",
    }


async def test_search_tracks(connection: Connection) -> None:
    """Make sure we can search tracks."""
    tracks = set()
    async for track in connection.tracks.search_term("I know a song").stream():
        tracks.add(track["Name"])
    assert tracks == set()
    async for track in connection.tracks.search_term("A").stream():
        tracks.add(track["Name"])
    assert tracks == {
        "11 Thrown Away",
        "Where the Bands Are (2018 Version)",
        "Zombie Christmas",
    }


async def test_similar_tracks(connection: Connection) -> None:
    """Make sure we can get similar tracks."""
    tracks = await connection.get_similar_tracks("54918f75ee8f6c8b8dc5efd680644f29")
    assert len(tracks["Items"]) == 1
    assert tracks["Items"][0]["Name"] == "11 Thrown Away"


async def test_get_suggestions(connection: Connection) -> None:
    """Make sure we can get suggestions."""
    tracks = await connection.get_suggested_tracks()
    assert len(tracks["Items"]) == 1
    assert tracks["Items"][0]["Name"] == "11 Thrown Away"
