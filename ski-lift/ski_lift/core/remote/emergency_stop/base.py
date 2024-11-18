"""Remote emergency stop handler."""

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ski_lift.core.view.base_view import BaseView


class RemoteEmergencyStopHandler(object):
    """Remote emergency stop handler.
    
    This is an abstract class representing a consumer that waits for remote
    emergency stop signals and executes them on the controller through the
    view. It is necessary because the messages need to be displayed to users,
    allowing them the option to cancel the actions.
    """

    def __init__(self, view: 'BaseView') -> None:
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
