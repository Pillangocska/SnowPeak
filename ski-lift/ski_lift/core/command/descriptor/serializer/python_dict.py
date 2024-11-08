"""Command descriptor json serializer."""

from ski_lift.core.command.descriptor.object import CommandDescriptor, InsertCardCommandDescriptor, ChangeStateCommandDescriptor
from ski_lift.core.command.descriptor.serializer.base import BaseDescriptorSerializer
from core.utils.string_utils import class_name_to_snake


class PythonDictDescriptorSerializer(BaseDescriptorSerializer):

    def process_descriptor_universally(self, command: CommandDescriptor) -> dict:
        return {
            'id': command.id,
            'type': class_name_to_snake(command),
            'time': command.time.isoformat(),
            'delay': command.delay,
            'user': command.user_card,
        }
    
    def process_insert_card_descriptor(self, command: InsertCardCommandDescriptor) -> dict:
        command_dict: dict = super().process_insert_card_descriptor(command)
        command_dict.update({'card_inserted': command.card_to_insert})
        return command_dict
    
    def process_change_state_descriptor(self, command: ChangeStateCommandDescriptor) -> dict:
        command_dict: dict =  super().process_change_state_descriptor(command)
        command_dict.update({'new_state': command.new_state.name})
        return command_dict