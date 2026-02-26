"""Switch platform for Tesla Custom."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensor import TeslaBaseEntity

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the switch platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    vehicle_id = data["vehicle_id"]
    vehicle_info = data["vehicle_info"]
    api = data["api"]

    switches = [
        TeslaSentryModeSwitch(coordinator, vehicle_id, vehicle_info, api),
        TeslaClimateSwitch(coordinator, vehicle_id, vehicle_info, api),
    ]
    async_add_entities(switches)

class TeslaSentryModeSwitch(TeslaBaseEntity, SwitchEntity):
    """Sentry mode switch."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_sentry_mode"
        self._attr_name = "Sentry Mode"
        self._attr_icon = "mdi:cctv"

    @property
    def is_on(self):
        """Return true if switch is on."""
        if not self.coordinator.data:
            return False
        return self.coordinator.data.get("vehicle_state", {}).get("sentry_mode")

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.api.command(self.vehicle_id, "set_sentry_mode", {"on": True})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.api.command(self.vehicle_id, "set_sentry_mode", {"on": False})
        await self.coordinator.async_request_refresh()

class TeslaClimateSwitch(TeslaBaseEntity, SwitchEntity):
    """Climate switch."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_climate"
        self._attr_name = "Climate"
        self._attr_icon = "mdi:air-conditioner"

    @property
    def is_on(self):
        """Return true if switch is on."""
        if not self.coordinator.data:
            return False
        return self.coordinator.data.get("climate_state", {}).get("is_climate_on")

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.api.command(self.vehicle_id, "auto_conditioning_start")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.api.command(self.vehicle_id, "auto_conditioning_stop")
        await self.coordinator.async_request_refresh()
