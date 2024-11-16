"""Remote emergency stop handler."""

from abc import abstractmethod
from ski_lift.core.view.base_view import BaseView


class RemoteEmergencyStopHandler(object):

    def __init__(self, view: BaseView) -> None:
        self._view: BaseView = view

    def __enter__(self):
        self.start_handling_remote_emergency_stops()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.stop_handling_remote_emergency_stops()
        return False

    @abstractmethod
    def start_handling_remote_emergency_stops(self) -> None:
        """Start handling remote emergency stops."""

    @abstractmethod
    def stop_handling_remote_emergency_stops(self) -> None:
        """Stop handling remote emergency stops."""
