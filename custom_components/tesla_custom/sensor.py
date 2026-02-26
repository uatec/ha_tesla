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
        TeslaSpeedSensor(coordinator, vehicle_id, vehicle_info),
        TeslaPowerSensor(coordinator, vehicle_id, vehicle_info),
        TeslaChargeRateSensor(coordinator, vehicle_id, vehicle_info),
        TeslaEnergyAddedSensor(coordinator, vehicle_id, vehicle_info),
        TeslaTimeToFullSensor(coordinator, vehicle_id, vehicle_info),
        TeslaHeadingSensor(coordinator, vehicle_id, vehicle_info),
        TeslaShiftStateSensor(coordinator, vehicle_id, vehicle_info),
        TeslaSoftwareVersionSensor(coordinator, vehicle_id, vehicle_info),
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
        return (self.coordinator.data.get("charge_state") or {}).get("battery_level")

class TeslaRangeSensor(TeslaBaseEntity, SensorEntity):
    """Range sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_range"
        self._attr_name = "Ideal Range"
        self._attr_device_class = SensorDeviceClass.DISTANCE
        gui = coordinator.data.get("gui_settings", {}) if self.coordinator.data else {}
        dist_units = gui.get("gui_distance_units", "mi/hr")
        self._attr_native_unit_of_measurement = UnitOfLength.KILOMETERS if "km" in dist_units.lower() else UnitOfLength.MILES

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("charge_state") or {}).get("ideal_battery_range") or 0.0

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
        return (self.coordinator.data.get("climate_state") or {}).get("inside_temp")

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
        return (self.coordinator.data.get("climate_state") or {}).get("outside_temp")

class TeslaOdometerSensor(TeslaBaseEntity, SensorEntity):
    """Odometer sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_odometer"
        self._attr_name = "Odometer"
        self._attr_device_class = SensorDeviceClass.DISTANCE
        gui = coordinator.data.get("gui_settings", {}) if self.coordinator.data else {}
        dist_units = gui.get("gui_distance_units", "mi/hr")
        self._attr_native_unit_of_measurement = UnitOfLength.KILOMETERS if "km" in dist_units.lower() else UnitOfLength.MILES

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("odometer") or 0.0

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

class TeslaSpeedSensor(TeslaBaseEntity, SensorEntity):
    """Speed sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_speed"
        self._attr_name = "Speed"
        self._attr_device_class = SensorDeviceClass.SPEED
        gui = coordinator.data.get("gui_settings", {}) if self.coordinator.data else {}
        dist_units = gui.get("gui_distance_units", "mi/hr")
        self._attr_native_unit_of_measurement = "km/h" if "km" in dist_units.lower() else "mph"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("drive_state") or {}).get("speed") or 0

class TeslaPowerSensor(TeslaBaseEntity, SensorEntity):
    """Power sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_power"
        self._attr_name = "Power"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_native_unit_of_measurement = "kW"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        power = (self.coordinator.data.get("drive_state") or {}).get("power")
        if not power:
            power = (self.coordinator.data.get("charge_state") or {}).get("charger_power", 0)
        return power or 0

class TeslaChargeRateSensor(TeslaBaseEntity, SensorEntity):
    """Charge Rate sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_charge_rate"
        self._attr_name = "Charge Rate"
        self._attr_native_unit_of_measurement = "mi/hr"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("charge_state") or {}).get("charge_rate")

class TeslaEnergyAddedSensor(TeslaBaseEntity, SensorEntity):
    """Energy Added sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_energy_added"
        self._attr_name = "Energy Added"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_native_unit_of_measurement = "kWh"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("charge_state") or {}).get("charge_energy_added")

class TeslaTimeToFullSensor(TeslaBaseEntity, SensorEntity):
    """Time to Full Charge sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_time_to_full"
        self._attr_name = "Time to Full Charge"
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_native_unit_of_measurement = "h"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("charge_state") or {}).get("time_to_full_charge")

class TeslaHeadingSensor(TeslaBaseEntity, SensorEntity):
    """Heading sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_heading"
        self._attr_name = "Heading"
        self._attr_native_unit_of_measurement = "°"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("drive_state") or {}).get("heading") or 0

class TeslaShiftStateSensor(TeslaBaseEntity, SensorEntity):
    """Shift State sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_shift_state"
        self._attr_name = "Shift State"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("drive_state") or {}).get("shift_state") or "P"

class TeslaSoftwareVersionSensor(TeslaBaseEntity, SensorEntity):
    """Software version sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_software_version"
        self._attr_name = "Software Version"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("car_version")
