import datetime as dt
from io import BytesIO
from typing import Optional, Union


class File:
    """Bsecure `File` type"""

    def __init__(self, content: BytesIO, filename: Optional[str] = None):
        self.filename = filename or content.name
        self.content = content


class FileID:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return self.id


def remove_trailing_slash(path: str) -> str:
    if path and path[-1] == "/":
        path = path[:-1]
    return path


def make_timestamp(value: Optional[Union[dt.datetime, dt.date]]) -> Optional[str]:
    if isinstance(
        value,
        (
            dt.datetime,
            dt.date,
        ),
    ):
        return value.isoformat()
    else:
        return None
