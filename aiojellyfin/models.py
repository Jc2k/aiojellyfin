"""Jellyfin API models."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

from mashumaro.config import BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.types import Discriminator

from .const import ImageType, ItemType, MediaProtocol, MediaSourceType


class JellyfinConfig(BaseConfig):
    """Mashumaro configuration."""

    forbid_extra_keys = False


@dataclass(kw_only=True)
class MediaStream(DataClassJSONMixin):
    """Information about a Jellyfin stream."""

    class Config(BaseConfig):
        """Mashumaro configuration."""

        discriminator = Discriminator(
            field="Type",
            include_subtypes=True,
        )

        aliases = {
            "codec": "Codec",
            "time_base": "TimeBase",
            "audio_spacial_format": "AudioSpacialFormat",
            "is_interlaced": "IsInterlaced",
            "is_avc": "IsAVC",
            "is_default": "IsDefault",
            "is_forced": "IsForced",
            "is_hearing_impaired": "IsHearingImpaired",
            "profile": "Profile",
            "media_stream_type": "Type",
            "index": "Index",
            "is_external": "IsExternal",
            "is_text_subtitle_stream": "IsTextSubtitleStream",
            "supports_external_stream": "SupportsExternalStream",
            "level": "Level",
        }

    codec: str
    time_base: str | None
    audio_spacial_format: str | None = None
    is_interlaced: bool | None
    is_avc: bool | None
    is_default: bool | None
    is_forced: bool | None
    is_hearing_impaired: bool | None
    profile: str | None = None
    media_stream_type: str | None
    index: int | None
    is_external: bool | None
    is_text_subtitle_stream: bool | None
    supports_external_stream: bool | None
    level: bool | None


@dataclass(kw_only=True)
class AudioMediaStream(MediaStream):
    """An audio media stream."""

    Type = "Audio"

    class Config(BaseConfig):
        """Mashumaro configuration."""

        aliases = {
            "codec_tag": "CodecTag",
            "language": "Language",
            "display_title": "DisplayTitle",
            "channel_layout": "ChannelLayout",
            "bit_rate": "BitRate",
            "channels": "Channels",
            "sample_rate": "SampleRate",
        }

    codec_tag: str | None = None
    language: str | None = None
    display_title: str
    channel_layout: str
    bit_rate: int
    channels: int
    sample_rate: int


@dataclass(kw_only=True)
class EmbeddedImageMediaStream(MediaStream):
    """An embedded image stream."""

    Type = "EmbeddedImage"


@dataclass(kw_only=True)
class MediaSource(DataClassJSONMixin):
    """Information about a Jellyfin media source."""

    Config = JellyfinConfig

    Protocol: MediaProtocol
    Id: str | None
    Path: str
    Type: MediaSourceType
    Container: str | None
    Size: int | None
    Name: str | None
    SupportsDirectPlay: bool | None
    SupportsDirectStream: bool | None
    SupportsTranscoding: bool | None
    MediaStreams: Sequence[MediaStream] | None


@dataclass(kw_only=True)
class ArtistItem:
    """Information about a relationship between media and an artist."""

    Config = JellyfinConfig

    Id: str
    Name: str


@dataclass(kw_only=True)
class UserData:
    """Metadata that is specific to the logged in user, like favorites."""

    Config = JellyfinConfig

    IsFavorite: bool


@dataclass(kw_only=True)
class MediaLibrary:
    """JSON data describing a single media library."""

    Config = JellyfinConfig

    Id: str
    Name: str
    CollectionType: str


@dataclass(kw_only=True)
class MediaLibraries:
    """JSON data describing a collection of media libraries."""

    Config = JellyfinConfig

    Items: list[MediaLibrary]
    TotalRecordCount: int
    StartIndex: int


@dataclass(kw_only=True)
class MediaItem(DataClassJSONMixin):
    """JSON data describing a single media item."""

    class Config(BaseConfig):
        """Config for mashumaro."""

        discriminator = Discriminator(
            field="Type",
            include_subtypes=True,
        )

        aliases = {
            "id": "Id",
            "item_type": "Type",
            "name": "Name",
            "media_type": "MediaType",
            "sort_name": "SortName",
            "provider_ids": "ProviderIds",
            "run_time_ticks": "RunTimeTicks",
            "image_tags": "ImageTags",
            "backdrop_image_tags": "BackdropImageTags",
            "user_data": "UserData",
            "overview": "Overview",
            "index_number": "IndexNumber",
        }

    id: str
    item_type: ItemType
    name: str
    media_type: str
    sort_name: str | None = None
    provider_ids: dict[str, str] | None = None
    run_time_ticks: int
    image_tags: dict[ImageType, str]
    backdrop_image_tags: list[str]
    user_data: UserData | None = None
    overview: str | None = None
    index_number: int | None = None


MediaItemT = TypeVar("MediaItemT", bound=MediaItem)


@dataclass(kw_only=True)
class MediaItems(Generic[MediaItemT], DataClassJSONMixin):
    """JSON data describing a collection of media items."""

    class Config(BaseConfig):
        """Config for mashumaro."""

        aliases = {
            "items": "Items",
            "total_record_count": "TotalRecordCount",
            "start_index": "StartIndex",
        }

    items: list[MediaItemT]
    total_record_count: int
    start_index: int


@dataclass(kw_only=True)
class Artist(MediaItem):
    """JSON data describing a single artist."""

    Type = ItemType.MusicArtist


@dataclass(kw_only=True)
class Album(MediaItem):
    """JSON data describing a single album."""

    Type = ItemType.MusicAlbum

    CanDownload: bool | None = None
    ProductionYear: int | None = None
    ArtistItems: list[ArtistItem]
    AlbumArtists: list[ArtistItem]


@dataclass(kw_only=True)
class Track(MediaItem):
    """JSON data describing a single track."""

    Type = ItemType.Audio

    AlbumId: str | None = None
    Album: str | None = None
    AlbumArtist: str | None = None
    CanDownload: bool | None = None
    ProductionYear: int | None = None
    ParentIndexNumber: int
    MediaSources: list[MediaSource] | None = None
    MediaStreams: Sequence[MediaStream] | None = None
    NormalizationGain: int | None = None
    ArtistItems: list[ArtistItem]
    AlbumArtists: list[ArtistItem]


@dataclass(kw_only=True)
class Playlist(MediaItem):
    """JSON data describing a single playlist."""

    Type = ItemType.Playlist
