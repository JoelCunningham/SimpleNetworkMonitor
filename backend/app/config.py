"""
Pydantic-based configuration settings for the SimpleNetworkMonitor application.
"""
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

basedir = Path(__file__).parent.parent


class Config(BaseSettings):
    """Application settings with validation and type safety."""
    
    # Flask core settings
    debug: bool = Field(default=True, description="Enable debug mode")
    testing: bool = Field(default=False, description="Enable testing mode")
    
    # Database configuration
    database_url: str = Field(default=f'sqlite:///{basedir}/network_monitor.db')
    sqlalchemy_track_modifications: bool = Field(default=False)
    sqlalchemy_echo: bool = Field(default=False)
    
    # Background task configuration
    scan_check_interval_s: int = Field(default=10, ge=5)
    background_scan_interval_s: int = Field(default=60, ge=60)
    background_full_scan_interval_s: int = Field(default=300, ge=60)
    
    # Network configuration
    subnet: str = Field(default='192.168.0', pattern=r'^\d{1,3}\.\d{1,3}\.\d{1,3}$')
    min_scan_ip: int = Field(default=1, ge=1, le=254)
    max_scan_ip: int = Field(default=254, ge=1, le=254)
    max_threads: int = Field(default=254)
    ping_count: int = Field(default=3)
    
    # Retry configuration
    arp_max_retries: int = Field(default=3, ge=1)
    ping_max_retries: int = Field(default=3, ge=1)
    arp_retry_delay_ms: int = Field(default=100, ge=0)
    ping_retry_delay_ms: int = Field(default=100, ge=0)
    arp_retry_backoff: float = Field(default=2.0, ge=1.0)
    ping_retry_backoff: float = Field(default=2.0, ge=1.0)
    
    # Timeout configuration (in milliseconds)
    ping_timeout_ms: int = Field(default=2000)
    arp_timeout_ms: int = Field(default=1000)
    hostname_timeout_ms: int = Field(default=1000)
    port_scan_timeout_ms: int = Field(default=1000)
    service_detection_timeout_ms: int = Field(default=2000)
    discovery_timeout_ms: int = Field(default=3000)
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = 'ignore'

_config = Config()


def __getattr__(name: str):
    try:
        return getattr(_config, name)
    except AttributeError as exc:
        raise AttributeError(f"module {__name__} has no attribute {name}") from exc
