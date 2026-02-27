"""Cover platform for Tesla Custom."""
from homeassistant.components.cover import CoverEntity, CoverDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensor import TeslaBaseEntity

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the cover platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    vehicle_id = data["vehicle_id"]
    vehicle_info = data["vehicle_info"]
    api = data["api"]

    covers = [
        TeslaRearTrunkCover(coordinator, vehicle_id, vehicle_info, api),
        TeslaFrontTrunkCover(coordinator, vehicle_id, vehicle_info, api),
    ]
    async_add_entities(covers)

class TeslaCommandCover(TeslaBaseEntity, CoverEntity):
    """Base class for command covers."""

    def __init__(self, coordinator, vehicle_id, vehicle_info, api, trunk_name, unique_id_suffix):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self.trunk_name = trunk_name
        self._attr_unique_id = f"{vehicle_id}_{unique_id_suffix}"
        self._attr_device_class = CoverDeviceClass.DOOR

    async def async_open_cover(self, **kwargs) -> None:
        """Open the cover."""
        if not self.is_opened:
            await self.api.command(self.vehicle_id, "actuate_trunk", data={"which_trunk": self.trunk_name})
            await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs) -> None:
        """Close the cover."""
        if self.is_opened:
            await self.api.command(self.vehicle_id, "actuate_trunk", data={"which_trunk": self.trunk_name})
            await self.coordinator.async_request_refresh()

class TeslaRearTrunkCover(TeslaCommandCover):
    """Rear Trunk cover."""

    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info, api, "rear", "rear_trunk_cover")
        self._attr_name = "Rear Trunk"

    @property
    def is_opened(self) -> bool:
        """Return true if cover is open."""
        if not self.coordinator.data:
            return False
        return (self.coordinator.data.get("vehicle_state") or {}).get("rt", 0) > 0

    @property
    def is_closed(self) -> bool:
        """Return true if cover is closed."""
        return not self.is_opened

class TeslaFrontTrunkCover(TeslaCommandCover):
    """Front Trunk cover."""

    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info, api, "front", "front_trunk_cover")
        self._attr_name = "Front Trunk"

    @property
    def is_opened(self) -> bool:
        """Return true if cover is open."""
        if not self.coordinator.data:
            return False
        return (self.coordinator.data.get("vehicle_state") or {}).get("ft", 0) > 0

    @property
    def is_closed(self) -> bool:
        """Return true if cover is closed."""
        return not self.is_opened
