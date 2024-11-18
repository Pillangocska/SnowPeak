"""Command results.

Command results are simply data classes that can be used to encapsulate 
command results which are produced via command executors.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Optional

from ski_lift.core.command.descriptor.object import (
    AbortCommandDescriptor, ChangeStateCommandDescriptor, CommandDescriptor,
    DisplayStatusCommandDescriptor, EmergencyStopCommandDescriptor,
    InsertCardCommandDescriptor, MessageReportCommandDescriptor,
    RemoveCardCommandDescriptor)
from ski_lift.core.engine import EngineState

if TYPE_CHECKING:
    from ski_lift.core.command.result.processor import ResultProcessor



@dataclass(kw_only=True)
class CommandResult(ABC):
    """Base class for command results.

    Referenced as `result` in the project.

    Each result will include the command descriptor that originated it, an
    outcome which describers generally the overall outcome and optionally an
    exception.

    If a result is failed then it must have the exception which describes why
    it failed.
    
    Attributes:
        command (CommandDescriptor): Descriptor which this result relates to.
        outcome (OutCome): General outcome of the command.
        exception (Exception): Exception that's been raised during execution.

    Most attributes are initialized to None by default, allowing them to be
    modified later.
    """

    class OutCome(Enum):
        """Possible outcomes.
        
        Successful means the execution was successful.
        Delayed means that the command will be executed later.
        Failed means that the execution failed for some reason.
        """

        SUCCESSFUL = auto()
        DELAYED = auto()
        FAILED = auto()

    command: Optional[CommandDescriptor] = None
    time: datetime = field(init=False)
    outcome: Optional[OutCome] = None
    exception: Optional[Exception] = None

    def __post_init__(self):
        self.time = self.command.time + timedelta(self.command.delay)

    @abstractmethod
    def accept(self, processor: 'ResultProcessor') -> Any:
        """Used visitor pattern double dispatch."""
        pass

    @property
    def is_successful(self) -> bool:
        """A result considered successful if its not failed."""
        return self.outcome != self.OutCome.FAILED

@dataclass(kw_only=True)
class InsertCardCommandResult(CommandResult):
    """Command result for the insert card command."""

    command: Optional[InsertCardCommandDescriptor] = None

    def accept(self, processor: 'ResultProcessor') -> Any:        
        """Used visitor pattern double dispatch."""
        return processor.process_insert_card_result(self)


@dataclass(kw_only=True)
class RemoveCardCommandResult(CommandResult):
    """Command result for the remove card command."""
    
    command: Optional[RemoveCardCommandDescriptor] = None

    def accept(self, processor: 'ResultProcessor') -> Any:
        """Used visitor pattern double dispatch."""
        return processor.process_remove_card_result(self)


@dataclass(kw_only=True)
class ChangeStateCommandResult(CommandResult):
    """Command result for the change state command."""
    
    command: Optional[ChangeStateCommandDescriptor] = None
    
    def accept(self, processor: 'ResultProcessor') -> Any:
        """Used visitor pattern double dispatch."""
        return processor.process_change_state_result(self)


@dataclass(kw_only=True)
class DisplayStatusCommandResult(CommandResult):
    """Command result for the display status command."""
    
    command: Optional[DisplayStatusCommandDescriptor] = None
    result: Optional[EngineState] = None

    def accept(self, processor: 'ResultProcessor') -> Any:
        """Used visitor pattern double dispatch."""
        return processor.process_display_status_result(self)


@dataclass
class AbortCommandResult(CommandResult):
    """Command result for the abort command command."""

    command: Optional[AbortCommandDescriptor] = None

    def accept(self, processor: 'ResultProcessor') -> Any:
        """Used visitor pattern double dispatch."""
        return processor.process_abort_command_result(self)


@dataclass
class EmergencyStopCommandResult(CommandResult):
    """Command result for the emergency stop command."""
    
    command: Optional[EmergencyStopCommandDescriptor] = None

    def accept(self, processor: 'ResultProcessor') -> Any:
        """Used visitor pattern double dispatch."""
        return processor.process_emergency_stop_result(self)


@dataclass(kw_only=True)
class MessageReportCommandResult(CommandResult):
    """Command result for the message report command."""

    command: Optional[MessageReportCommandDescriptor] = None

    def accept(self, processor: 'ResultProcessor') -> Any:
        """Used visitor pattern double dispatch."""
        return processor.process_message_report_result(self)
