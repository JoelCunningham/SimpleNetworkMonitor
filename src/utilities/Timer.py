from typing import Iterator
from contextlib import contextmanager
import time

class Time:
    def __init__(self) -> None:
        self.value: float = 0.0

@contextmanager
def time_operation(timed: Time) -> Iterator[None]:
    start = time.time()
    yield
    timed.value = round((time.time() - start) * 1000, 1)
