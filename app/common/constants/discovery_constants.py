from typing import Final

# mDNS constants
MDNS_ADDITIONAL_COUNT: Final[int] = 0
MDNS_ANSWERS_COUNT: Final[int] = 0
MDNS_AUTHORITY_COUNT: Final[int] = 0
MDNS_DEVICE_NAME_PREFIX: Final[str] = "mDNS-"
MDNS_DEVICE_TYPE: Final[str] = "mDNS/Bonjour Device"
MDNS_FLAGS: Final[int] = 0x0000
MDNS_HEADER_LENGTH: Final[int] = 12
MDNS_PORT: Final[int] = 5353
MDNS_PROTOCOL_NAME: Final[str] = "mdns"
MDNS_QUESTIONS_COUNT: Final[int] = 1
MDNS_SERVICE_QUERY: Final[bytes] = b'\x09_services\x07_dns-sd\x04_udp\x05local\x00\x00\x0c\x00\x01'
MDNS_TRANSACTION_ID: Final[int] = 0x0000

# NetBIOS constants
NETBIOS_ADDITIONAL_COUNT: Final[int] = 0
NETBIOS_ANSWERS_COUNT: Final[int] = 0
NETBIOS_AUTHORITY_COUNT: Final[int] = 0
NETBIOS_HEADER_LENGTH: Final[int] = 12
NETBIOS_MAX_NAME_LENGTH: Final[int] = 15
NETBIOS_MIN_RESPONSE_LENGTH: Final[int] = 50
NETBIOS_MIN_WORD_LENGTH: Final[int] = 2
NETBIOS_NAME_LENGTH: Final[bytes] = b'\x20'
NETBIOS_PORT: Final[int] = 137
NETBIOS_PROTOCOL_NAME: Final[str] = "netbios"
NETBIOS_QUERY_FLAGS: Final[int] = 0x0110
NETBIOS_QUERY_SUFFIX: Final[bytes] = b'\x00\x00\x20\x00\x01'
NETBIOS_QUESTIONS_COUNT: Final[int] = 1
NETBIOS_TRANSACTION_ID: Final[int] = 0x1234
NETBIOS_WILDCARD: Final[bytes] = b'A' * 31

# UPnP / SSDP / common discovery constants
UPNP_DEVICE_TYPE: Final[str] = "UPnP Device"
SSDP_HOST_HEADER: Final[str] = "HOST: 239.255.255.250:1900\r\n"
SSDP_MAN_HEADER: Final[str] = 'MAN: "ssdp:discover"\r\n'
SSDP_MX_PREFIX: Final[str] = "MX: "
SSDP_REQUEST_LINE: Final[str] = "M-SEARCH * HTTP/1.1\r\n"
SSDP_ST_HEADER: Final[str] = "ST: upnp:rootdevice\r\n"
UPNP_HEADER_SEPARATOR: Final[str] = ':'
UPNP_PORT: Final[int] = 1900
UPNP_PROTOCOL_NAME: Final[str] = "upnp"
UPNP_SERVER_HEADER_PREFIX: Final[str] = 'SERVER:'
UPNP_SPLIT_LIMIT: Final[int] = 1

DEVICE_INFO_SERVICE_TYPE: Final[bytes] = b'_device-info._tcp'
HTTP_SERVICE_TYPE: Final[bytes] = b'_http._tcp'
IP_SEPARATOR: Final[str] = '.'
LAST_OCTET_INDEX: Final[int] = -1
ASCII_ENCODING: Final[str] = 'ascii'
HTTP_OK_RESPONSE: Final[str] = "HTTP/1.1 200 OK"
ST_HEADER_PREFIX: Final[str] = 'ST:'
WINDOWS_DEVICE_TYPE: Final[str] = "Windows/SMB Device"

CRLF: Final[str] = "\r\n"
STRUCT_PACK_FORMAT: Final[str] = '>HHHHHH'