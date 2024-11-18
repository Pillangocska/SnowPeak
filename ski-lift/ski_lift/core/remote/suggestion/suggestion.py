"""Suggestion representation."""

import datetime
import json
from dataclasses import dataclass
from enum import Enum

from camel_converter import dict_to_snake


class SuggestionCategory(Enum):

    INFO = 'INFO'
    WARNING = 'WARNING'
    DANGER = 'DANGER'


severity_color_mapping = {
    SuggestionCategory.INFO: 'blue',
    SuggestionCategory.WARNING: 'yellow',
    SuggestionCategory.DANGER: 'red',
}


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

    def __post_init__(self):
        if isinstance(self.time, str):
            self.time = datetime.datetime.fromisoformat(self.time)
        if isinstance(self.category, str):
            self.category = SuggestionCategory(self.category.upper())

    @property
    def as_rich_text(self) -> str:
        formatted_time = self.time.strftime("%Y-%m-%d %H:%M:%S")
        severity_color = severity_color_mapping.get(self.category, 'purple')
        return f'[{severity_color}][{formatted_time}] [{self.category.name}]  {self.message}[/{severity_color}]'

    @classmethod
    def from_dict(cls, data: dict) -> 'Suggestion':
        try:
            return cls(
                sender_card_number=data.get('user'),
                time=data.get('timestamp'),
                category=data.get('severity'),
                message=data.get('message'),
            )
        except TypeError as exc:
            print(exc)
            return None
        
    @classmethod
    def from_json(cls, json_str: str) -> 'Suggestion':
        return cls.from_dict(dict_to_snake(json.loads(json_str)))
