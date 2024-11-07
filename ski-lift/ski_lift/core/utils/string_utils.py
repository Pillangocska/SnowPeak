"""String related utility functions."""

import re
from typing import Optional, Any


def pascal_to_snake(name):
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def class_name_to_snake(cls: Any, to_remove: Optional[str] = None) -> str:
    string_name: str = cls.__class__.__name__
    if to_remove is not None:
        string_name = string_name.replace(to_remove, '')
    return pascal_to_snake(string_name)
