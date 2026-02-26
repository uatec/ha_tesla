"""Device tracker platform for Tesla Custom."""
from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensor import TeslaBaseEntity

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the device tracker platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    vehicle_id = data["vehicle_id"]
    vehicle_info = data["vehicle_info"]

    trackers = [
        TeslaDeviceTracker(coordinator, vehicle_id, vehicle_info),
    ]
    async_add_entities(trackers)

class TeslaDeviceTracker(TeslaBaseEntity, TrackerEntity):
    """Device tracker."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_location"
        self._attr_name = "Location"

    @property
    def source_type(self):
        """Return the source type."""
        return SourceType.GPS

    @property
    def latitude(self):
        """Return latitude."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("drive_state", {}).get("latitude")

    @property
    def longitude(self):
        """Return longitude."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("drive_state", {}).get("longitude")
