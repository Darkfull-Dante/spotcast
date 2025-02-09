"""Module for all CurrentTrackFeatures

Classes:
"""

from logging import getLogger
from typing import Any

from homeassistant.const import STATE_UNKNOWN

from custom_components.spotcast.sensor.abstract_sensor import (
    SpotcastSensor,
    SensorStateClass,
    SensorDeviceClass,
)

LOGGER = getLogger(__name__)


class AbstractAudioFeatureSensor(SpotcastSensor):
    """A Home Assistant sensor reporting audio feature information

    Methods:
        - async_update
    """

    STATE_CLASS: str = SensorStateClass.MEASUREMENT
    FEATURE_NAME = "abstract"

    @property
    def _generic_id(self) -> str:
        return f"current_track_{self.FEATURE_NAME}"

    @property
    def name(self) -> str:
        feature = self.FEATURE_NAME.replace("_", " ")
        feature = [x.capitalize() for x in feature.split(" ")]
        feature = " ".join(feature)
        return f"Spotcast - {self.account.name} Current Track {feature}"

    def _cleanup(self, feature: Any) -> Any:
        return feature

    async def _async_update_process(self):
        audio_features = self.account.current_item["audio_features"]
        audio_feature = audio_features.get(self.FEATURE_NAME)

        if audio_feature is None:
            self._attr_state = STATE_UNKNOWN
        else:
            self._attr_state = self._cleanup(audio_feature)


class AbstractPercentSensor(AbstractAudioFeatureSensor):
    """A Home Assistant sensor reporting a percentage value"""
    UNITS_OF_MEASURE = "%"
    _attr_suggested_display_precision = 1

    def _cleanup(self, feature: float) -> float:
        return feature * 100


class CurrentTrackDanceabilitySensor(AbstractPercentSensor):
    """A Home Assistant sensor reporting the danceability percentage of
    a song"""
    FEATURE_NAME = "danceability"
    ICON = "mdi:dance-ballroom"


class CurrentTrackEnergySensor(AbstractPercentSensor):
    """A Home Assistant sensor reporting the percentage of energy of
    the song"""
    FEATURE_NAME = "energy"
    ICON = "mdi:lightning-bolt"


class CurrentTrackKeySensor(AbstractAudioFeatureSensor):
    """A Home Assistant sensor reporting the key the song is in"""
    FEATURE_NAME = "key"
    STATE_CLASS = None
    ICON = "mdi:language-csharp"
    KEYS = (
        "C",
        "C#/D♭",
        "D",
        "D#/E♭",
        "E",
        "F",
        "F#/G♭",
        "G",
        "G#/A♭",
        "A",
        "A#/B♭",
        "B",
    )

    def _cleanup(self, feature: int) -> str:

        if 0 <= feature < len(self.KEYS):
            return self.KEYS[feature]

        return "-"


class CurrentTrackLoudnessSensor(AbstractAudioFeatureSensor):
    """A Home Assistant sensor reporting the loudness of the song in
    decibel"""
    FEATURE_NAME = "loudness"
    UNITS_OF_MEASURE = "dB"
    ICON = "mdi:bullhorn"
    _attr_suggested_display_precision = 1

    @property
    def device_class(self) -> SensorDeviceClass:
        return SensorDeviceClass.SOUND_PRESSURE

    @property
    def icon(self) -> str:
        if not isinstance(self._attr_state, (float, int)):
            return "mdi:volume-off"

        if self._attr_state < -40:
            return "mdi:volume-low"

        if self._attr_state < -20:
            return "mdi:volume-medium"

        return "mdi:volume-high"


class CurrentTrackModeSensor(AbstractAudioFeatureSensor):
    """A Home Assistant sensor reporting the mode the song is in"""
    FEATURE_NAME = "mode"
    STATE_CLASS = None
    ICON = "mdi:music"

    def _cleanup(self, feature: int) -> str:
        return "major" if feature == 1 else "minor"


class CurrentTrackSpeechinessSensor(AbstractPercentSensor):
    """A Home Assistant sensor reporting the percentage of speechiness
    of the current song as a percentage"""
    FEATURE_NAME = "speechiness"
    ICON = "mdi:speaker-message"


class CurrentTrackAcousticnessSensor(AbstractPercentSensor):
    """A Home Assistant sensor reporting the level of acousticness of
    the current song"""
    FEATURE_NAME = "acousticness"
    ICON = "mdi:guitar-acoustic"

    @property
    def icon(self) -> str:
        if not isinstance(self._attr_state, float) or self._attr_state > 50:
            return "mdi:guitar-acoustic"

        return "mdi:guitar-electric"


class CurrentTrackInstrumentalnessSensor(AbstractPercentSensor):
    """A Home Assistant sensor reporting the level of instrumentalness
    of the current song as a percentage"""
    FEATURE_NAME = "instrumentalness"
    ICON = "mdi:piano"


class CurrentTrackLivenessSensor(AbstractPercentSensor):
    """A Home Assistant sensor reporting the likelyhood the song is
    live as a percentage"""
    FEATURE_NAME = "liveness"
    ICON = "mdi:account-group"


class CurrentTrackValenceSensor(AbstractPercentSensor):
    """A Home Assistant sensor reporting the valence (happy vs. sad)
    feel of the current song as a percentage. `0` being sad and `100`
    being happy"""
    FEATURE_NAME = "valence"
    ICON = "mdi:emoticon"

    @property
    def icon(self) -> str:
        if not isinstance(self._attr_state, float):
            return "mdi:emoticon-outline"

        if self._attr_state < 20:
            return "mdi:emoticon-cry"
        if self._attr_state < 40:
            return "mdi:emoticon-sad"
        if self._attr_state < 60:
            return "mdi:emoticon-neutral"
        if self._attr_state < 80:
            return "mdi:emoticon-happy"

        return "mdi:emoticon-excited"


class CurrentTrackTempoSensor(AbstractAudioFeatureSensor):
    """A Home Asssistant sensor reporting the tempo of a song in beats
    per minute"""
    FEATURE_NAME = "tempo"
    UNITS_OF_MEASURE = "bpm"
    ICON = "mdi:metronome"
    _attr_suggested_display_precision = 0


class CurrentTrackTimeSignatureSensor(AbstractAudioFeatureSensor):
    """A Home Assistant sensor reporting the time signature of the song
    as its fractional time signature"""
    FEATURE_NAME = "time_signature"
    STATE_CLASS = None
    ICON = "mdi:music-clef-treble"

    def _cleanup(self, feature: int) -> str:
        return f"{feature}/4"


SENSORS = (
    CurrentTrackDanceabilitySensor,
    CurrentTrackEnergySensor,
    CurrentTrackKeySensor,
    CurrentTrackLoudnessSensor,
    CurrentTrackModeSensor,
    CurrentTrackSpeechinessSensor,
    CurrentTrackAcousticnessSensor,
    CurrentTrackInstrumentalnessSensor,
    CurrentTrackLivenessSensor,
    CurrentTrackValenceSensor,
    CurrentTrackTempoSensor,
    CurrentTrackTimeSignatureSensor
)
