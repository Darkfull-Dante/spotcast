"""Module containing the chromecast media player implementation"""

from logging import getLogger
from hashlib import md5

from pychromecast import Chromecast as ParentChromecast

from custom_components.spotcast.media_player._abstract_player import (
    MediaPlayer
)


LOGGER = getLogger(__name__)


class Chromecast(ParentChromecast, MediaPlayer):
    """A chromecast media player

    Constants:
        - PLATFORM(str): the Home Assistant platform hosting the
            devices
        - DEVICE_TYPE(type): the type of device searched for

    Properties:
        - id: the spotify device if for the player

    functions:
        - from_hass
        - from_network
    """

    INTEGRATION = "cast"

    @property
    def id(self) -> str:
        """Returns the spotify id of the player"""
        return md5(self.name.encode()).hexdigest()
