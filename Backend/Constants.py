from Backend.Objects.PingCommand import PingCommand

# ============================================================================
# SYSTEM & PLATFORM CONSTANTS
# ============================================================================

# Platform Identifiers
PLATFORM_WINDOWS = "Windows"
PLATFORM_LINUX = "Linux"
PLATFORM_MACOS = "Darwin"

# Configuration
DEFAULT_CONFIG_PATH = "config.json"

# Concurrency
MAX_WORKERS = 20

# Encoding & Buffer Settings
ASCII_ENCODING = 'ascii'
DEFAULT_ENCODING = 'utf-8'
ENCODING_ERROR_HANDLING = 'ignore'
SOCKET_BUFFER_SIZE = 1024

# Durations
DB_POOL_RECYCLE_TIME = 3600  # 1 hour

# ============================================================================
# NETWORK PORTS & SERVICES
# ============================================================================

# Individual Port Definitions
SSH_PORT = 22
UPNP_PORT = 1900
MDNS_PORT = 5353
HTTPS_PORT = 443
NETBIOS_PORT = 137

# Port Collections
HTTP_PORTS = [80, 443, 8080, 8443]
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 
    993, 995, 1723, 3389, 5900, 8080
]

# Port-to-Service Mapping
PORT_SERVICE_MAP = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    135: "msrpc",
    139: "netbios-ssn",
    143: "imap",
    443: "https",
    993: "imaps",
    995: "pop3s",
    1723: "pptp",
    3389: "rdp",
    5900: "vnc",
    8080: "http-alt"
}

# Port Scanning Constants
OPEN_PORT_RESULT = 0
UNKNOWN_PORT_TEMPLATE = "unknown-{port}"

# ============================================================================
# SERVICE DETECTION & PROTOCOLS
# ============================================================================

# Protocol Schemes
HTTP_SCHEME = "http"
HTTPS_SCHEME = "https"

# Service Names
SSH_SERVICE_NAME = "ssh"
HTTP_SERVICE_NAME = "http"
BANNER_SERVICE_NAMES = ["telnet", "smtp", "pop3", "imap", "ftp"]

# SSH Service Constants
DEFAULT_SSH_PRODUCT = "SSH Server"
SSH_BANNER_PREFIX = 'SSH-'
DEFAULT_VERSION = "Unknown"

# HTTP Service Constants
DEFAULT_HTTP_SERVER = 'Unknown HTTP Server'
SERVER_HEADER = 'Server'
USER_AGENT_HEADER = "User-Agent"
USER_AGENT_VALUE = 'NetworkMonitor/1.0'
HTTP_URL_TEMPLATE = "{protocol_scheme}://{ip_address}:{port}/"
HTTP_INFO_TEMPLATE = "Status: {status}"
HTTP_OK_RESPONSE = "HTTP/1.1 200 OK"

# Banner Service Constants
MAX_BANNER_LENGTH = 100

# ============================================================================
# NETWORK DISCOVERY PROTOCOLS
# ============================================================================

# UPnP/SSDP Constants
SSDP_REQUEST_LINE = "M-SEARCH * HTTP/1.1\r\n"
SSDP_HOST_HEADER = "HOST: 239.255.255.250:1900\r\n"
SSDP_MAN_HEADER = 'MAN: "ssdp:discover"\r\n'
SSDP_ST_HEADER = "ST: upnp:rootdevice\r\n"
SSDP_MX_PREFIX = "MX: "
UPNP_PROTOCOL_NAME = "upnp"
DEFAULT_UPNP_DEVICE_TYPE = "UPnP Device"
UPNP_SERVER_HEADER_PREFIX = 'SERVER:'
ST_HEADER_PREFIX = 'ST:'
UPNP_HEADER_SEPARATOR = ':'
UPNP_SPLIT_LIMIT = 1

