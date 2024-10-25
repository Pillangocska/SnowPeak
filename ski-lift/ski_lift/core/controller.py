"""Controller implementation."""


from ski_lift.core.auth.authorizer.base_authorizer import (BaseAuthorizer,
                                                           CommandAuthorizable)
from ski_lift.core.command.descriptor.executor.delayed import \
    DelayedCommandExecutor
from ski_lift.core.engine import Engine
from ski_lift.core.monitor.descriptor.descriptor_monitor import (
    CommandDescriptorMonitor, CommandDescriptorMonitorSource)
from ski_lift.core.monitor.result.result_monitor import (
    CommandResultMonitor, CommandResultMonitorSource)


class Controller(
    DelayedCommandExecutor, CommandAuthorizable, CommandResultMonitorSource, CommandDescriptorMonitorSource
):
    """Controller.
    
    The controller class represents that main business logic of a ski lift
    operator panel. It uses a delayed command executor which means that delayed
    commands will be executed in a background thread. These commands can be
    aborted as well.

    Processing commands can be authorized via the authorizer. Use the
    `send_through_auth` decorator for automatic authorization check.

    The class itself is also a result and descriptor monitor source which means
    that commands and their results can be monitored via the registered
    monitors.

    Check the super classes for more information.
    """

    def __init__(self, engine: Engine, authorizer: BaseAuthorizer):
        self._engine = engine
        super().__init__(authorizer=authorizer)

    @property
    def inserted_card(self) -> int:
        return self._authorizer.inserted_card