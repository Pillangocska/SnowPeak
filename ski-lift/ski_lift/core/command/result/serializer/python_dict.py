"""Command result python dict serializer."""

from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from ski_lift.core.utils.string_utils import class_name_to_snake


class PythonDictResultSerializer(BaseResultSerializer):

    def process_result_universally(self, result: CommandResult) -> dict:
        return {
            'id': result.command.id,
            'type': 'result',
            'kind': class_name_to_snake(result, to_remove='CommandResult'),
            'time': result.time.isoformat(),
            'user': result.command.user_card,
            'outcome': result.outcome.name,
            'exception': class_name_to_snake(result.exception)
        }
