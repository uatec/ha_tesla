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
        TeslaValetModeSwitch(coordinator, vehicle_id, vehicle_info, api),
        TeslaChargingSwitch(coordinator, vehicle_id, vehicle_info, api),
        TeslaMaxRangeSwitch(coordinator, vehicle_id, vehicle_info, api),
        TeslaChargePortSwitch(coordinator, vehicle_id, vehicle_info, api),
        TeslaSpeedLimitSwitch(coordinator, vehicle_id, vehicle_info, api),
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
        return (self.coordinator.data.get("vehicle_state") or {}).get("sentry_mode")

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
        return (self.coordinator.data.get("climate_state") or {}).get("is_climate_on")

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.api.command(self.vehicle_id, "auto_conditioning_start")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.api.command(self.vehicle_id, "auto_conditioning_stop")
        await self.coordinator.async_request_refresh()

class TeslaValetModeSwitch(TeslaBaseEntity, SwitchEntity):
    """Valet Mode switch."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_valet_mode"
        self._attr_name = "Valet Mode"
        self._attr_icon = "mdi:car-key"

    @property
    def is_on(self):
        """Return true if switch is on."""
        if not self.coordinator.data:
            return False
        return (self.coordinator.data.get("vehicle_state") or {}).get("valet_mode")

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        # Note: requires a PIN; using 0000 as a placeholder default if required, 
        # normally you might want to configure this or use the last PIN.
        await self.api.command(self.vehicle_id, "set_valet_mode", params={"on": True, "password": "0000"})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.api.command(self.vehicle_id, "set_valet_mode", params={"on": False, "password": "0000"})
        await self.coordinator.async_request_refresh()

class TeslaChargingSwitch(TeslaBaseEntity, SwitchEntity):
    """Charging active switch."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_charging"
        self._attr_name = "Charging"
        self._attr_icon = "mdi:ev-station"

    @property
    def is_on(self):
        """Return true if switch is on."""
        if not self.coordinator.data:
            return False
        return (self.coordinator.data.get("charge_state") or {}).get("charging_state") == "Charging"

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.api.command(self.vehicle_id, "charge_start")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.api.command(self.vehicle_id, "charge_stop")
        await self.coordinator.async_request_refresh()

class TeslaMaxRangeSwitch(TeslaBaseEntity, SwitchEntity):
    """Max Range Charge Limit switch."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_max_range_charge"
        self._attr_name = "Max Range Charge"
        self._attr_icon = "mdi:battery-arrow-up"

    @property
    def is_on(self):
        """Return true if switch is on."""
        if not self.coordinator.data:
            return False
        # If the charge limit is 100%, consider "max range" to be on
        return (self.coordinator.data.get("charge_state") or {}).get("charge_limit_soc") == 100

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.api.command(self.vehicle_id, "charge_max_range")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.api.command(self.vehicle_id, "charge_standard")
        await self.coordinator.async_request_refresh()

class TeslaChargePortSwitch(TeslaBaseEntity, SwitchEntity):
    """Charge Port switch."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_charge_port"
        self._attr_name = "Charge Port"
        self._attr_icon = "mdi:ev-plug-tesla"

    @property
    def is_on(self):
        """Return true if switch is on."""
        if not self.coordinator.data:
            return False
        return (self.coordinator.data.get("charge_state") or {}).get("charge_port_door_open")

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.api.command(self.vehicle_id, "charge_port_door_open")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.api.command(self.vehicle_id, "charge_port_door_close")
        await self.coordinator.async_request_refresh()

class TeslaSpeedLimitSwitch(TeslaBaseEntity, SwitchEntity):
    """Speed Limit switch."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_speed_limit"
        self._attr_name = "Speed Limit"
        self._attr_icon = "mdi:car-speed-limiter"

    @property
    def is_on(self):
        """Return true if switch is on."""
        if not self.coordinator.data:
            return False
        return (self.coordinator.data.get("vehicle_state") or {}).get("speed_limit_mode", {}).get("active")

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.api.command(self.vehicle_id, "speed_limit_activate", data={"pin": "0000"})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.api.command(self.vehicle_id, "speed_limit_deactivate", data={"pin": "0000"})
        await self.coordinator.async_request_refresh()
