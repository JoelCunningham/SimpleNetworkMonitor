from abc import ABC
from typing import Any


class Injectable(ABC):
    """Base class for injectable components."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def dispose(self) -> None:
        pass