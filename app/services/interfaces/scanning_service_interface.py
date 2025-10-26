from datetime import datetime
from typing import Protocol

from app.objects import AddressData


class ScanningServiceInterface(Protocol):
	"""Interface for the background scanning manager."""

	def start_continuous_scan(self) -> None:
		"""Start the background scanning thread/task."""
		...

	def get_latest_results(self) -> list[AddressData]:
		"""Return the most recent scan results as a list of AddressData."""
		...

	def stop_continuous_scan(self) -> None:
		"""Stop the background scanning thread/task."""
		...
    
	def get_last_scan_time(self) -> datetime | None:
		"""Return the datetime of the last completed scan, or None."""
		...