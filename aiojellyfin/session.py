"""A simple library for talking to a Jellyfin server."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Final, cast

from aiohttp import ClientResponseError, ClientSession

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


@dataclass
class SessionConfiguration:
    """Configuration needed to connect to a Jellyfin server."""

    session: ClientSession
    url: str
    app_name: str
    app_version: str
    device_name: str
    device_id: str

    verify_ssl: bool = True

    @property
    def user_agent(self) -> str:
        """Get the user agent for this session."""
        return f"{self.app_name}/{self.app_version}"

    def authentication_header(self, api_token: str | None = None) -> str:
        """Build the Authorization header for this session."""
        params = {
            "Client": self.app_name,
            "Device": self.device_name,
            "DeviceId": self.device_id,
            "Version": self.app_version,
        }
        if api_token:
            params["Token"] = api_token
        param_line = ", ".join(f'{k}="{v}"' for k, v in params.items())
        return f"MediaBrowser {param_line}"


class Session:
    """A connection to a Jellyfin server."""

    def __init__(self, session_config: SessionConfiguration, user_id: str, access_token: str):
        """Initialise the session instance."""
        self._session_config = session_config
        self._session = session_config.session
        self.base_url = session_config.url.rstrip("/")
        self._user_id = user_id
        self._access_token = access_token

    async def get_json(self, url: str, params: Mapping[str, str]) -> dict[str, Any]:
        """Call a Jellyfin API and retrieve the JSON response."""
        try:
            resp = await self._session.get(
                f"{self.base_url}{url}",
                params=params,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": self._session_config.user_agent,
                    "Authorization": self._session_config.authentication_header(self._access_token),
                },
                ssl=self._session_config.verify_ssl,
                raise_for_status=True,
            )
        except ClientResponseError as e:
            if e.status == 404:
                raise NotFound("Resource not found")
            raise

        return cast(dict[str, Any], await resp.json())
