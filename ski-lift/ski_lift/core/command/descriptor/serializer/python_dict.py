"""Command descriptor json serializer."""

from typing import Any

from ski_lift.core.command.descriptor.object import (
    ChangeStateCommandDescriptor, CommandDescriptor,
    InsertCardCommandDescriptor)
from ski_lift.core.command.descriptor.serializer.base import \
    BaseDescriptorSerializer
from ski_lift.core.utils import class_name_to_snake

from ..object import MessageReportCommandDescriptor


class PythonDictDescriptorSerializer(BaseDescriptorSerializer):

    def process_descriptor_universally(self, command: CommandDescriptor) -> dict:
        return {
            'id': command.id,
            'type': 'command',
            'kind': class_name_to_snake(command, to_remove='CommandDescriptor'),
            'time': command.time.isoformat(),
            'delay': command.delay,
            'user': command.user_card,
        }
    
    def process_insert_card_descriptor(self, command: InsertCardCommandDescriptor) -> dict:
        command_dict: dict = super().process_insert_card_descriptor(command)
        command_dict.update({'args': {'card_inserted': command.card_to_insert}})
        return command_dict
    
    def process_change_state_descriptor(self, command: ChangeStateCommandDescriptor) -> dict:
        command_dict: dict =  super().process_change_state_descriptor(command)
        command_dict.update({'args': {'new_state': command.new_state.name}})
        return command_dict
    
    def process_message_report_descriptor(self, command: MessageReportCommandDescriptor) -> Any:
        command_dict: dict =  super().process_change_state_descriptor(command)
        command_dict.update({'args': {'severity': command.severity.name, 'message': command.message}})
        return command_dict