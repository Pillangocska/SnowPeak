"""Controller implementation."""

from ski_lift.core.auth.authorizer.base_authorizer import (BaseAuthorizer,
                                                           send_through_auth)
from ski_lift.core.command.descriptor.object import (
    AbortCommandDescriptor, ChangeStateCommandDescriptor, CommandDescriptor,
    DisplayStatusCommandDescriptor, EmergencyStopDescriptor, InsertCardCommandDescriptor,
    RemoveCardCommandDescriptor)
from ski_lift.core.command.result.object import (AbortCommandResult,
                                                 ChangeStateCommandResult,
                                                 CommandResult,
                                                 DisplayStatusCommandResult, EmergencyStopResult,
                                                 InsertCardCommandResult,
                                                 RemoveCardCommandResult)
from ski_lift.core.controller import Controller
from ski_lift.core.engine import Engine
from ski_lift.core.monitor.descriptor.descriptor_monitor import \
    monitor_descriptor
from ski_lift.core.monitor.result.result_monitor import monitor_result


class SkiLiftController(Controller):

    def __init__(self, engine: Engine, authorizer: BaseAuthorizer):
        super().__init__(engine=engine, authorizer=authorizer)

    def handle_delayed(self, command: CommandDescriptor):
        self.authenticate_delayed(command)
        return super().handle_delayed(command)

    @monitor_result
    @monitor_descriptor
    def execute(self, command: CommandDescriptor) -> CommandResult:
        return super().execute(command)

    @send_through_auth
    def process_insert_card_descriptor(self, command: InsertCardCommandDescriptor) -> InsertCardCommandResult:
        return super().process_insert_card_descriptor(command)

    @send_through_auth
    def process_remove_card_descriptor(self, command: RemoveCardCommandDescriptor) -> RemoveCardCommandResult:
        return super().process_remove_card_descriptor(command)

    @send_through_auth
    def process_change_state_descriptor(self, command: ChangeStateCommandDescriptor) -> ChangeStateCommandResult:
        match(command.new_state):
            case ChangeStateCommandDescriptor.Option.MAX_STEAM:
                self._engine.max_steam()
            case ChangeStateCommandDescriptor.Option.FULL_STEAM:
                self._engine.full_steam()
            case ChangeStateCommandDescriptor.Option.HALF_STEAM:
                self._engine.half_steam()
            case ChangeStateCommandDescriptor.Option.STOP:
                self._engine.stop()
        return super().process_change_state_descriptor(command)

    @send_through_auth
    def process_display_status_descriptor(self, command: DisplayStatusCommandDescriptor) -> DisplayStatusCommandResult:
        result: DisplayStatusCommandResult = super().process_display_status_descriptor(command)
        result.result = self._engine.state
        return result
    
    @send_through_auth
    def process_abort_command_descriptor(self, command: AbortCommandDescriptor) -> AbortCommandResult:
        self.abort(command.command_to_abort)
        return super().process_abort_command_descriptor(command)
    
    def process_emergency_stop_descriptor(self, command: EmergencyStopDescriptor) -> EmergencyStopResult:
        self._engine.stop()
        return super().process_emergency_stop_descriptor(command)