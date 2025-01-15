"""Jellyfin API models."""

from dataclasses import dataclass
from typing import Annotated, Generic, Sequence, TypeVar

from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.config import BaseConfig
from mashumaro.types import Discriminator

from .const import ImageType, ItemType, MediaProtocol, MediaSourceType


class JellyfinConfig(BaseConfig):

    forbid_extra_keys = False


@dataclass(kw_only=True)
class MediaStream(DataClassJSONMixin):
    """Information about a Jellyfin stream."""

    class Config(BaseConfig):
        discriminator = Discriminator(
            field="Type",
            include_subtypes=True,
        )

    Codec: str
    TimeBase: str | None
    AudioSpacialFormat: str | None = None
    IsInterlaced: bool | None
    IsAVC: bool | None
    IsDefault: bool | None
    IsForced: bool | None
    IsHearingImpaired: bool | None
    Profile: str | None = None
    Type: str | None
    Index: int | None
    IsExternal: bool | None
    IsTextSubtitleStream: bool | None
    SupportsExternalStream: bool | None
    Level: bool | None

@dataclass(kw_only=True)
class AudioMediaStream(MediaStream):
    Type = "Audio"

    CodecTag: str | None = None     
    Language: str | None = None
    DisplayTitle: str
    ChannelLayout: str
    BitRate: int
    Channels: int
    SampleRate: int

@dataclass(kw_only=True)
class EmbeddedImageMediaStream(MediaStream):
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

    Config = JellyfinConfig

    Id: str
    Type: ItemType
    Name: str
    MediaType: str
    SortName: str
    ProviderIds: dict[str, str]
    RunTimeTicks: int
    ImageTags: dict[ImageType, str]
    BackdropImageTags: list[str]
    UserData: UserData
    Overview: str | None = None
    IndexNumber: int | None = None
    

MediaItemT = TypeVar("MediaItemT", bound=MediaItem)


@dataclass(kw_only=True)
class MediaItems(Generic[MediaItemT], DataClassJSONMixin):
    """JSON data describing a collection of media items."""

    Config = JellyfinConfig

    Items: list[MediaItemT]
    TotalRecordCount: int
    StartIndex: int


@dataclass(kw_only=True)
class Artist(MediaItem):
    """JSON data describing a single artist."""


@dataclass(kw_only=True)
class Album(MediaItem):
    """JSON data describing a single album."""

    CanDownload: bool | None = None
    ProductionYear: int | None = None
    ArtistItems: list[ArtistItem]
    AlbumArtists: list[ArtistItem]


@dataclass(kw_only=True)
class Track(MediaItem):
    """JSON data describing a single track."""

    AlbumId: str | None = None
    Album: str | None = None
    AlbumArtist: str | None = None
    CanDownload: bool
    ProductionYear: int | None = None
    ParentIndexNumber: int
    MediaSources: list[MediaSource]
    MediaStreams: Sequence[MediaStream] | None
    NormalizationGain: int | None = None
    ArtistItems: list[ArtistItem]
    AlbumArtists: list[ArtistItem]


@dataclass(kw_only=True)
class Playlist(MediaItem):
    """JSON data describing a single playlist."""
