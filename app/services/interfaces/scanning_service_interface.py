from datetime import datetime
from typing import Protocol


class ScanningServiceInterface(Protocol):
	"""Interface for the background scanning manager."""

	def start_continuous_scan(self) -> None:
		"""Start the background scanning thread/task."""
		...

	def stop_continuous_scan(self) -> None:
		"""Stop the background scanning thread/task."""
		...
    
	def get_last_scan_time(self) -> datetime | None:
		"""Return the datetime of the last completed scan, or None."""
		...