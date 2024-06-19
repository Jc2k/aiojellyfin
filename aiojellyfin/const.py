"""Constants for the Jellyfin APIs."""

from enum import StrEnum


class ItemType(StrEnum):
    """The type of an object in Jellyfin."""

    AggregateFolder = "AggregateFolder"
    Audio = "Audio"
    AudioBook = "AudioBook"
    BasePluginFolder = "BasePluginFolder"
    Book = "Book"
    BoxSet = "BoxSet"
    Channel = "Channel"
    ChannelFolderItem = "ChannelFolderItem"
    CollectionFolder = "CollectionFolder"
    Episode = "Episode"
    Folder = "Folder"
    Genre = "Genre"
    ManualPlaylistsFolder = "ManualPlaylistsFolder"
    Movie = "Movie"
    LiveTvChannel = "LiveTvChannel"
    LiveTvProgram = "LiveTvProgram"
    MusicAlbum = "MusicAlbum"
    MusicArtist = "MusicArtist"
    MusicGenre = "MusicGenre"
    MusicVideo = "MusicVideo"
    Person = "Person"
    Photo = "Photo"
    PhotoAlbum = "PhotoAlbum"
    Playlist = "Playlist"
    PlaylistsFolder = "PlaylistsFolder"
    Program = "Program"
    Recording = "Recording"
    Season = "Season"
    Series = "Series"
    Studio = "Studio"
    Trailer = "Trailer"
    TvChannel = "TvChannel"
    TvProgram = "TvProgram"
    UserRootFolder = "UserRootFolder"
    UserView = "UserView"
    Video = "Video"
    Year = "Year"


class ImageType(StrEnum):
    """The type of an image in Jellyfin."""

    Primary = "Primary"
    Art = "Art"
    Backdrop = "Backdrop"
    Banner = "Banner"
    Logo = "Logo"
    Thumb = "Thumb"
    Disc = "Disc"
    Box = "Box"
    Screenshot = "Screenshot"
    Menu = "Menu"
    Chapter = "Chapter"
    BoxRear = "BoxRear"
    Profile = "Profile"
