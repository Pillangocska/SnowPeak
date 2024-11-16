"""Suggestion forwarder."""

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ski_lift.core.view import BaseView


class SuggestionForwarder:
    
    def __init__(self, view: 'BaseView'):
        self._view = view

    def __enter__(self):
        self.start_handling_suggestions()
        return self
    
    def __exit__(self, exc_type, exc_value, stack_trace) -> bool:
        self.stop_handling_suggestions()
        return False

    @abstractmethod
    def start_handling_suggestions(self) -> None:
        pass
    
    @abstractmethod
    def stop_handling_suggestions(self):
        pass
