"""Command result python dict serializer."""

from typing import Any

from ski_lift.core.command.result.object import (AbortCommandResult,
                                                 ChangeStateCommandResult,
                                                 CommandResult,
                                                 InsertCardCommandResult,
                                                 MessageReportCommandResult)
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from ski_lift.core.utils import class_name_to_snake


class PythonDictResultSerializer(BaseResultSerializer):
    """Python dict descriptor serializer.
    
    This is the default implementation that converts command descriptors
    into python dicts.

    This serializer was created specifically to match the structure of the
    rabbitMQ messages discussed previously.
    """

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

    def process_message_report_result(self, result: MessageReportCommandResult) -> Any:
        result_dict: dict = super().process_abort_command_result(result)
        result_dict['args'] = {
            'severity': result.command.severity.name,
            'message': result.command.message,
        }
        return result_dict