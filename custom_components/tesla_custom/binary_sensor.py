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
        TeslaDriverFrontDoorBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaDriverRearDoorBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaPassengerFrontDoorBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaPassengerRearDoorBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaFrontTrunkBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaRearTrunkBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaFrontDefrosterBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaRearDefrosterBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaSideMirrorHeatersBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaIsPreconditioningBinarySensor(coordinator, vehicle_id, vehicle_info),
        TeslaScheduledChargingPendingBinarySensor(coordinator, vehicle_id, vehicle_info),
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

class TeslaDriverFrontDoorBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Driver Front Door binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_driver_front_door"
        self._attr_name = "Driver Front Door"
        self._attr_device_class = BinarySensorDeviceClass.DOOR

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("df")

class TeslaDriverRearDoorBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Driver Rear Door binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_driver_rear_door"
        self._attr_name = "Driver Rear Door"
        self._attr_device_class = BinarySensorDeviceClass.DOOR

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("dr")

class TeslaPassengerFrontDoorBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Passenger Front Door binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_passenger_front_door"
        self._attr_name = "Passenger Front Door"
        self._attr_device_class = BinarySensorDeviceClass.DOOR

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("pf")

class TeslaPassengerRearDoorBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Passenger Rear Door binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_passenger_rear_door"
        self._attr_name = "Passenger Rear Door"
        self._attr_device_class = BinarySensorDeviceClass.DOOR

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("pr")

class TeslaFrontTrunkBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Front Trunk binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_front_trunk"
        self._attr_name = "Front Trunk"
        self._attr_device_class = BinarySensorDeviceClass.DOOR

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("ft")

class TeslaRearTrunkBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Rear Trunk binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_rear_trunk"
        self._attr_name = "Rear Trunk"
        self._attr_device_class = BinarySensorDeviceClass.DOOR

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("vehicle_state") or {}).get("rt")

class TeslaFrontDefrosterBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Front Defroster binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_front_defroster"
        self._attr_name = "Front Defroster"
        self._attr_device_class = BinarySensorDeviceClass.HEAT

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("climate_state") or {}).get("is_front_defroster_on")

class TeslaRearDefrosterBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Rear Defroster binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_rear_defroster"
        self._attr_name = "Rear Defroster"
        self._attr_device_class = BinarySensorDeviceClass.HEAT

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("climate_state") or {}).get("is_rear_defroster_on")

class TeslaSideMirrorHeatersBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Side Mirror Heaters binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_side_mirror_heaters"
        self._attr_name = "Side Mirror Heaters"
        self._attr_device_class = BinarySensorDeviceClass.HEAT

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("climate_state") or {}).get("side_mirror_heaters")

class TeslaIsPreconditioningBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Is Preconditioning binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_is_preconditioning"
        self._attr_name = "Preconditioning"
        self._attr_device_class = BinarySensorDeviceClass.RUNNING

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("climate_state") or {}).get("is_preconditioning")

class TeslaScheduledChargingPendingBinarySensor(TeslaBaseEntity, BinarySensorEntity):
    """Scheduled Charging Pending binary sensor."""
    
    def __init__(self, coordinator, vehicle_id, vehicle_info):
        """Init."""
        super().__init__(coordinator, vehicle_id, vehicle_info)
        self._attr_unique_id = f"{vehicle_id}_scheduled_charging_pending"
        self._attr_name = "Scheduled Charging Pending"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        return (self.coordinator.data.get("charge_state") or {}).get("scheduled_charging_pending")
