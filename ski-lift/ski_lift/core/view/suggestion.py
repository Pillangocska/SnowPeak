"""Suggestion representation."""

import datetime
from dataclasses import dataclass
from enum import Enum, auto


class SuggestionCategory(Enum):

    INFO = auto()
    WARNING = auto()
    DANGER = auto()


@dataclass(kw_only=True)
class Suggestion:
    """Suggestion representation.
    
    Suggestion is a simple data class that represent the suggestions which
    can be sent from the central operation room.

    Attributes:
        sender_card_number (str): Operator who sent the suggestion.
        time (datetime): Time when the suggestion was sent.
        category (SuggestionCategory): Describes who serious the topic is.
        message (str): The suggestion itself.
    """

    sender_card_number: str
    time: datetime
    category: SuggestionCategory
    message: str
