"""Command file monitor."""


from ski_lift.core.monitor.logger.base import BaseCommandLogger
from datetime import datetime
from ski_lift.core.command.descriptor.serializer.base import BaseDescriptorSerializer
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
import os
from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.result.object import CommandResult



class FileCommandLogger(BaseCommandLogger):
    """Command file monitor.

    Monitor command execution and results into a log file.
    """

    def __init__(
        self,
        descriptor_serializer: BaseDescriptorSerializer,
        result_serializer: BaseResultSerializer,
    ) -> None:
        self._init_time = datetime.now()
        os.makedirs('logs', exist_ok=True)
        super().__init__(descriptor_serializer=descriptor_serializer, result_serializer=result_serializer)

    @property
    def file_name(self) -> str:
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, f'commands-{self._init_time.strftime("%Y-%m-%d_%H-%M-%S")}.log')

    def process_descriptor_universally(self, command: CommandDescriptor) -> None:
        with open(self.file_name, 'a') as log_file:
            log_file.write(self.serialize_command(command))

    def process_result_universally(self, result: CommandResult) -> None:
        with open(self.file_name, 'a') as log_file:
            log_file.write(self.serialize_result(result))
