"""Command result json serializer."""

from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.command.result.serializer.python_dict import PythonDictResultSerializer
from camel_converter import dict_to_camel
import json



class JSONBytesResultSerializer(PythonDictResultSerializer):
    
    def __init__(self, convert_to_camel: bool = True) -> None:
        self._convert_to_camel: bool = convert_to_camel

    def serialize(self, result: CommandResult) -> bytes:
        command_dict: dict = super().serialize(result)
        if self._convert_to_camel:
            command_dict = dict_to_camel(command_dict)
        return json.dumps(command_dict).encode('utf-8')
