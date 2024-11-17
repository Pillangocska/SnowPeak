"""Controller implementation."""

from ski_lift.core.auth import BaseAuthorizer, CommandAuthorizable
from ski_lift.core.command.descriptor.executor.delayed import \
    DelayedCommandExecutor
from ski_lift.core.engine import Engine, EngineState
from ski_lift.core.math.erlang_c import ErlangCModel
from ski_lift.core.monitor.descriptor.descriptor_monitor import \
    CommandDescriptorMonitorSource
from ski_lift.core.monitor.result.result_monitor import \
    CommandResultMonitorSource
from ski_lift.core.remote.communicator import RemoteCommunicator


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

    def __init__(
        self,
        lift_id: str,
        engine: Engine,
        authorizer: BaseAuthorizer,
        remote_communicator: RemoteCommunicator,
        queue_status: ErlangCModel,
    ):
        self._lift_id = lift_id
        self._engine = engine
        self._remote_communicator = remote_communicator
        self._remote_communicator.set_controller(self)
        self._queue_status = queue_status
        super().__init__(authorizer=authorizer)

    def __enter__(self):
        super().__enter__()
        self._remote_communicator.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self._remote_communicator.stop()
        return False


    @property
    def queue_time(self) -> float:
        if self.engine_state == EngineState.STOPPED:
            return -1
        multiplier: float = 0.5 if self.engine_state == EngineState.HALF_STEAM else 1.0
        metrics: dict = self._queue_status.get_performance_metrics(speed_multiplier=multiplier)
        return metrics.get('waiting_time [min]', -1)
        

    @property
    def lift_id(self) -> str:
        return self._lift_id

    @property
    def inserted_card(self) -> int:
        return self._authorizer.inserted_card
    
    @property
    def engine_state(self) -> EngineState:
        return self._engine.state
