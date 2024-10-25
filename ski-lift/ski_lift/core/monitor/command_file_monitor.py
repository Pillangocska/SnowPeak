"""Command file monitor."""


from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.monitor.descriptor.descriptor_monitor import CommandDescriptorMonitor
from ski_lift.core.monitor.result.result_monitor import CommandResultMonitor
from datetime import datetime
import os


class CommandFileMonitor(CommandDescriptorMonitor, CommandResultMonitor):
    """Command file monitor.
    
    Monitor command execution and results into a log file.
    """

    def __init__(self):
        self._init_time = datetime.now()
        os.makedirs('logs', exist_ok=True)

    @property
    def file_name(self) -> str:
        return f'logs/commands-{self._init_time.strftime('%Y-%m-%d-%H:%M:%S')}.log'

    def process_descriptor_universally(self, command: CommandDescriptor) -> None:
        with open(self.file_name, 'a') as log_file:
            log_file.write(f'[time:{command.time}] [type: command request] [kind:{command.__class__.__name__}] [command_id:{command.id}] [user:{command.user_card}]\n')

    def process_result_universally(self, result: CommandResult) -> None:
        with open(self.file_name, 'a') as log_file:
            log_file.write(f'[time:{result.command.time}] [type:command result] [command_id:{result.command.id}] [outcome:{result.outcome.name}] [exception:{result.exception.__class__.__name__}]\n')
