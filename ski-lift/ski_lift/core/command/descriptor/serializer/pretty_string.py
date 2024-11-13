"""Pretty string serializer."""


from dataclasses import dataclass
from string import Template
from typing import Any, Optional

from ski_lift.core.command.descriptor.object import (
    ChangeStateCommandDescriptor, CommandDescriptor,
    InsertCardCommandDescriptor)
from ski_lift.core.command.descriptor.serializer.base import \
    BaseDescriptorSerializer
from ski_lift.core.utils import class_name_to_snake


@dataclass
class PrettyDescriptorSerializerConfig:
    """Config class for pretty descriptor serializer.
    
    Attributes:
        template(str): should cover the common attributes for descriptors
        arg_template (str): generic template for extra arguments
        time_format (str): optional format for `datetime.strftime`
    """

    template: str
    arg_template: str
    time_format: str = "%Y-%m-%d %H:%M:%S"



DEFAULT_CONFIG: PrettyDescriptorSerializerConfig = PrettyDescriptorSerializerConfig(
    template='[$id:command][type:$type][time:$time][delay:$delay][user:$user]',
    arg_template='[$arg_name:$arg_value]'
)



class PrettyStringDescriptorSerializer(BaseDescriptorSerializer):
    """Pretty string descriptor serializer.
    
    Serializes commands into strings. The class itself is configurable via the
    `PrettyDescriptorSerializerConfig` dataclass.
    """

    def __init__(self, config: Optional[PrettyDescriptorSerializerConfig] = None) -> None:
        self._config = config or DEFAULT_CONFIG
        self._template: Template = Template(self._config.template)
        self._arg_template: Template = Template(self._config.arg_template)

    def process_descriptor(self, command: CommandDescriptor) -> Any:
        return super().process_descriptor(command) + '\n'

    def process_descriptor_universally(self, command: CommandDescriptor) -> str:
        return self._template.substitute(
            id=command.id,
            type=class_name_to_snake(command, to_remove='CommandDescriptor'),
            time=command.time.strftime(self._config.time_format),
            delay=command.delay,
            user=command.user_card,
        )
    
    def process_insert_card_descriptor(self, command: InsertCardCommandDescriptor) -> str:
        pretty_text: str = super().process_insert_card_descriptor(command)
        pretty_text += self._arg_template.substitute(
            arg_name='card_inserted',
            arg_value=command.card_to_insert,
        )
        return pretty_text
    
    def process_change_state_descriptor(self, command: ChangeStateCommandDescriptor) -> str:
        pretty_text: str = super().process_change_state_descriptor(command)
        pretty_text += self._arg_template.substitute(
            arg_name='new_state',
            arg_value=command.new_state.name
        )
        return pretty_text
