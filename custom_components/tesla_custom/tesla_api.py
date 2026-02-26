"""Tesla API Client for Home Assistant."""
import logging
from typing import Any, Dict, List, Optional
import aiohttp

_LOGGER = logging.getLogger(__name__)

class TeslaAPI:
    """Client for Tesla Owner API."""

    def __init__(self, token: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self.token = token
        self.session = session
        self.base_url = "https://owner-api.teslamotors.com/api/1"

    @property
    def headers(self) -> Dict[str, str]:
        """Get standard headers for API requests."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "HomeAssistant-TeslaCustom/1.0",
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make an API request."""
        url = f"{self.base_url}/{endpoint}"
        try:
            async with self.session.request(method, url, headers=self.headers, **kwargs) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data.get("response")
        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to Tesla API: %s", err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error from Tesla API: %s", err)
            raise

    async def get_vehicles(self) -> List[Dict[str, Any]]:
        """Get all vehicles."""
        return await self._request("GET", "vehicles")

    async def get_vehicle_data(self, vehicle_id: str) -> Dict[str, Any]:
        """Get all vehicle data."""
        return await self._request("GET", f"vehicles/{vehicle_id}/vehicle_data")

    async def command(self, vehicle_id: str, cmd: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """Send a command to the vehicle."""
        if cmd == "wake_up":
            # Wake up is not a standard command endpoint pattern
            return await self._request("POST", f"vehicles/{vehicle_id}/wake_up")
        
        endpoint = f"vehicles/{vehicle_id}/command/{cmd}"
        return await self._request("POST", endpoint, json=data or {})
