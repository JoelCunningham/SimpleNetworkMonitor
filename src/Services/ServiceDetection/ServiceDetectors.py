"""Service detection implementations."""
import socket
from typing import Optional
import urllib.error
import urllib.request

from Interfaces.IConfigurationProvider import IConfigurationProvider
from Interfaces.IServiceDetection import IHttpServiceDetector, ISshServiceDetector, IBannerGrabber
from Objects.Injectable import Injectable
from Objects.ServiceInfo import ServiceInfo


class HttpServiceDetector(IHttpServiceDetector, Injectable):
    """Detector for HTTP services."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
    
    def detect_service(self, ip_address: str, port: int, protocol: str = "tcp") -> Optional[ServiceInfo]:
        """Detect HTTP service and get server information."""
        timeout_settings = self._config_provider.get_timeout_settings()
        timeout_seconds = timeout_settings["service_detection_timeout_ms"] / 1000
        
        try:
            protocol_scheme = "https" if port == 443 else "http"
            url = f"{protocol_scheme}://{ip_address}:{port}/"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'NetworkMonitor/1.0')
            
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                headers = response.headers
                server = headers.get('Server', 'Unknown HTTP Server')
                
                return ServiceInfo(
                    service_name="http",
                    product=server,
                    extra_info=f"Status: {response.status}"
                )
        
        except (urllib.error.URLError, socket.timeout, Exception):
            return ServiceInfo(service_name="http", product="Unknown HTTP Server")


class SshServiceDetector(ISshServiceDetector, Injectable):
    """Detector for SSH services."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
    
    def detect_service(self, ip_address: str, port: int, protocol: str = "tcp") -> Optional[ServiceInfo]:
        """Detect SSH service and get version banner."""
        timeout_settings = self._config_provider.get_timeout_settings()
        timeout_seconds = timeout_settings["service_detection_timeout_ms"] / 1000
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout_seconds)
                sock.connect((ip_address, port))
                
                # Read SSH banner
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                
                if banner.startswith('SSH-'):
                    parts = banner.split()
                    version = parts[0] if parts else "Unknown"
                    
                    return ServiceInfo(
                        service_name="ssh",
                        version=version,
                        extra_info=banner
                    )
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return ServiceInfo(service_name="ssh", product="SSH Server")


class GenericBannerGrabber(IBannerGrabber, Injectable):
    """Generic banner grabbing service."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
    
    def grab_banner(self, ip_address: str, port: int) -> Optional[str]:
        """Generic banner grabbing for text-based services."""
        timeout_settings = self._config_provider.get_timeout_settings()
        timeout_seconds = timeout_settings["service_detection_timeout_ms"] / 1000
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout_seconds)
                sock.connect((ip_address, port))
                
                # Try to read banner
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                
                if banner:
                    return banner[:100]  # Limit banner length
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return None


class ServiceDetectionOrchestrator(Injectable):
    """Orchestrates service detection across multiple detectors."""
    
    def __init__(self, config_provider: IConfigurationProvider,
                 http_detector: IHttpServiceDetector,
                 ssh_detector: ISshServiceDetector,
                 banner_grabber: IBannerGrabber) -> None:
        self._config_provider = config_provider
        self._http_detector = http_detector
        self._ssh_detector = ssh_detector
        self._banner_grabber = banner_grabber
    
    def detect_service_on_port(self, ip_address: str, port: int, service_name: str) -> Optional[ServiceInfo]:
        """Detect service on a specific port based on the service type."""
        feature_flags = self._config_provider.get_feature_flags()
        
        # HTTP detection
        if (feature_flags.get("detect_http", False) and 
            (port in [80, 443, 8080, 8443] or "http" in service_name.lower())):
            return self._http_detector.detect_service(ip_address, port)
        
        # SSH detection
        if (feature_flags.get("detect_ssh", False) and 
            (port == 22 or "ssh" in service_name.lower())):
            return self._ssh_detector.detect_service(ip_address, port)
        
        # Generic banner grabbing
        if (feature_flags.get("detect_banners", False) and 
            service_name in ["telnet", "smtp", "pop3", "imap", "ftp"]):
            banner = self._banner_grabber.grab_banner(ip_address, port)
            if banner:
                return ServiceInfo(
                    service_name=service_name,
                    extra_info=banner
                )
        
        return None
