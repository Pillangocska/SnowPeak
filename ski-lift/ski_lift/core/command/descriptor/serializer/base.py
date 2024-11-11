"""Command descriptor serializer."""


from ski_lift.core.command.descriptor.processor import DescriptorProcessor
from ski_lift.core.command.descriptor.object import CommandDescriptor
from typing import Any


class BaseDescriptorSerializer(DescriptorProcessor):
    """Base descriptor serializer.
    
    This is a special `DescriptorProcessor` which can serialize
    `CommandDescriptors` into a specified format (eg. JSON).

    The `serializer` function only exists to make a more fitting name for the
    context. The base `process_descriptor` function could have been used as
    well.
    """

    def serialize(self, command: CommandDescriptor) -> Any:
        return self.process_descriptor(command)
