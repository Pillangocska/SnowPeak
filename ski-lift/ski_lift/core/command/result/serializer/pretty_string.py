"""Pretty string serializer."""


from dataclasses import dataclass
from typing import Optional

from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from string import Template
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.utils.string_utils import class_name_to_snake


@dataclass
class PrettyResultSerializerConfig:
    """Config class for pretty descriptor serializer.
    
    Attributes:
        template(str): should cover the common attributes for descriptors
        arg_template (str): generic template for extra arguments
        time_format (str): optional format for `datetime.strftime`
    """

    template: str
    arg_template: str
    time_format: str = "%Y-%m-%d %H:%M:%S"



DEFAULT_CONFIG: PrettyResultSerializerConfig = PrettyResultSerializerConfig(
    template='[$id:result][time:$time][user:$user][outcome:$outcome][exception:$exception]',
    arg_template='[$arg_name:$arg_value]'
)



class PrettyResultStringSerializer(BaseResultSerializer):
    """Pretty string result serializer.
    
    Serializes results into strings. The class itself is configurable via the
    `PrettyResultSerializerConfig` dataclass.
    """

    def __init__(self, config: Optional[PrettyResultSerializerConfig] = None) -> None:
        self._config = config or DEFAULT_CONFIG
        self._template: Template = Template(self._config.template)
        self._arg_template: Template = Template(self._config.arg_template)

    def process_result(self, result: CommandResult) -> str:
        return super().process_result(result) + '\n'

    def process_result_universally(self, result: CommandResult) -> str:
        return self._template.substitute(
            id=result.command.id,
            time=result.time.strftime(self._config.time_format),
            user=result.command.user_card,
            outcome=result.outcome.name,
            exception=class_name_to_snake(result.exception),
        )
