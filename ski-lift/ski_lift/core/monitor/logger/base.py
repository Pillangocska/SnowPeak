"""Command file monitor."""


from typing import TYPE_CHECKING, Any

from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.descriptor.serializer.base import \
    BaseDescriptorSerializer
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from ski_lift.core.monitor.descriptor.descriptor_monitor import \
    CommandDescriptorMonitor
from ski_lift.core.monitor.result.result_monitor import CommandResultMonitor

if TYPE_CHECKING:
    from ski_lift.core.controller import Controller


class BaseCommandLogger(CommandDescriptorMonitor, CommandResultMonitor):

    def __init__(
        self,
        descriptor_serializer: BaseDescriptorSerializer,
        result_serializer: BaseResultSerializer,
    ) -> None:
        self._descriptor_serializer = descriptor_serializer
        self._result_serializer = result_serializer

    def attach_to(self, controller: 'Controller') -> None:
        controller.register_descriptor_monitor(self)
        controller.register_result_monitor(self)

    def serialize_command(self, command: CommandDescriptor) -> Any:
        return self._descriptor_serializer.serialize(command)
    
    def serialize_result(self, result: CommandResult) -> Any:
        return self._result_serializer.serialize(result)
