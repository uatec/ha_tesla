"""Binary Sensor platform for Tesla Custom."""
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensor import TeslaBaseEntity

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the binary sensor platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    vehicle_id = data["vehicle_id"]
    vehicle_info = data["vehicle_info"]

    sensors = [
        TeslaIsUserPresentBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaBatteryHeaterBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaSteeringWheelHeaterBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaWiperBladeHeaterBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaFastChargerPresentBinarySensor(coordinator, vehicle_id, vehicle_info),
    ]
    async_add_entities(sensors)

class TeslaIsUserPresentBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Is User Present binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_is_user_present"
        self._attr_name = "User Present"
        self._attr_device_class = BinarySensorDeviceClass.PRESENCE

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("is_user_present")

class TeslaBatteryHeaterBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Battery Heater binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_battery_heater"
        self._attr_name = "Battery Heater"
        self._attr_device_class = BinarySensorDeviceClass.HEAT

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("climate_state") or {}).get("battery_heater")

class TeslaSteeringWheelHeaterBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Steering Wheel Heater binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_steering_wheel_heater"
        self._attr_name = "Steering Wheel Heater"
        self._attr_device_class = BinarySensorDeviceClass.HEAT

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("climate_state") or {}).get("steering_wheel_heater")

class TeslaWiperBladeHeaterBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Wiper Blade Heater binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_wiper_blade_heater"
        self._attr_name = "Wiper Blade Heater"
        self._attr_device_class = BinarySensorDeviceClass.HEAT

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("climate_state") or {}).get("wiper_blade_heater")

class TeslaFastChargerPresentBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Fast Charger Present binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_fast_charger_present"
        self._attr_name = "Fast Charger Present"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("charge_state") or {}).get("fast_charger_present")
