

from abc import ABC, abstractmethod
from typing import Any

from ski_lift.core.command.result.object import (AbortCommandResult,
                                                 ChangeStateCommandResult,
                                                 CommandResult,
                                                 DisplayStatusCommandResult, EmergencyStopCommandResult,
                                                 InsertCardCommandResult,
                                                 RemoveCardCommandResult)


class ResultProcessor(ABC):
    """Result processor.
    
    This is simple visitor that uses double dispatch to process the results
    with their specific functions.

    By default each result will be processed via the
    `process_result_universally` function which is meant to be a universal
    solution.
    """
    
    def process_result(self, result: CommandResult) -> Any:
        return result.accept(self)

    @abstractmethod
    def process_result_universally(self, result: CommandResult) -> Any:
        pass
    
    def process_insert_card_result(self, result: InsertCardCommandResult) -> Any:
        return self.process_result_universally(result)

    def process_remove_card_result(self, result: RemoveCardCommandResult) -> Any:
        return self.process_result_universally(result)

    def process_change_state_result(self, result: ChangeStateCommandResult) -> Any:
        return self.process_result_universally(result)

    def process_display_status_result(self, result: DisplayStatusCommandResult) -> Any:
        return self.process_result_universally(result)

    def process_abort_command_result(self, result: AbortCommandResult) -> Any:
        return self.process_result_universally(result)

    def process_emergency_stop_result(self, result: EmergencyStopCommandResult) -> Any:
        return self.process_result_universally(result)
