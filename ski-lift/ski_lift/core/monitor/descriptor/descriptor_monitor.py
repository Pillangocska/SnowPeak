"""Command descriptor monitor."""

from functools import wraps
from typing import Any, Callable, List

from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.descriptor.processor import DescriptorProcessor


class CommandDescriptorMonitor(DescriptorProcessor):
    """Command descriptor monitor.
    
    This is a special `DescriptorProcessor` which can be used to monitor/log
    commands.

    The idea is that the incoming commands can be handled specifically in
    their own process functions where for example they can be written in to log
    files or sent over a network.

    The `monitor_descriptor` function only exists to make a more fitting name for the
    context. The base `process_descriptor` function could have been used as
    well.
    """

    def monitor_descriptor(self, command: CommandDescriptor) -> None:
        self.process_descriptor(command)


class CommandDescriptorMonitorSource:
    """Command descriptor monitor source.
    
    Inheriting from this marks to given class as a descriptor monitor source.

    To trigger the monitoring for a given command you can use the
    `forward_command_descriptor` function manually or the
    `monitor_descriptor` decorator for automatic forwarding and monitoring.
    """

    def __init__(self, *args, **kwargs):
        self._descriptor_monitors: List[CommandDescriptorMonitor] = []
        super().__init__(*args, **kwargs)

    def register_descriptor_monitor(self, command_monitor: CommandDescriptorMonitor):
        self._descriptor_monitors.append(command_monitor)

    def remove_descriptor_monitor(self, command_monitor: CommandDescriptorMonitor):
        if command_monitor in self._descriptor_monitors:
            self._descriptor_monitors.remove(command_monitor)

    def forward_command_descriptor(self, command: CommandDescriptor):
        for monitor in self._descriptor_monitors:
            monitor.monitor_descriptor(command)


def monitor_descriptor(func: Callable[[CommandDescriptorMonitorSource, CommandDescriptor], Any]):
    """Monitor descriptor decorator.
    
    Place this decorator onto functions where you want to monitor the commands.
    The commands will be forwarded to the monitor classes before execution.

    Decorated functions are marked with a `_monitor_descriptor` attribute
    which makes them filterable for example in test cases via the inspect
    module.

    !WARNING!: Only use it on functions which follow the argument types
    defined in the type hint below otherwise the code could break.
    """
    func._monitor_descriptor = True
    @wraps(func)
    def wrapper(self: CommandDescriptorMonitorSource, command: CommandDescriptor) -> Any:
        self.forward_command_descriptor(command)
        return func(self, command)
    return wrapper
