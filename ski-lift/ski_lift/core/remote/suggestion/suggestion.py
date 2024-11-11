"""Suggestion representation."""

import datetime
from enum import Enum, auto
from dataclasses import dataclass
import json
from camel_converter import dict_to_snake
from ski_lift.core.utils.json_utils import datetime_parser

class SuggestionCategory(Enum):

    INFO = 'INFO'
    WARNING = 'WARNING'
    DANGER = 'DANGER'


def suggestion_category_parser(data):
    for key, value in data.items():
        if isinstance(value, str):
            try:
                data[key] = SuggestionCategory(value)
            except ValueError:
                pass
    return data


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

    @classmethod
    def from_dict(cls, data: dict) -> 'Suggestion':
        try:
            return cls(**data)
        except TypeError as exc:
            print(exc)
            return None
        
    @classmethod
    def from_json(cls, json_str: str) -> 'Suggestion':
        return cls.from_dict(dict_to_snake(
            json.loads(
                json_str,
                object_hook=lambda data: datetime_parser(suggestion_category_parser(data)))
            )
        )