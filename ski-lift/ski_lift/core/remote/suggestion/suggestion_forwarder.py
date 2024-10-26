"""Suggestion forwarder."""

from abc import abstractmethod
from ski_lift.core.controller import Controller
from threading import Event, Thread

from ski_lift.core.view.base_view import BaseView


class SuggestionForwarder:
    
    def __init__(self, view: BaseView):
        self._view = view
        self._stop_event = Event()
        self._executor_thread = Thread(target=self.handle_suggestions, daemon=True)

    @abstractmethod
    def handle_suggestions(self) -> None:
        pass

    def start(self):
        self._executor_thread.start()

    def stop(self):
        self._stop_event.set()
        self._executor_thread.join()
