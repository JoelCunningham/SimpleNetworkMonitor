from dataclasses import dataclass


@dataclass
class PingCommand:
    """Ping command information."""
    instruction: str
    count_flag: str
    timeout_flag: str
