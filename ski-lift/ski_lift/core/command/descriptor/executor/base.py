

from typing import Any
from ski_lift.core.command.descriptor.object import (
    AbortCommandDescriptor, ChangeStateCommandDescriptor, CommandDescriptor,
    DisplayStatusCommandDescriptor, EmergencyStopDescriptor, InsertCardCommandDescriptor,
    RemoveCardCommandDescriptor)
from ski_lift.core.command.descriptor.processor import DescriptorProcessor
from ski_lift.core.command.descriptor_result_factory import \
    DescriptorResultFactory
from ski_lift.core.command.result.object import (AbortCommandResult,
                                                 ChangeStateCommandResult,
                                                 CommandResult,
                                                 DisplayStatusCommandResult,
                                                 InsertCardCommandResult,
                                                 RemoveCardCommandResult)


class CommandExecutor(DescriptorProcessor):
    """Command executor.
    
    This is a special `DescriptorProcessor` which processes
    `CommandDescriptors` and returns the corresponding `CommandResult` for each
    of them.

    By default each command will be processed into a successful result.
    If an exception is raised during the execution the appropriate failed
    result will be returned containing the exception it self.

    The `execute` function only exists to make a more fitting name for the
    context. The base `process_descriptor` function could have been used as
    well.

    The process functions are implemented again to help the type checker only
    nothing else.
    """

    def execute(self, command: CommandDescriptor) -> CommandResult:
        """Execute the """
        try:
            return self.process_descriptor(command)
        except Exception as exc:
            return DescriptorResultFactory().build(command, CommandResult.OutCome.FAILED, exc)

    def process_descriptor(self, command: CommandDescriptor) -> CommandResult:
        return super().process_descriptor(command)

    def process_descriptor_universally(self, command: CommandDescriptor) -> CommandResult:
        return DescriptorResultFactory().build(command, CommandResult.OutCome.SUCCESSFUL)
    
    def process_insert_card_descriptor(self, command: InsertCardCommandDescriptor) -> InsertCardCommandResult:
        return super().process_insert_card_descriptor(command)

    def process_remove_card_descriptor(self, command: RemoveCardCommandDescriptor) -> RemoveCardCommandResult:
        return super().process_remove_card_descriptor(command)

    def process_change_state_descriptor(self, command: ChangeStateCommandDescriptor) -> ChangeStateCommandResult:
        return super().process_change_state_descriptor(command)

    def process_display_status_descriptor(self, command: DisplayStatusCommandDescriptor) -> DisplayStatusCommandResult:
        return super().process_display_status_descriptor(command)

    def process_abort_command_descriptor(self, command: AbortCommandDescriptor) -> AbortCommandResult:
        return super().process_abort_command_descriptor(command)
    
    def process_emergency_stop_descriptor(self, command: EmergencyStopDescriptor) -> EmergencyStopDescriptor:
        return super().process_emergency_stop_descriptor(command)
