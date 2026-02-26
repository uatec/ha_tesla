"""Lock platform for Tesla Custom."""
from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensor import TeslaBaseEntity

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the lock platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    vehicle_id = data["vehicle_id"]
    vehicle_info = data["vehicle_info"]
    api = data["api"]

    locks = [
        TeslaDoorLock(coordinator, vehicle_id, vehicle_info, api),
    ]
    async_add_entities(locks)

class TeslaDoorLock(TeslaBaseEntity, LockEntity):
    """Door lock."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_doors"
        self._attr_name = "Doors"

    @property
    def is_locked(self):
        """Return true if locked."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("vehicle_state", {}).get("locked")

    async def async_lock(self, **kwargs):
        """Lock the car."""
        await self.api.command(self.vehicle_id, "door_lock")
        await self.coordinator.async_request_refresh()

    async def async_unlock(self, **kwargs):
        """Unlock the car."""
        await self.api.command(self.vehicle_id, "door_unlock")
        await self.coordinator.async_request_refresh()
