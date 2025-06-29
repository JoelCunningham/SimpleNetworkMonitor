import socket
from typing import Optional

from Objects.Injectable import Injectable
from Objects.ServiceInfo import ServiceInfo
from Services.AppConfig import AppConfig


class ServiceDetectionService(Injectable):
    """Service for detecting specific services and gathering banner information."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
    
    def detect_http_service(self, ip_address: str, port: int) -> Optional[ServiceInfo]:
        """Detect HTTP service and get server information."""
        import urllib.error
        import urllib.request
        try:
            protocol = "https" if port == 443 else "http"
            url = f"{protocol}://{ip_address}:{port}/"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'NetworkMonitor/1.0')
            
            with urllib.request.urlopen(req, timeout=self._config.service_detection_timeout_ms / 1000) as response:
                headers = response.headers
                server = headers.get('Server', 'Unknown HTTP Server')
                
                return ServiceInfo(
                    service_name="http",
                    product=server,
                    extra_info=f"Status: {response.status}"
                )
        
        except (urllib.error.URLError, socket.timeout, Exception):
            return ServiceInfo(service_name="http", product="Unknown HTTP Server")
    
    def detect_ssh_service(self, ip_address: str, port: int) -> Optional[ServiceInfo]:
        """Detect SSH service and get version banner."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self._config.service_detection_timeout_ms / 1000)
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
    
    def grab_banner(self, ip_address: str, port: int) -> Optional[ServiceInfo]:
        """Generic banner grabbing for text-based services."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self._config.service_detection_timeout_ms / 1000)
                sock.connect((ip_address, port))
                
                # Try to read banner
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                
                if banner:
                    return ServiceInfo(
                        service_name="unknown",
                        extra_info=banner[:100]  # Limit banner length
                    )
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return None
