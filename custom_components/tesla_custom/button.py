"""Button platform for Tesla Custom."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensor import TeslaBaseEntity

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the button platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    vehicle_id = data["vehicle_id"]
    vehicle_info = data["vehicle_info"]
    api = data["api"]

    buttons = [
        TeslaWakeUpButton(coordinator, vehicle_id, vehicle_info, api),
        TeslaHornButton(coordinator, vehicle_id, vehicle_info, api),
        TeslaFlashLightsButton(coordinator, vehicle_id, vehicle_info, api),
        TeslaOpenChargePortButton(coordinator, vehicle_id, vehicle_info, api),
        TeslaCloseChargePortButton(coordinator, vehicle_id, vehicle_info, api),
        TeslaActuateTrunkButton(coordinator, vehicle_id, vehicle_info, api),
        TeslaActuateFrunkButton(coordinator, vehicle_id, vehicle_info, api),
    ]
    async_add_entities(buttons)

class TeslaCommandButton(TeslaBaseEntity, ButtonEntity):
    """Base class for command buttons."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info, api, command, name, icon):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self.command_name = command
        self._attr_unique_id = f"{vehicle_id}_{command}"
        self._attr_name = name
        self._attr_icon = icon

    async def async_press(self) -> None:
        """Press the button."""
        await self.api.command(self.vehicle_id, self.command_name)

class TeslaWakeUpButton(TeslaCommandButton):
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info, api, "wake_up", "Wake Up", "mdi:sleep-off")

class TeslaHornButton(TeslaCommandButton):
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info, api, "honk_horn", "Honk Horn", "mdi:bullhorn")

class TeslaFlashLightsButton(TeslaCommandButton):
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info, api, "flash_lights", "Flash Lights", "mdi:car-light-high")

class TeslaOpenChargePortButton(TeslaCommandButton):
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info, api, "charge_port_door_open", "Open Charge Port", "mdi:ev-plug-tesla")

class TeslaCloseChargePortButton(TeslaCommandButton):
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info, api, "charge_port_door_close", "Close Charge Port", "mdi:ev-plug-tesla")

class TeslaActuateTrunkButton(TeslaBaseEntity, ButtonEntity):
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_actuate_trunk"
        self._attr_name = "Actuate Trunk"
        self._attr_icon = "mdi:car-back"

    async def async_press(self) -> None:
        """Press the button."""
        await self.api.command(self.vehicle_id, "actuate_trunk", data={"which_trunk": "rear"})

class TeslaActuateFrunkButton(TeslaBaseEntity, ButtonEntity):
    def __init__(self, coordinator, vehicle_id, vehicle_info, api):
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self.api = api
        self._attr_unique_id = f"{vehicle_id}_actuate_frunk"
        self._attr_name = "Actuate Frunk"
        self._attr_icon = "mdi:car"

    async def async_press(self) -> None:
        """Press the button."""
        await self.api.command(self.vehicle_id, "actuate_trunk", data={"which_trunk": "front"})
