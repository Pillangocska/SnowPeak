"""Descriptor processor."""

from abc import ABC, abstractmethod
from typing import Any

from ski_lift.core.command.descriptor.object import (
    AbortCommandDescriptor, ChangeStateCommandDescriptor, CommandDescriptor,
    DisplayStatusCommandDescriptor, EmergencyStopCommandDescriptor,
    InsertCardCommandDescriptor, RemoveCardCommandDescriptor)


class DescriptorProcessor(ABC):
    """Descriptor processor.
    
    This is simple visitor that uses double dispatch to process the commands
    with their specific functions.

    By default each command will be processed via the
    `process_descriptor_universally` which is meant to be a universal solution.
    """

    def process_descriptor(self, command: CommandDescriptor) -> Any:
        return command.accept(self)

    @abstractmethod
    def process_descriptor_universally(self, command: CommandDescriptor) -> Any:
        pass
    
    def process_insert_card_descriptor(self, command: InsertCardCommandDescriptor) -> Any:
        return self.process_descriptor_universally(command)

    def process_remove_card_descriptor(self, command: RemoveCardCommandDescriptor) -> Any:
        return self.process_descriptor_universally(command)

    def process_change_state_descriptor(self, command: ChangeStateCommandDescriptor) -> Any:
        return self.process_descriptor_universally(command)

    def process_display_status_descriptor(self, command: DisplayStatusCommandDescriptor) -> Any:
        return self.process_descriptor_universally(command)

    def process_abort_command_descriptor(self, command: AbortCommandDescriptor) -> Any:
        return self.process_descriptor_universally(command)

    def process_emergency_stop_descriptor(self, command: EmergencyStopCommandDescriptor) -> Any:
        return self.process_descriptor_universally(command)
