
from ski_lift.core.command.descriptor.factory import CommandDescriptorFactory
from ski_lift.core.remote.suggestion.suggestion_forwarder import SuggestionForwarder

from abc import abstractmethod
from ski_lift.core.controller import Controller
from threading import Event, Thread

from ski_lift.core.remote.suggestion.suggestion_forwarder import SuggestionForwarder
from ski_lift.core.view.base_view import BaseView
from ski_lift.core.view.suggestion import Suggestion, SuggestionCategory
from datetime import datetime
import random
from time import sleep

class TestEmergencyStopper(SuggestionForwarder):

    def handle_suggestions(self) -> None:
        sleep_time = 0
        while not self._stop_event.is_set():
            sleep(1)
            if sleep_time < 60:
                sleep_time+=1
                continue
            self._view.display_suggestion(
                Suggestion(
                    sender_card_number='xyz123',
                    time=datetime.now(),
                    category=SuggestionCategory.DANGER,
                    message='Emergency stop initialized due to bad weather.'
                ),
                reset_input=False,
            )
            self._view._controller.execute(CommandDescriptorFactory().create_emergency_stop(user_card='xyz', delay=5))
            sleep_time = 0
