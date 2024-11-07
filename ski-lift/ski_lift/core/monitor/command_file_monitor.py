"""Command file monitor."""


from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.monitor.descriptor.descriptor_monitor import CommandDescriptorMonitor
from ski_lift.core.monitor.result.result_monitor import CommandResultMonitor
from datetime import datetime
from ski_lift.core.command.descriptor.serializer.pretty_string import PrettyStringDescriptorSerializer
from ski_lift.core.command.result.serializer.pretty_string import PrettyResultStringSerializer
import os


class CommandFileMonitor(CommandDescriptorMonitor, CommandResultMonitor):
    """Command file monitor.

    Monitor command execution and results into a log file.
    """

    def __init__(self):
        self._init_time = datetime.now()
        os.makedirs('logs', exist_ok=True)
        self._descriptor_serializer = PrettyStringDescriptorSerializer()
        self._result_serializer = PrettyResultStringSerializer()

    @property
    def file_name(self) -> str:
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, f'commands-{self._init_time.strftime("%Y-%m-%d_%H-%M-%S")}.log')

    def process_descriptor_universally(self, command: CommandDescriptor) -> None:
        with open(self.file_name, 'a') as log_file:
            log_file.write(self._descriptor_serializer.serialize(command))

    def process_result_universally(self, result: CommandResult) -> None:
        with open(self.file_name, 'a') as log_file:
            log_file.write(self._result_serializer.serialize(result))
