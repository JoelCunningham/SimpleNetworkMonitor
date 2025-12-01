"""
Retry utilities for handling transient network failures.
"""
import enum
import time
from typing import Callable, TypeVar, Optional

T = TypeVar('T')

class RetryStatus(enum.Enum):
    FAILURE = enum.auto()
    TIMEOUT = enum.auto()
    ERROR = enum.auto()

def run_and_retry(func: Callable[[], RetryStatus | T], max_attempts: int, initial_delay: float, backoff_factor: float) -> Optional[T]:
    delay = initial_delay
    
    for attempt in range(max_attempts):
        result = func()
        
        if result not in (RetryStatus.FAILURE, RetryStatus.TIMEOUT, RetryStatus.ERROR):
            return result
        
        if attempt < max_attempts - 1:
            time.sleep(delay)
            delay *= backoff_factor
    
    return None
