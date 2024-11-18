"""Command descriptor json serializer."""

import json

from camel_converter import dict_to_camel

from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.descriptor.serializer.python_dict import \
    PythonDictDescriptorSerializer


class JSONBytesDescriptorSerializer(PythonDictDescriptorSerializer):
    """JSON bytes descriptor serializer.
    
    This is a special serializer which can serialize commands into json
    byte strings.

    By default the serializer converts key values into camel case
    (from snake case).
    """
    
    def __init__(self, convert_to_camel: bool = True) -> None:
        self._convert_to_camel: bool = convert_to_camel

    def serialize(self, command: CommandDescriptor) -> bytes:
        command_dict: dict = super().serialize(command)
        if self._convert_to_camel:
            command_dict = dict_to_camel(command_dict)
        return json.dumps(command_dict).encode('utf-8')
