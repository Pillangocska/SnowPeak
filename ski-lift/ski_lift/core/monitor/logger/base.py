"""Base command logger."""


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


class BaseCommandLogger(CommandResultMonitor):
    """Base command logger.
    
    This specialized command result monitor can be attached to a Controller to
    log its commands and their results to a specified destination.

    It utilizes a result serializer that can be invoked via the
    `serialize_result` function.
    """


    def __init__(self, result_serializer: BaseResultSerializer) -> None:
        self._result_serializer = result_serializer

    def attach_to(self, controller: 'Controller') -> None:
        controller.register_result_monitor(self)

    def serialize_result(self, result: CommandResult) -> Any:
        return self._result_serializer.serialize(result)
