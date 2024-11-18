"""Command result descriptor serializer."""


from typing import Any

from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.command.result.processor import ResultProcessor


class BaseResultSerializer(ResultProcessor):
    """Base result serializer.
    
    This is a special `ResultProcessor` which can serialize
    `CommandResult` into a specified format (eg. JSON).

    The `serializer` function only exists to make a more fitting name for the
    context. The base `process_descriptor` function could have been used as
    well.
    """

    def serialize(self, result: CommandResult) -> Any:
        """Serializer the result into a specified format."""
        return self.process_result(result)
