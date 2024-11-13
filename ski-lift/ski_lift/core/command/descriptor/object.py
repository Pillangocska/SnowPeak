"""Command descriptors.

Command descriptors are simply data classes that can be used to describe 
commands that are intended to be executed on a ski lift controller.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from ski_lift.core.command.descriptor.processor import DescriptorProcessor


@dataclass(kw_only=True)
class CommandDescriptor(ABC):
    """Base class for command descriptors.

    Referenced as `command` in the project.

    Attributes:
        id (int): Automatically incremented id.
        user_card (str): User who requested the command.
        time (datetime): Time the command has been requested.
        delay (int): Delay in seconds after the command should be executed.
        secret (str): Secret for the secret based authentication.

    !WARNING!: The `id` attribute only ensures unique identifiers for each
    session or run, so it should not be used in databases or any form of
    permanent storage. If you need to use it for such purposes, combining the
    `time` and `id` attributes will guarantee uniqueness.
    """

    id: int = field(init=False)
    user_card: str
    time: datetime
    delay: int = 0
    secret: Optional[str] = None

    _id_counter: ClassVar[int] = 0

    def __post_init__(self):
        """Set and increment the id."""
        self.id = CommandDescriptor._generate_next_id()

    @abstractmethod
    def accept(self, processor: 'DescriptorProcessor'):
        pass

    @classmethod
    def _generate_next_id(cls):
        cls._id_counter += 1
        return cls._id_counter

@dataclass(kw_only=True)
class InsertCardCommandDescriptor(CommandDescriptor):
    """Command descriptor for inserting a user card into the control panel.
    
    Attributes:
        card_to_insert (str): Card number that is intended to be inserted.
    """

    card_to_insert: str

    def accept(self, processor: 'DescriptorProcessor'):
        return processor.process_insert_card_descriptor(self)


@dataclass(kw_only=True)
class RemoveCardCommandDescriptor(CommandDescriptor):
    """Command descriptor for removing cards from the control panel."""
    
    def accept(self, processor: 'DescriptorProcessor'):
        return processor.process_remove_card_descriptor(self)


@dataclass(kw_only=True)
class ChangeStateCommandDescriptor(CommandDescriptor):
    """Command descriptor for changing the state of the engine.
    
    Attributes:
        new_state (Option): New state the engine should be set to.
    """
    
    class Option(Enum):
        """Options.
        
        These options correspond to the ones defined in the Engine class.
        """

        MAX_STEAM = auto()
        FULL_STEAM = auto()
        HALF_STEAM = auto()
        STOP = auto()

    new_state: Option

    def accept(self, processor: 'DescriptorProcessor'):
        return processor.process_change_state_descriptor(self)


@dataclass(kw_only=True)
class DisplayStatusCommandDescriptor(CommandDescriptor):
    """Command descriptor for displaying current status of the engine."""
    
    def accept(self, processor: 'DescriptorProcessor'):
        return processor.process_display_status_descriptor(self)


@dataclass(kw_only=True)
class AbortCommandDescriptor(CommandDescriptor):
    """Command descriptor for aborting a delayed command.
    
    Attribute:
        command_to_abort (int): Id of the command that should be aborted.
    """

    command_to_abort: int

    def accept(self, processor: 'DescriptorProcessor'):
        return processor.process_abort_command_descriptor(self)
    

@dataclass
class EmergencyStopCommandDescriptor(CommandDescriptor):
    """Command descriptor for emergency stop."""

    def accept(self, processor: 'DescriptorProcessor'):
        return processor.process_emergency_stop_descriptor(self)