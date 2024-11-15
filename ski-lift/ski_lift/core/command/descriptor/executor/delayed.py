

import time
from threading import Event, Lock, Thread
from typing import List

from ski_lift.core.command.descriptor.executor.base import CommandExecutor
from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.descriptor_result_factory import \
    DescriptorResultFactory
from ski_lift.core.command.result.object import CommandResult


class DelayedCommandExecutor(CommandExecutor):
    """Delayed command executor.
    
    This is a special command executor which allows executing delayed commands
    in the future determined with their delay attribute.

    Also the delayed commands can be aborted as well before the scheduled
    execution.
    """

    def __init__(self, *args, **kwargs):
        self._delayed_commands: List[CommandDescriptor] = []
        self._lock = Lock()
        self._stop_event = Event()
        self._executor_thread = Thread(target=self._process_delayed_commands, daemon=True)
        self._abort_in_progress = False
        super().__init__(*args, **kwargs)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        return False

    def start(self):
        """Start the execution thread.
        
        Delayed commands will be processed in the background.
        """
        self._executor_thread.start()

    def stop(self):
        """Stop the execution thread."""
        self._stop_event.set()
        self._executor_thread.join()

    def execute(self, descriptor: CommandDescriptor) -> CommandResult:
        if self.is_delayed(descriptor):
            self.handle_delayed(descriptor)
            return self._create_delayed_result(descriptor)
        else:
            return super().execute(descriptor)
        
    def is_delayed(self, descriptor: CommandDescriptor) -> bool:
        current_time = time.time()
        return current_time < descriptor.time.timestamp() + descriptor.delay
    
    def handle_delayed(self, command: CommandDescriptor):
        Thread(target=self._register_delayed_command, args=(command, ), daemon=True).start()
    
    def handle_instant(self, command: CommandDescriptor):
        Thread(target=self._unregister_delayed_command, args=(command, ), daemon=True).start()

    def abort(self, id: int):
        self._abort_in_progress = True
        self.remove(id)
        self._abort_in_progress = False

    def remove(self, id: int):
        with self._lock:
            self._delayed_commands = [
                command
                for command in self._delayed_commands
                if command.id != int(id)
            ]

    def _register_delayed_command(self, command: CommandDescriptor):
        with self._lock:
            if command not in self._delayed_commands:
                self._delayed_commands.append(command)

    def _unregister_delayed_command(self, command: CommandDescriptor):
        with self._lock:
            if command in self._delayed_commands:
                self.remove(command)

    def _process_delayed_commands(self):
        while not self._stop_event.is_set():
            time.sleep(1)
            with self._lock:
                to_keep = []
                for command in self._delayed_commands:
                    if self.is_delayed(command):
                        to_keep.append(command)
                    elif not self._abort_in_progress:
                        self.execute(command)
                    else:
                        to_keep.append(command)
                self._delayed_commands = to_keep

    def _create_delayed_result(self, command: CommandDescriptor) -> CommandResult:
        return DescriptorResultFactory().build(command, CommandResult.OutCome.DELAYED)