# NetBIOS Constants
NETBIOS_TRANSACTION_ID = 0x1234
NETBIOS_QUERY_FLAGS = 0x0110
NETBIOS_QUESTIONS_COUNT = 1
NETBIOS_ANSWERS_COUNT = 0
NETBIOS_AUTHORITY_COUNT = 0
NETBIOS_ADDITIONAL_COUNT = 0
NETBIOS_NAME_LENGTH = b'\x20'
NETBIOS_WILDCARD = b'A' * 31 
NETBIOS_QUERY_SUFFIX = b'\x00\x00\x20\x00\x01'
NETBIOS_HEADER_LENGTH = 12
NETBIOS_PROTOCOL_NAME = "netbios"
WINDOWS_DEVICE_TYPE = "Windows/SMB Device"
NETBIOS_MIN_RESPONSE_LENGTH = 50
NETBIOS_MIN_WORD_LENGTH = 2
NETBIOS_MAX_NAME_LENGTH = 15

# mDNS Constants
MDNS_TRANSACTION_ID = 0x0000
MDNS_FLAGS = 0x0000
MDNS_QUESTIONS_COUNT = 1
MDNS_ANSWERS_COUNT = 0
MDNS_AUTHORITY_COUNT = 0
MDNS_ADDITIONAL_COUNT = 0
MDNS_SERVICE_QUERY = b'\x09_services\x07_dns-sd\x04_udp\x05local\x00\x00\x0c\x00\x01'
MDNS_HEADER_LENGTH = 12
HTTP_SERVICE_TYPE = b'_http._tcp'
DEVICE_INFO_SERVICE_TYPE = b'_device-info._tcp'
MDNS_PROTOCOL_NAME = "mdns"
MDNS_DEVICE_NAME_PREFIX = "mDNS-"
MDNS_DEVICE_TYPE = "mDNS/Bonjour Device"

# ============================================================================
# NETWORK UTILITIES & PING
# ============================================================================

# Ping Configuration
SUCCESSFUL_PING_EXIT_CODE = 0
PING_COMMANDS = {
    PLATFORM_WINDOWS: PingCommand("ping", "-n", "-w"),
    PLATFORM_LINUX: PingCommand("ping", "-c", "-W"),
    PLATFORM_MACOS: PingCommand("ping", "-c", "-W"),
}

# TTL (Time To Live) Constants
TTL_REGEX = r'[tT][tT][lL][=](\d+)'  # Windows: "TTL=64" or "TTL=128" # Linux/Mac: "ttl=64" or "ttl=128"
TTL_OS_MAPPING = {
    30: "Android",
    32: "Windows 95/98/ME",
    60: "Other Linux",
    64: "Linux/Unix/macOS", 
    128: "Windows XP/Vista/7/8/10/11",
    255: "Cisco/Network Device"
}
ROUTER_TTL_TEMPLATE = "{os_name} (via router)"
UNKNOWN_OS_TEMPLATE = "Unknown (TTL: {ttl})"

# ============================================================================
# MAC ADDRESS & VENDOR LOOKUP
# ============================================================================

# MAC Address Constants
BROADCAST_MAC_ADDRESS = "ff:ff:ff:ff:ff:ff"
MAC_ADDRESS_ATTR = "hwsrc"
MAC_OUI_LENGTH = 6

# MAC Vendor Fallback Mapping
MAC_VENDOR_FALLBACK_MAPPING = {
    "00:03:93": "Apple",
    "00:1A:11": "Google", 
    "00:0D:3A": "Microsoft",
    "00:07:AB": "Samsung",
    "00:03:47": "Intel",
    "00:27:19": "TP-Link",
    "00:09:5B": "Netgear",
    "00:06:25": "Linksys",
    "00:01:42": "Cisco"
}

# ============================================================================
# STRING CONSTANTS & TEMPLATES
# ============================================================================

# String Literals
CRLF = "\r\n"
IP_SEPARATOR = '.'
UNKNOWN_DEVICE_NAME = "Unknown Device"

# Binary & Struct Constants
STRUCT_PACK_FORMAT = '>HHHHHH'
LAST_OCTET_INDEX = -1