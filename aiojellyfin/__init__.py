"""A simple library for talking to a Jellyfin server."""

import urllib
from typing import Final, cast

from aiohttp import ClientSession
from mashumaro.codecs.basic import BasicDecoder

from .builder import AlbumQueryBuilder, ArtistQueryBuilder, PlaylistQueryBuilder, TrackQueryBuilder
from .const import ImageType, ItemType
from .models import (
    Album,
    Artist,
    MediaItems,
    MediaLibraries,
    Playlist,
    Track,
)
from .session import Session, SessionConfiguration

DEFAULT_FIELDS: Final[str] = (
    "Path,Genres,SortName,Studios,Writer,Taglines,LocalTrailerCount,"
    "OfficialRating,CumulativeRunTimeTicks,ItemCounts,"
    "Metascore,AirTime,DateCreated,People,Overview,"
    "CriticRating,CriticRatingSummary,Etag,ShortOverview,ProductionLocations,"
    "Tags,ProviderIds,ParentId,RemoteTrailers,SpecialEpisodeNumbers,"
    "MediaSources,VoteCount,RecursiveItemCount,PrimaryImageAspectRatio"
)


class NotFound(Exception):
    """Raised when media cannot be found."""


class Connection:
    """A connection to a Jellyfin server."""

    def __init__(self, session_config: SessionConfiguration, user_id: str, access_token: str):
        """Initialise the connection instance."""
        self._session = Session(session_config, user_id, access_token)
        self._session_config = session_config
        self.base_url = session_config.url.rstrip("/")
        self._user_id = user_id
        self._access_token = access_token

        # These will go away when we transition to dataclasses
        self._artist_decoder = BasicDecoder(Artist)
        self._album_decoder = BasicDecoder(Album)
        self._track_decoder = BasicDecoder(Track)
        self._tracks_decoder = BasicDecoder(MediaItems[Track])
        self._playlist_decoder = BasicDecoder(Playlist)

        self.artists = ArtistQueryBuilder.setup(self._session)
        self.albums = AlbumQueryBuilder.setup(self._session)
        self.tracks = TrackQueryBuilder.setup(self._session)
        self.playlists = PlaylistQueryBuilder.setup(self._session)

    async def get_media_folders(self, fields: str | None = None) -> MediaLibraries:
        """Fetch a list of media libraries."""
        params: dict[str, str | int] = {}
        if fields:
            params["fields"] = fields
        resp = await self._session.get_json("/Items", params=params)
        return cast(MediaLibraries, resp)

    async def get_artist(self, artist_id: str) -> Artist:
        """Fetch all data for a single artist."""
        artist = self._artist_decoder.decode(
            await self._session.get_json(
                f"/Users/{self._user_id}/Items/{artist_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if artist["Type"] != ItemType.MusicArtist:
            raise NotFound(artist_id)
        return artist

    async def get_album(self, album_id: str) -> Album:
        """Fetch all data for a single album."""
        album = self._album_decoder.decode(
            await self._session.get_json(
                f"/Users/{self._user_id}/Items/{album_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            )
        )
        if album["Type"] != ItemType.MusicAlbum:
            raise NotFound(album_id)
        return album

    async def get_track(self, track_id: str) -> Track:
        """Fetch all data for a single track."""
        track = self._track_decoder.decode(
            await self._session.get_json(
                f"/Users/{self._user_id}/Items/{track_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if track["Type"] != ItemType.Audio:
            raise NotFound(track_id)
        return track

    async def get_playlist(self, playlist_id: str) -> Playlist:
        """Fetch all data for a single playlist."""
        playlist = self._playlist_decoder.decode(
            await self._session.get_json(
                f"/Users/{self._user_id}/Items/{playlist_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if playlist["Type"] != ItemType.Playlist:
            raise NotFound(playlist_id)
        return playlist

    async def get_suggested_tracks(self) -> MediaItems[Track]:
        """Return suggested tracks."""
        return self._tracks_decoder.decode(
            await self._session.get_json(
                "/Items/Suggestions",
                {
                    "mediaType": "Audio",
                    "type": "Audio",
                    "limit": 50,
                    "enableUserData": "true",
                },
            )
        )

    async def get_similar_tracks(
        self,
        track_id: str,
        limit: int | None = None,
        fields: list[str] | None = None,
    ) -> MediaItems[Track]:
        """Return similar tracks."""
        params: dict[str, str | int] = {}

        if limit:
            params["limit"] = limit

        if fields:
            params["fields"] = ",".join(fields)

        resp = await self._session.get_json(
            f"/Items/{track_id}/Similar",
            params=params or {},
        )
        return self._tracks_decoder.decode(resp)

    def _build_url(self, url: str, params: dict[str, str | int]) -> str:
        assert url.startswith("/")

        if "api_key" not in params:
            params["api_key"] = self._access_token

        encoded = urllib.parse.urlencode(params)

        return f"{self.base_url}{url}?{encoded}"

    def artwork(
        self,
        item_id: str,
        image_type: ImageType,
        max_width: int | None = None,
        extension: str | None = None,
        index: int | None = None,
    ) -> str:
        """Given a TrackId, return a URL to some artwork."""
        params: dict[str, str | int] = {}
        if max_width:
            params["maxWidth"] = max_width
        if extension:
            params["format"] = extension
        if index is None:
            return self._build_url(f"/Items/{item_id}/Images/{image_type!s}", params)
        return self._build_url(f"/Items/{item_id}/Images/{image_type!s}/{index}", params)

    def audio_url(
        self,
        item_id: str,
        container: str | None = None,
        audio_codec: str | None = None,
        max_streaming_bitrate: int = 140000000,
    ) -> str:
        """Given a TrackId, return a URL to stream from."""
        params: dict[str, str | int] = {
            "UserId": self._user_id,
            "DeviceId": self._session_config.device_id,
            "MaxStreamingBitrate": max_streaming_bitrate,
        }

        if container:
            params["Container"] = container

        if audio_codec:
            params["AudioCodec"] = audio_codec

        return self._build_url(f"/Audio/{item_id}/universal", params)


async def authenticate_by_name(
    session_config: SessionConfiguration, username: str, password: str = ""
) -> Connection:
    """Authenticate against a server with a username and password and return a connection."""
    session = ClientSession(
        base_url=session_config.url,
    )
    async with session:
        res = await session.post(
            "/Users/AuthenticateByName",
            json={"Username": username, "Pw": password},
            headers={
                "Content-Type": "application/json",
                "User-Agent": session_config.user_agent,
                "Authorization": session_config.authentication_header(),
            },
            raise_for_status=True,
        )
        user_session = await res.json()

    user = user_session["User"]

    return Connection(session_config, user["Id"], user_session["AccessToken"])
