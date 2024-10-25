"""Suggestion forwarder."""

from ski_lift.core.remote.suggestion.suggestion_forwarder import SuggestionForwarder
from ski_lift.core.view.base_view import BaseView
from ski_lift.core.view.suggestion import Suggestion, SuggestionCategory
from datetime import datetime
import random
from time import sleep


class TestSuggestionForwarder(SuggestionForwarder):
    
    def handle_suggestions(self) -> None:
        while not self._stop_event.is_set():
            sleep(random.randint(5, 20))
            self._view.display_suggestion(
                Suggestion(
                    sender_card_number='xyz123',
                    time=datetime.now(),
                    category=random.choice(list(SuggestionCategory)),
                    message='This is a suggestion sent.'
                )
            )

