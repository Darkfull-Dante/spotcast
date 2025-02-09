"""Module for the abstract SpotcastSensor class"""

from logging import getLogger
from typing import final, override

from homeassistant.components.sensor import (
    SensorStateClass,
    SensorEntity,
)

# imports for object availability
from homeassistant.components.sensor import (  # pylint: disable=W0611
    SensorEntityDescription,
    EntityCategory,
    SensorDeviceClass,

)

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.sensor.abstract_entity import SpotcastEntity

LOGGER = getLogger(__name__)


class SpotcastSensor(SpotcastEntity, SensorEntity):
    """A child abstract class of the `SpotcastEntity` for Sensor
    entities

    Constants:
        - PLATFORM(str, optional): Seys the platform of the entities
            to `sensor`
        - UNITS_OF_MEASURE(str, optional): The units of masure used
            by a sensor. Defaults to None, when no measurements.

    Properties:
        - units_of_measurement(str): the units of measurement used by
            the sensor.
        - state(str|int|float): return the current state of the sensor
        - icon(str): the icon of the instance. Icon is based on `ICON`.
            The inactive icon is shown when sate is inactive or equal
            to 0 (zero) when numeric state
    """

    PLATFORM = "sensor"
    UNITS_OF_MEASURE: str = None
    STATE_CLASS: str = SensorStateClass.MEASUREMENT

    def __init__(self, account: SpotifyAccount):
        self._attr_state_class = self.STATE_CLASS
        self._sensor_option_unit_of_measurement = self.UNITS_OF_MEASURE
        super().__init__(account)

    @final
    @property
    @override
    def unit_of_measurement(self) -> str:  # pylint: disable=W0239
        """Returns the units measured by the sensor"""
        return self.UNITS_OF_MEASURE

    @final
    @property
    @override
    def state(self) -> str | int | float:  # pylint: disable=W0239
        """Returns the currently saved state of the sensor"""
        return self._attr_state

    @property
    def icon(self) -> str:
        """Sets the icon of the entity"""

        state = self._attr_state
        if (
            isinstance(state, str) and state != self.INACTIVE_STATE
            or isinstance(state, (int, float)) and state > 0
        ):
            return self.ICON

        return self._icon_off

    @property
    def _default_attributes(self) -> dict:
        """Reconstructors default attributes. If no attributes exist
        for the sensor. None is returned"""
        return None
