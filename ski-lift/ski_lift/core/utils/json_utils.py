"""JSON related utils."""

from datetime import datetime


def datetime_parser(data):
    for key, value in data.items():
        if isinstance(value, str):
            try:
                # Try to parse ISO 8601 format
                data[key] = datetime.fromisoformat(value)
            except ValueError:
                # If parsing fails, keep the original value
                pass
    return data