"""Remote communicator implementation."""

import random
from abc import ABC, abstractmethod
from random import random
from threading import Event, Thread
from time import sleep
from typing import TYPE_CHECKING

from ski_lift.core.command.descriptor.object import \
    MessageReportCommandDescriptor

if TYPE_CHECKING:
    from ski_lift.core.controller import Controller


class RemoteCommunicator(ABC):
    """Remote communicator.
    
    This is an abstract class that represents a communicator, which can be used
    to send both on-demand and periodic messages to the remote control center
    with the master operators.

    Currently the supported messages are the periodic status updates about the
    lift and the report messages initiated by the worker operator.

    By default the status updates are sent every 5 seconds.
    """

    def __init__(self, status_update_interval: int = 5) -> None:
        self._controller: Controller = None
        self._status_update_interval: int = status_update_interval
        self._thread: Thread = None
        self._stop_event: Event = None 

    def __enter__(self):
        """Needed for `with` keyword support."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Needed for `with` keyword support."""
        self.stop()
        return False

    @property
    def lift_id(self) -> str:
        if self._controller is not None:
            return self._controller.lift_id

    def set_controller(self, controller: 'Controller') -> None:
        self._controller = controller

    def start(self) -> None:
        if self._thread is None:
            self._stop_event = Event()
            self._thread = Thread(target=self.status_update_loop)
            self._thread.start()

    def stop(self) -> None:
        if self._thread is not None and self._stop_event is not None:
            self._stop_event.set()
            self._thread.join()
            self._thread = None
            self._stop_event = None
            

    def status_update_loop(self) -> None:
        # randomize start time so the lifts
        # wont send data at the exact same time
        sleep(random.randint(0, self._status_update_interval))
        while not self._stop_event.is_set():
            self.send_status_update()
            sleep(self._status_update_interval)

    @abstractmethod
    def send_message_report(self, report: MessageReportCommandDescriptor):
        """Send a message report the remote control centre."""

    
    @abstractmethod
    def send_status_update(self) -> None:
        """Send a status update to the remote control centre."""
