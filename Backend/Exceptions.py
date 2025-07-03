class NetworkMonitorError(Exception):
    """Base exception class for network monitor errors."""
    pass


class ConfigurationError(NetworkMonitorError):
    """Raised when there's an issue with configuration."""
    pass


class DatabaseError(NetworkMonitorError):
    """Raised when there's a database-related error."""
    pass


class NetworkScanError(NetworkMonitorError):
    """Raised when there's an error during network scanning."""
    pass


class ValidationError(NetworkMonitorError):
    """Raised when data validation fails."""
    pass
