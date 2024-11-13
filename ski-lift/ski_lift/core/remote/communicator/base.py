"""Remote communicator implementation."""

from abc import ABC, abstractmethod
from ski_lift.core.command.descriptor.object import MessageReportCommandDescriptor


class RemoteCommunicator(ABC):
    """Remote communicator.
    
    This class is responsible for sending on demand messages to the control
    center.
    """

    @abstractmethod
    def send_message_report(self, report: MessageReportCommandDescriptor):
        """Send a message report the control centrum."""
