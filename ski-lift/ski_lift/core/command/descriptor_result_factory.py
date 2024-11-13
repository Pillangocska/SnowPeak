"""Descriptor result factory."""

from typing import Any, Optional

from ski_lift.core.command.descriptor.object import (
    AbortCommandDescriptor, ChangeStateCommandDescriptor, CommandDescriptor,
    DisplayStatusCommandDescriptor, EmergencyStopCommandDescriptor, InsertCardCommandDescriptor,
    RemoveCardCommandDescriptor)
from ski_lift.core.command.descriptor.processor import DescriptorProcessor
from ski_lift.core.command.result.object import (AbortCommandResult,
                                                 ChangeStateCommandResult,
                                                 CommandResult,
                                                 DisplayStatusCommandResult, EmergencyStopCommandResult,
                                                 InsertCardCommandResult,
                                                 RemoveCardCommandResult)


class DescriptorResultFactory(DescriptorProcessor):
    """Descriptor result factory.
    
    This is a special `DescriptorProcessor` which can produces appropriate
    result for a given command. 
    """

    def build(
        self,
        command: CommandDescriptor,
        outcome: CommandResult.OutCome,
        exception: Optional[Exception] = None,
    ) -> CommandDescriptor:
        result: CommandResult = self.process_descriptor(command)
        result.outcome = outcome
        result.exception = exception
        return result

    def process_descriptor_universally(self, descriptor: CommandDescriptor) -> Any:
        pass

    def process_insert_card_descriptor(self, descriptor: InsertCardCommandDescriptor) -> InsertCardCommandResult:
        return InsertCardCommandResult(command=descriptor)
    
    def process_remove_card_descriptor(self, descriptor: RemoveCardCommandDescriptor) -> RemoveCardCommandResult:
        return RemoveCardCommandResult(command=descriptor)
    
    def process_change_state_descriptor(self, descriptor: ChangeStateCommandDescriptor) -> ChangeStateCommandResult:
        return ChangeStateCommandResult(command=descriptor)
    
    def process_display_status_descriptor(self, descriptor: DisplayStatusCommandDescriptor) -> DisplayStatusCommandResult:
        return DisplayStatusCommandResult(command=descriptor)
    
    def process_abort_command_descriptor(self, descriptor: AbortCommandDescriptor) -> AbortCommandResult:
        return AbortCommandResult(command=descriptor)

    def process_emergency_stop_descriptor(self, descriptor: EmergencyStopCommandDescriptor) -> EmergencyStopCommandResult:
        return EmergencyStopResult(command=descriptor)
