"""Utility functions."""

import os
import sys
from datetime import datetime
from typing import Any, Optional

from camel_converter import to_snake


def get_lift_id_or_exit() -> str:
    """Get the lift id or exit the program if fails.

    Retrieve the lift id from either environmental variables or from sys
    arguments. If both are present then the sys arg takes precedence.

    Returns:
        str: Lift id.
    """
    lift_id: str = os.environ.get('LIFT_ID')
    try:
        lift_id = sys.argv[1]
    except IndexError:
        if lift_id is None:
            print('Usage: python -m ski_lift <lift_id>')
            exit(1)


def datetime_parser(data):
    """Object hook for json module thats parser iso strings to datetime."""
    for key, value in data.items():
        if isinstance(value, str):
            try:
                # Try to parse ISO 8601 format
                data[key] = datetime.fromisoformat(value)
            except ValueError:
                # If parsing fails, keep the original value
                pass
    return data


def class_name_to_snake(cls: Any, to_remove: Optional[str] = None) -> str:
    """Convert a class name to snake case string.

    Optionally parts can be removed from the name. Useful for post fixes for
    example.

    Args:
        cls (Any): Class to convert from.
        to_remove (Optional[str], optional): Part to remove.

    Returns:
        str: Class name converted to snake case variant.
    """
    string_name: str = cls.__class__.__name__
    if to_remove is not None:
        string_name = string_name.replace(to_remove, '')
    return to_snake(string_name)
