import socket
import urllib.error
import urllib.request
from typing import Optional

from Backend.Constants import (DEFAULT_HTTP_SERVER, HTTP_INFO_TEMPLATE,
                               HTTP_SCHEME, HTTP_SERVICE_NAME,
                               HTTP_URL_TEMPLATE, HTTPS_PORT, HTTPS_SCHEME,
                               SERVER_HEADER, USER_AGENT_HEADER,
                               USER_AGENT_VALUE)
from Backend.Objects.Injectable import Injectable
from Backend.Objects.ServiceInfo import ServiceInfo
from Backend.Services.AppConfiguration import AppConfig


class HttpServiceDetector(Injectable):
    """Detector for HTTP services."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
    
    def detect_service(self, ip_address: str, port: int) -> Optional[ServiceInfo]:
        """Detect HTTP service and get server information."""        
        try:
            protocol_scheme = HTTPS_SCHEME if port == HTTPS_PORT else HTTP_SCHEME
            url = HTTP_URL_TEMPLATE.format(protocol_scheme=protocol_scheme, ip_address=ip_address, port=port)
            
            req = urllib.request.Request(url)
            req.add_header(USER_AGENT_HEADER, USER_AGENT_VALUE)
            
            with urllib.request.urlopen(req, timeout=self._config.timeout.service_detection_timeout_s()) as response:
                headers = response.headers
                server = headers.get(SERVER_HEADER, DEFAULT_HTTP_SERVER)
                
                return ServiceInfo(
                    service_name=HTTP_SERVICE_NAME,
                    product=server,
                    extra_info=HTTP_INFO_TEMPLATE.format(status=response.status)
                )
        
        except (urllib.error.URLError, socket.timeout, Exception):
            return ServiceInfo(service_name=HTTP_SERVICE_NAME, product=DEFAULT_HTTP_SERVER)
