"""Jellyfin API models."""

from typing import Generic, Required, TypedDict, TypeVar

from .const import ImageType, ItemType


class MediaStream(TypedDict, total=False):
    """Information about a Jellyfin stream."""

    Channels: int
    Codec: str


class MediaSource(TypedDict, total=False):
    """Information about a Jellyfin media source."""

    Path: str


class ArtistItem(TypedDict):
    """Information about a relationship between media and an artist."""

    Id: str
    Name: str


class UserData(TypedDict, total=False):
    """Metadata that is specific to the logged in user, like favorites."""

    IsFavorite: bool


class MediaLibrary(TypedDict, total=False):
    """JSON data describing a single media library."""

    Id: Required[str]
    Name: Required[str]
    CollectionType: str


class MediaLibraries(TypedDict):
    """JSON data describing a collection of media libraries."""

    Items: list[MediaLibrary]
    TotalRecordCount: int
    StartIndex: int


class MediaItem(TypedDict, total=False):
    """JSON data describing a single media item."""

    Id: Required[str]
    Type: ItemType
    Name: str
    MediaType: str
    IndexNumber: int
    SortName: str
    AlbumArtist: str
    Overview: str
    ProductionYear: int
    ProviderIds: dict[str, str]
    CanDownload: bool
    RunTimeTicks: int
    MediaStreams: list[MediaStream]
    AlbumId: str
    Album: str
    ParentIndexNumber: int
    ArtistItems: list[ArtistItem]
    ImageTags: dict[ImageType, str]
    BackdropImageTags: list[str]
    UserData: UserData
    AlbumArtists: list[ArtistItem]
    MediaSources: list[MediaSource]


MediaItemT = TypeVar("MediaItemT", bound=MediaItem)


class MediaItems(Generic[MediaItemT], TypedDict):
    """JSON data describing a collection of media items."""

    Items: list[MediaItemT]
    TotalRecordCount: int
    StartIndex: int


class Artist(MediaItem, TypedDict, total=False):
    """JSON data describing a single artist."""


class Album(MediaItem, TypedDict, total=False):
    """JSON data describing a single album."""


class Track(MediaItem, TypedDict, total=False):
    """JSON data describing a single track."""


class Playlist(MediaItem, TypedDict, total=False):
    """JSON data describing a single playlist."""
