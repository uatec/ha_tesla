"""The Tesla Custom integration."""
import asyncio
from datetime import timedelta
import logging

from aiohttp import ClientError
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL, CONF_REFRESH_TOKEN
from .tesla_api import TeslaAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.BUTTON,
    Platform.LOCK,
    Platform.DEVICE_TRACKER,
    Platform.NUMBER,
    Platform.COVER,
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tesla from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    token = entry.data[CONF_ACCESS_TOKEN]
    refresh_token = entry.data.get(CONF_REFRESH_TOKEN)
    session = async_get_clientsession(hass)

    async def token_refresh_cb(new_token: str, new_refresh_token: str):
        """Callback to save the new tokens."""
        hass.config_entries.async_update_entry(
            entry,
            data={
                **entry.data,
                CONF_ACCESS_TOKEN: new_token,
                CONF_REFRESH_TOKEN: new_refresh_token,
            },
        )

    api = TeslaAPI(token, session, refresh_token=refresh_token, token_refresh_cb=token_refresh_cb)

    try:
        vehicles = await api.get_vehicles()
    except Exception as err:
        _LOGGER.error("Could not authenticate with Tesla API: %s", err)
        return False

    if not vehicles:
        _LOGGER.error("No vehicles found on this account")
        return False

    # We will just use the first vehicle for simplicity, or we could set up multiple coordinators
    vehicle_id = vehicles[0]["id_s"]

    # Wake up the vehicle initially, so vehicle_data doesn't fail, though wake_up might take time.
    try:
        await api.command(vehicle_id, "wake_up")
    except Exception:
        _LOGGER.warning("Failed to wake up vehicle %s during setup", vehicle_id)

    async def async_update_data():
        """Fetch data from API."""
        try:
            return await api.get_vehicle_data(vehicle_id)
        except ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Tesla Vehicle Data",
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
        "vehicle_id": vehicle_id,
        "vehicle_info": vehicles[0]
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
