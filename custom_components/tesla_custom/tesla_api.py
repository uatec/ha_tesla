"""Tesla API Client for Home Assistant."""
import logging
from typing import Any, Dict, List, Optional
import aiohttp

_LOGGER = logging.getLogger(__name__)

class TeslaAPI:
    """Client for Tesla Owner API."""

    def __init__(self, token: str, session: aiohttp.ClientSession, refresh_token: Optional[str] = None, token_refresh_cb=None):
        """Initialize the API client."""
        self.token = token
        self.session = session
        self.refresh_token = refresh_token
        self.token_refresh_cb = token_refresh_cb
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
            return await self._execute_request(method, url, **kwargs)
        except aiohttp.ClientResponseError as err:
            if err.status == 401 and self.refresh_token:
                _LOGGER.info("Access token expired. Attempting to refresh.")
                await self.async_refresh_token()
                # Retry the request with the new token
                return await self._execute_request(method, url, **kwargs)
            else:
                _LOGGER.error("Error connecting to Tesla API: %s", err)
                raise
        except Exception as err:
            _LOGGER.error("Unexpected error from Tesla API: %s", err)
            raise

    async def _execute_request(self, method: str, url: str, **kwargs) -> Any:
        async with self.session.request(method, url, headers=self.headers, **kwargs) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data.get("response")

    async def async_refresh_token(self):
        """Refresh the access token."""
        url = "https://auth.tesla.com/oauth2/v3/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": "ownerapi",
            "refresh_token": self.refresh_token,
        }
        async with self.session.post(url, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            self.token = data["access_token"]
            self.refresh_token = data.get("refresh_token", self.refresh_token)
            
            if self.token_refresh_cb:
                await self.token_refresh_cb(self.token, self.refresh_token)

    async def get_vehicles(self) -> List[Dict[str, Any]]:
        """Get all vehicles."""
        # Tesla removed the /vehicles endpoint, we must use /products
        products = await self._request("GET", "products")
        if not products:
            return []
        
        # Filter for products that are actually vehicles (they have a VIN)
        return [p for p in products if "vin" in p]

    async def get_vehicle_data(self, vehicle_id: str) -> Dict[str, Any]:
        """Get all vehicle data."""
        endpoints = (
            "location_data;charge_state;climate_state;closures_state;"
            "drive_state;gui_settings;vehicle_config;vehicle_state;vehicle_data_combo"
        )
        return await self._request("GET", f"vehicles/{vehicle_id}/vehicle_data", params={"endpoints": endpoints})

    async def command(self, vehicle_id: str, cmd: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a command to the vehicle."""
        if cmd == "wake_up":
            # Wake up is not a standard command endpoint pattern
            return await self._request("POST", f"vehicles/{vehicle_id}/wake_up")
        
        endpoint = f"vehicles/{vehicle_id}/command/{cmd}"
        return await self._request("POST", endpoint, json=data or {}, params=params)
