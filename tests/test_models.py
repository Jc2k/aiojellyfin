"""Test we can parse Jellyfin models into Music Assistant models."""

import pathlib

import pytest
from syrupy.assertion import SnapshotAssertion

from aiojellyfin.models import Album, Artist, Track

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"
ARTIST_FIXTURES = list(FIXTURES_DIR.glob("artists/*.json"))
ALBUM_FIXTURES = list(FIXTURES_DIR.glob("albums/*.json"))
TRACK_FIXTURES = list(FIXTURES_DIR.glob("tracks/*.json"))


@pytest.mark.parametrize("example", ARTIST_FIXTURES, ids=lambda val: str(val.stem))
def test_parse_artists(example: pathlib.Path, snapshot: SnapshotAssertion) -> None:
    """Test we can parse artists."""
    with open(example) as fp:
        parsed = Artist.from_json(fp.read())
    assert snapshot == parsed


@pytest.mark.parametrize("example", ALBUM_FIXTURES, ids=lambda val: str(val.stem))
def test_parse_albums(example: pathlib.Path, snapshot: SnapshotAssertion) -> None:
    """Test we can parse albums."""
    with open(example) as fp:
        parsed = Album.from_json(fp.read())
    assert snapshot == parsed


@pytest.mark.parametrize("example", TRACK_FIXTURES, ids=lambda val: str(val.stem))
def test_parse_tracks(example: pathlib.Path, snapshot: SnapshotAssertion) -> None:
    """Test we can parse tracks."""
    with open(example) as fp:
        parsed = Track.from_json(fp.read())
    assert snapshot == parsed
