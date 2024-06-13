import uuid
from aiohttp import ClientSession
from typing import LiteralString, TypedDict, Required, cast
import urllib

class MediaLibrary(TypedDict, total=False):
    Id: Required[str]
    Name: Required[str]
    CollectionType: str

class MediaLibraries(TypedDict):
    Items: list[MediaLibrary]
    TotalRecordCount: int
    StartIndex: 0

class Artist(TypedDict, total=False):
    Id: Required[str]
    Name: Required[str]

class Artists(TypedDict):
    Items: list[MediaLibrary]
    TotalRecordCount: int
    StartIndex: 0


"""
search_media_items
get_item
artwork
"""

class Connection:

    def __init__(self, url: str, user_id: str, device_id: str, access_token: str):
        self.base_url = url
        self._session = ClientSession(
            base_url=url,
        )
        self._user_id = user_id
        self._access_token = access_token
        self._device_id = device_id

    async def _get_json(self, url, params):
        resp = await self._session.get(
            url,
            params=params,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Music Assistant/0.0.0",
                "Authorization": _get_authenication_header("Music Assistant", "Music Assistant", str(uuid.uuid4()), "0.0.0", self._access_token),
            },
            raise_for_status=True,
        )
        return await resp.json()
    
    async def get_media_folders(self, fields=None) -> MediaLibraries:
        params = {}
        if fields:
            params["fields"] = fields
        resp = await self._get_json("/Items", params=params)
        return cast(MediaLibraries, resp)
    
    async def artists(self, library_id: str) -> Artists:
        resp = await self._get_json(
            "/Artists",
            params={
                "ParentId": library_id,
                "ArtistType": "Artist,AlbumArtist",
            },
        )
        return cast(Artists, resp)
    
    async def user_items(self, handler: LiteralString="", params=None):
        # FIXME: This will be removed ASAP with something with more typing
        return await self._get_json(
            f"/Items{handler}",
            params=params,
        ) 

    def audio_url(self, item_id: str, container=None, audio_codec=None, max_streaming_bitrate=140000000) -> str:
        params = {
            "UserId": self._user_id,
            "DeviceId": self._device_id,
            "MaxStreamingBitrate": max_streaming_bitrate,
        }

        if container:
            params["Container"] = container

        if audio_codec:
            params["AudioCodec"] = audio_codec

        if "api_key" not in params:
            params["api_key"] = self._access_token

        encoded = urllib.parse.urlencode(params)

        payload = f"{self.base_url}Audio/{item_id}/universal?{encoded}"
        
        return payload
    

def _get_authenication_header(name: str, device: str, device_id: str, version: str, token: str=None) -> str:
    params = {
        "Client": name,
        "Device": device,
        "DeviceId": device_id,
        "Version": version
    }
    if token:
        params["Token"] = token
    param_line = ", ".join(f'{k}="{v}"' for k, v in params.items())
    return f"MediaBrowser {param_line}"


async def authenticate_by_name(url: str, username: str, password: str="") -> Connection:
    session = ClientSession(
        base_url=url,
    )
    async with session:
        res = await session.post(
            "/Users/AuthenticateByName",
            json={"Username": username, "Pw": password},
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Music Assistant/0.0.0",
                "Authorization": _get_authenication_header("Music Assistant", "Music Assistant", str(uuid.uuid4()), "0.0.0"),
            },
            raise_for_status=True,
        )
        user_session = await res.json()

    user = user_session["User"]
    session_info = user_session["SessionInfo"]

    return Connection(url, user["Id"], session_info["DeviceId"], user_session["AccessToken"])