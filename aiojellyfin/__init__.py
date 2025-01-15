"""A simple library for talking to a Jellyfin server."""

import urllib
from typing import Final, cast

from mashumaro.codecs.basic import BasicDecoder

from .builder import AlbumQueryBuilder, ArtistQueryBuilder, PlaylistQueryBuilder, TrackQueryBuilder
from .const import ImageType, ItemFields, ItemType
from .models import (
    Album,
    Artist,
    MediaItem,
    MediaItems,
    MediaLibraries,
    MediaLibrary,
    Playlist,
    Track,
)
from .session import Session, SessionConfiguration

__all__ = [
    "Album",
    "Artist",
    "Connection",
    "ImageType",
    "ItemFields",
    "ItemType",
    "MediaItem",
    "MediaItems",
    "MediaLibraries",
    "MediaLibrary",
    "NotFound",
    "Playlist",
    "Track",
    "authenticate_by_name",
]

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

        self.artists = ArtistQueryBuilder.setup(self._session)
        self.albums = AlbumQueryBuilder.setup(self._session)
        self.tracks = TrackQueryBuilder.setup(self._session)
        self.playlists = PlaylistQueryBuilder.setup(self._session)

    async def get_media_folders(self, fields: str | None = None) -> MediaLibraries:
        """Fetch a list of media libraries."""
        params: dict[str, str] = {}
        if fields:
            params["fields"] = fields
        resp = await self._session.get_json("/Items", params=params)
        return cast(MediaLibraries, resp)

    async def get_artist(self, artist_id: str) -> Artist:
        """Fetch all data for a single artist."""
        artist = Artist.from_dict(
            await self._session.get_json(
                f"/Users/{self._user_id}/Items/{artist_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if artist.Type != ItemType.MusicArtist:
            raise NotFound(artist_id)
        return artist

    async def get_album(self, album_id: str) -> Album:
        """Fetch all data for a single album."""
        album = Album.from_dict(
            await self._session.get_json(
                f"/Users/{self._user_id}/Items/{album_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            )
        )
        if album.Type != ItemType.MusicAlbum:
            raise NotFound(album_id)
        return album

    async def get_track(self, track_id: str) -> Track:
        """Fetch all data for a single track."""
        track = Track.from_dict(
            await self._session.get_json(
                f"/Users/{self._user_id}/Items/{track_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if track.Type != ItemType.Audio:
            raise NotFound(track_id)
        return track

    async def get_playlist(self, playlist_id: str) -> Playlist:
        """Fetch all data for a single playlist."""
        playlist = Playlist.from_dict(
            await self._session.get_json(
                f"/Users/{self._user_id}/Items/{playlist_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if playlist.Type != ItemType.Playlist:
            raise NotFound(playlist_id)
        return playlist

    async def get_suggested_tracks(self) -> MediaItems[Track]:
        """Return suggested tracks."""
        return MediaItems[Track].from_dict(
            await self._session.get_json(
                "/Items/Suggestions",
                {
                    "mediaType": "Audio",
                    "type": "Audio",
                    "limit": "50",
                    "enableUserData": "true",
                },
            )
        )

    async def get_similar_tracks(
        self,
        track_id: str,
        limit: int | None = None,
        fields: list[ItemFields] | None = None,
    ) -> MediaItems[Track]:
        """Return similar tracks."""
        params: dict[str, str] = {}

        if limit:
            params["limit"] = str(limit)

        if fields:
            params["fields"] = ",".join(f.value for f in fields)

        resp = await self._session.get_json(
            f"/Items/{track_id}/Similar",
            params=params or {},
        )
        return MediaItems[Track].from_dict(resp)

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

    def audio_url(  # noqa: PLR0913
        self,
        item_id: str,
        media_source_id: str | None = None,
        container: str | None = None,
        max_streaming_bitrate: int = 140000000,
        max_audio_channels: int | None = None,
        max_audio_sample_rate: int | None = None,
        max_audio_bit_depth: int | None = None,
        enable_remote_media: bool | None = None,
        transcoding_codec: str | None = None,
        transcoding_bit_rate: str | None = None,
        transcoding_protocol: str | None = None,
        transcoding_container: str | None = None,
        transcoding_audio_channels: int | None = None,
        start_time_ticks: int | None = None,
        enable_audio_vbr_encoding: bool | None = None,
        enable_redirection: bool | None = None,
        break_on_non_key_frames: bool | None = None,
    ) -> str:
        """Given a TrackId, return a URL to stream from."""
        params: dict[str, str | int] = {
            "userId": self._user_id,
            "deviceId": self._session_config.device_id,
            "maxStreamingBitrate": max_streaming_bitrate,
        }

        # Filters for which stream to select
        if media_source_id:
            params["mediaSourceId"] = media_source_id

        if container:
            params["container"] = container

        if max_audio_channels:
            params["maxAudioChannels"] = max_audio_channels

        if max_audio_sample_rate:
            params["maxAudioSampleRate"] = max_audio_sample_rate

        if max_audio_bit_depth:
            params["maxAudioBitDepth"] = max_audio_bit_depth

        if enable_remote_media:
            params["enableRemoteMedia"] = "true" if enable_remote_media else "false"

        # Transcoding settings
        if transcoding_codec:
            params["audioCodec"] = transcoding_codec

        if transcoding_bit_rate:
            params["audioBitrate"] = transcoding_bit_rate

        if transcoding_protocol:
            params["transcodingProtocol"] = transcoding_protocol

        if transcoding_container:
            params["transcodingContainer"] = transcoding_container

        if transcoding_audio_channels:
            params["transcodingAudioChannels"] = str(transcoding_audio_channels)

        if start_time_ticks:
            params["startTimeTicks"] = str(start_time_ticks)

        if enable_audio_vbr_encoding:
            params["enableAudioVbrEncoding"] = "true" if enable_audio_vbr_encoding else "false"

        # Misc settings
        if enable_redirection:
            params["enableRedirection"] = "true" if enable_redirection else "false"

        if break_on_non_key_frames:
            params["breakOnNonKeyFrames"] = "true" if break_on_non_key_frames else "false"

        return self._build_url(f"/Audio/{item_id}/universal", params)


async def authenticate_by_name(
    session_config: SessionConfiguration, username: str, password: str = ""
) -> Connection:
    """Authenticate against a server with a username and password and return a connection."""
    base_url = session_config.url.rstrip("/")
    res = await session_config.session.post(
        f"{base_url}/Users/AuthenticateByName",
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
