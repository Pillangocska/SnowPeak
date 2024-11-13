"""Suggestion forwarder."""

from abc import abstractmethod
from threading import Event, Thread

from ski_lift.core.controller import Controller
from ski_lift.core.view.base_view import BaseView


class SuggestionForwarder:
    
    def __init__(self, view: BaseView):
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
