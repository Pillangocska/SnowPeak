"""Command result python dict serializer."""

from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from core.utils.string_utils import class_name_to_snake


class PythonDictDescriptorSerializer(BaseResultSerializer):

    def process_result_universally(self, result: CommandResult) -> dict:
        return {
            'id': result.command.id,
            'time': result.time.isoformat(),
            'user': result.command.user_card,
            'outcome': result.outcome.name,
            'exception': class_name_to_snake(result.exception)
        }
