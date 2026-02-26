"""Number platform for Tesla Custom."""
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensor import TeslaBaseEntity

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the number platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    vehicle_id = data["vehicle_id"]
    vehicle_info = data["vehicle_info"]
    api = data["api"]

    numbers = [
        TeslaChargeLimitNumber(coordinator, vehicle_id, vehicle_info, api),
        TeslaTemperatureNumber(coordinator, vehicle_id, vehicle_info, api),
    ]
    async_add_entities(numbers)

class TeslaChargeLimitNumber(TeslaBaseEntity, NumberEntity):
    """Charge limit number."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_charge_limit"
        self._attr_name = "Charge Limit"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_native_min_value = 50
        self._attr_native_max_value = 100
        self._attr_native_step = 1

    @property
    def native_value(self):
        """Return the state of the entity."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("charge_state") or {}).get("charge_limit_soc")

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        await self.api.command(
            self.vehicle_id,
            "set_charge_limit",
            params={"percent": int(value)}
        )
        await self.coordinator.async_request_refresh()

class TeslaTemperatureNumber(TeslaBaseEntity, NumberEntity):
    """Temperature set number."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_temperature_set"
        self._attr_name = "Set Temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_native_min_value = 15
        self._attr_native_max_value = 28
        self._attr_native_step = 0.5

    @property
    def native_value(self):
        """Return the state of the entity."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("climate_state") or {}).get("driver_temp_setting")

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        await self.api.command(
            self.vehicle_id,
            "set_temps",
            params={
                "driver_temp": value,
                "passenger_temp": value
            }
        )
        await self.coordinator.async_request_refresh()
