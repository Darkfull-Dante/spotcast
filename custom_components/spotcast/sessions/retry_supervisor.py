"""Module containing a class managing the retry behavior after
internal server errors

Classes:
    - RetrySupervisor
"""

from time import time
from logging import getLogger, ERROR, DEBUG
from urllib3.exceptions import ReadTimeoutError
from aiohttp.client_exceptions import ClientOSError, ClientConnectorError

from requests.exceptions import (
    ReadTimeout,
    ConnectionError as RequestsConnError
)

from custom_components.spotcast.sessions.exceptions import (
    InternalServerError,
    UpstreamServerNotready,
)

LOGGER = getLogger(__name__)


class RetrySupervisor:
    """Supervisor for retrying attempts at connecting to an API.
    Handles clean error management and logs to appropriate levels
    according to the number of prior consecutive failed attempts

    Attributes:
        communication_count(int): number of consecutive failed attempts
        is_healthy(bool): True if currently able to communicate with
            server
        next_retry(int): timestamp when a next retry should be
            attempted

    Methods:
        failed
        log_message
    """

    SUPERVISED_EXCEPTIONS = (
        ReadTimeout,
        ReadTimeoutError,
        InternalServerError,
        UpstreamServerNotready,
        ClientConnectorError,
        ClientOSError,
        RequestsConnError,
    )

    def __init__(self):
        """Supervisor for retrying attempts at connecting to an API.
        Handles clean error management and logs to appropriate levels
        according to the number of prior consecutive failed attempts
        """
        self._is_healthy = True
        self._next_retry = 0
        self.communication_counter = 0

    @property
    def is_healthy(self) -> bool:
        """Returns the health state of the session"""
        return self._is_healthy

    @is_healthy.setter
    def is_healthy(self, value: bool):
        self._is_healthy = value

        if self._is_healthy:
            self._next_retry = 0
            self.communication_counter = 0
        else:
            self.failed()

    @property
    def next_retry(self) -> int:
        """Return the time stamp when it will be ok to retry
        communicating with the upstream server"""
        return self._next_retry

    @property
    def is_ready(self) -> bool:
        """Returns True if the up stream is ready to reattemp a
        connection. Based on a retry delay of 30 seconds"""
        return time() > self.next_retry

    def failed(self):
        """Updates the next_retry time because the connection failed
        """
        self._next_retry = time() + 30

    def log_message(self, msg: str):
        """Logs a message to the logger. Sends as an Error level on the
        first and debug on subsequent messages"""
        level = DEBUG if self.communication_counter > 0 else ERROR
        LOGGER.log(level, msg)
        self.communication_counter += 1
