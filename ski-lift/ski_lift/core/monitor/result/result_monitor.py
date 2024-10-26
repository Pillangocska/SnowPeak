

from functools import wraps
from typing import Any, Callable, List

from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.command.result.processor import ResultProcessor


class CommandResultMonitor(ResultProcessor):
    """Command result monitor.
    
    This is a special `ResultProcessor` which can be used to monitor/log
    command results.

    The idea is that the incoming results can be handled specifically in
    their own process functions where for example they can be written in to log
    files or sent over a network.

    The `monitor_result` function only exists to make a more fitting name for
    the context. The base `process_result` function could have been used as
    well.
    """

    def monitor_result(self, result: CommandResult) -> None:
        self.process_result(result)

    def process_result_universally(self, result: CommandResult) -> Any:
        pass


class CommandResultMonitorSource:
    """Command result monitor source.
    
    Inheriting from this marks to given class as a result monitor source.

    To trigger the monitoring for a given result you can use the
    `forward_command_result` function manually or the
    `monitor_result` decorator for automatic forwarding and monitoring.
    """

    def __init__(self, *args, **kwargs):
        self._result_monitors: List[CommandResultMonitor] = []
        super().__init__(*args, **kwargs)

    def register_result_monitor(self, monitor: CommandResultMonitor):
        self._result_monitors.append(monitor)

    def remove_result_monitor(self, monitor: CommandResultMonitor):
        if monitor in self._result_monitors:
            self._result_monitors.remove(monitor)

    def forward_command_result(self, result: CommandResult):
        for monitor in self._result_monitors:
            monitor.monitor_result(result)


def monitor_result(func: Callable[[CommandResultMonitorSource, CommandDescriptor], CommandResult]):
    """Monitor result decorator.
    
    Place this decorator onto functions where you want to monitor the results.

    Decorated functions are marked with a `_monitor_result` attribute
    which makes them filterable for example in test cases via the inspect
    module.

    !WARNING!: Only use it on functions which follow the argument types
    defined in the type hint below otherwise the code could break.
    """
    func._monitor_result = True
    @wraps(func)
    def wrapper(self: CommandResultMonitorSource, command: CommandDescriptor) -> CommandResult:        
        result: CommandResult = func(self, command)
        self.forward_command_result(result)
        return result
    return wrapper
