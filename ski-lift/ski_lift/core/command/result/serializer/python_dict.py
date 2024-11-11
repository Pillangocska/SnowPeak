"""Command result python dict serializer."""

from ..object import AbortCommandResult

from ..object import ChangeStateCommandResult
from ..object import InsertCardCommandResult
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from ski_lift.core.utils.string_utils import class_name_to_snake


class PythonDictResultSerializer(BaseResultSerializer):

    def process_result_universally(self, result: CommandResult) -> dict:
        return {
            'messageKind': 'command',
            'type': class_name_to_snake(result, to_remove='CommandResult'),
            'timestamp': result.time.isoformat(),
            'user': result.command.user_card,
            'outcome': result.outcome.name,
            'exception': class_name_to_snake(result.exception).upper(),
        }
    
    def process_insert_card_result(self, result: InsertCardCommandResult) -> dict:
        result_dict: dict = super().process_insert_card_result(result)
        result_dict['args'] = {'card_inserted': result.command.card_to_insert}
        return result_dict
    
    def process_change_state_result(self, result: ChangeStateCommandResult) -> dict:
        result_dict: dict = super().process_change_state_result(result)
        result_dict['args'] = {'new_state': result.command.new_state.name}
        return result_dict
    
    def process_abort_command_result(self, result: AbortCommandResult) -> dict:
        result_dict: dict = super().process_abort_command_result(result)
        result_dict['args'] = {'command_to_abort': result.command.command_to_abort}
        return result_dict
