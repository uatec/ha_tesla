"""Sensor platform for Tesla Custom."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature, UnitOfLength
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    vehicle_id = data["vehicle_id"]
    vehicle_info = data["vehicle_info"]

    sensors = [
        TeslaBatterySensor(coordinator, vehicle_id, vehicle_info),
        TeslaRangeSensor(coordinator, vehicle_id, vehicle_info),
        TeslaInsideTempSensor(coordinator, vehicle_id, vehicle_info),
        TeslaOutsideTempSensor(coordinator, vehicle_id, vehicle_info),
        TeslaOdometerSensor(coordinator, vehicle_id, vehicle_info),
        TeslaStateSensor(coordinator, vehicle_id, vehicle_info),
    ]
    async_add_entities(sensors)

class TeslaBaseEntity(CoordinatorEntity):
    """Base class for Tesla entities."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Initialize the entity."""
        super().__init__(coordinator)
        self.vehicle_id = vehicle_id
        self.vehicle_info = vehicle_info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self.vehicle_id)},
            "name": self.vehicle_info.get("display_name", "Tesla"),
            "manufacturer": "Tesla",
            "model": "Vehicle",
        }

class TeslaBatterySensor(TeslaBaseEntity, SensorEntity):
    """Battery level sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_battery"
        self._attr_name = "Battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("charge_state", {}).get("battery_level")

class TeslaRangeSensor(TeslaBaseEntity, SensorEntity):
    """Range sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_range"
        self._attr_name = "Ideal Range"
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_native_unit_of_measurement = UnitOfLength.MILES

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("charge_state", {}).get("ideal_battery_range")

class TeslaInsideTempSensor(TeslaBaseEntity, SensorEntity):
    """Inside temperature sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_inside_temp"
        self._attr_name = "Inside Temperature"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("climate_state", {}).get("inside_temp")

class TeslaOutsideTempSensor(TeslaBaseEntity, SensorEntity):
    """Outside temperature sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_outside_temp"
        self._attr_name = "Outside Temperature"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("climate_state", {}).get("outside_temp")

class TeslaOdometerSensor(TeslaBaseEntity, SensorEntity):
    """Odometer sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_odometer"
        self._attr_name = "Odometer"
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_native_unit_of_measurement = UnitOfLength.MILES

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("vehicle_state", {}).get("odometer")

class TeslaStateSensor(TeslaBaseEntity, SensorEntity):
    """State sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_state"
        self._attr_name = "State"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("state")
