import socket
import urllib.error
import urllib.request

from app import config
from app.objects import ServiceInfo
from app.services.interfaces import ProtocolServiceInterface

HTTP_DEFAULT_SERVER = 'Unknown HTTP Server'
HTTP_INFO_TEMPLATE = "Status: {status}"
HTTP_SCHEME = "http"
HTTPS_SCHEME = "https"
HTTP_SERVICE_NAME = "http"
HTTP_URL_TEMPLATE = "{protocol_scheme}://{ip_address}:{port}/"
HTTPS_PORT = 443

SSH_DEFAULT_PRODUCT = "SSH Server"
SSH_BANNER_PREFIX = 'SSH-'
SSH_SERVICE_NAME = "ssh"

MAX_BANNER_LENGTH = 100

DEFAULT_VERSION = "Unknown"
DEFAULT_ENCODING = 'utf-8'
ENCODING_ERROR_HANDLING = 'ignore'
SOCKET_BUFFER_SIZE = 1024
SERVER_HEADER = 'Server'
USER_AGENT_HEADER = "User-Agent"
USER_AGENT_VALUE = 'NetworkMonitor/1.0'

class ProtocolService(ProtocolServiceInterface):
    """Detector for HTTP services."""
    
    def detect_http(self, ip: str, port: int) -> ServiceInfo | None:
        """Detect HTTP service and get server information."""        
        try:
            protocol_scheme = HTTPS_SCHEME if port == HTTPS_PORT else HTTP_SCHEME
            url = HTTP_URL_TEMPLATE.format(protocol_scheme=protocol_scheme, ip_address=ip, port=port)
            
            req = urllib.request.Request(url)
            req.add_header(USER_AGENT_HEADER, USER_AGENT_VALUE)
            
            timeout = config.service_detection_timeout_ms / 1000
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                headers = response.headers
                server = headers.get(SERVER_HEADER, HTTP_DEFAULT_SERVER)
                
                return ServiceInfo(
                    service_name=HTTP_SERVICE_NAME,
                    product=server,
                    extra_info=HTTP_INFO_TEMPLATE.format(status=response.status)
                )
        
        except (urllib.error.URLError, socket.timeout, Exception):
            return ServiceInfo(service_name=HTTP_SERVICE_NAME, product=HTTP_DEFAULT_SERVER)

    def detect_ssh(self, ip: str, port: int) -> ServiceInfo | None:
        """Detect SSH service and get version banner."""
        try:

            timeout = config.service_detection_timeout_ms / 1000
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((ip, port))
                
                banner = sock.recv(SOCKET_BUFFER_SIZE).decode(DEFAULT_ENCODING, errors=ENCODING_ERROR_HANDLING).strip()
                
                if banner.startswith(SSH_BANNER_PREFIX):
                    parts = banner.split()
                    version = parts[0] if parts else DEFAULT_VERSION
                    
                    return ServiceInfo(
                        service_name=SSH_SERVICE_NAME,
                        version=version,
                        extra_info=banner
                    )
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return ServiceInfo(service_name=SSH_SERVICE_NAME, product=SSH_DEFAULT_PRODUCT)
    
    def detect_banner(self, ip: str, port: int, service_name: str) -> ServiceInfo | None:
        """Generic banner grabbing for text-based services."""        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(config.service_detection_timeout_ms / 1000)
                sock.connect((ip, port))
                
                banner = sock.recv(SOCKET_BUFFER_SIZE).decode(DEFAULT_ENCODING, errors=ENCODING_ERROR_HANDLING).strip()
                
                if banner:
                    return ServiceInfo(
                        service_name=service_name,
                        extra_info=banner[:MAX_BANNER_LENGTH]
                    )                
                        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return None