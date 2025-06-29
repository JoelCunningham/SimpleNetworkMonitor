# Configuration
DEFAULT_CONFIG_PATH = "config.json"
DEFAULT_ENCODING = "utf-8"

# Network scanning
IP_ADDRESS_REGEX = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
MAC_ADDRESS_REGEX = r'^[0-9a-f]{12}$'
TTL_REGEX = r'[tT][tT][lL][=](\d+)' # Windows: "TTL=64" or "TTL=128" # Linux/Mac: "ttl=64" or "ttl=128"

# Network protocols
BROADCAST_MAC_ADDRESS = "ff:ff:ff:ff:ff:ff"
SUCCESSFUL_PING_EXIT_CODE = 0

# Platforms
PLATFORM_WINDOWS = "Windows"
PLATFORM_LINUX = "Linux"
PLATFORM_MACOS = "Darwin"

# Platform-specific ping commands
PING_COMMANDS = {
    PLATFORM_WINDOWS: {"cmd": "ping", "count_flag": "-n", "timeout_flag": "-w"},
    PLATFORM_LINUX: {"cmd": "ping", "count_flag": "-c", "timeout_flag": "-W"},
    PLATFORM_MACOS: {"cmd": "ping", "count_flag": "-c", "timeout_flag": "-W"}, 
}

# Database
DATABASE_POOL_RECYCLE_TIME = 3600  # 1 hour

# Network timeouts (in seconds)
DEFAULT_ARP_TIMEOUT = 0.5
DEFAULT_PING_TIMEOUT = 0.3

# Validation limits
MIN_IP_ADDRESS = 1
MAX_IP_ADDRESS = 254
MIN_TIMEOUT_MS = 1
MIN_THREADS = 1
MIN_PING_COUNT = 1

# Display formatting
SEPARATOR_LINE = "-" * 80
IP_COLUMN_WIDTH = 15
MAC_COLUMN_WIDTH = 17
DEVICE_NAME_COLUMN_WIDTH = 30

# Default values
UNKNOWN_DEVICE_NAME = "Unknown Device"
UNKNOWN_MAC_NAME = "Unknown"

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Messages
SCAN_INTERRUPTED_MESSAGE = "\nScan interrupted by user."
DEVICE_SCAN_FORMAT = "{ip:<15} - {mac:<17} - {name:<30} | ping: {ping:>4}ms | arp: {arp:>4}ms | host: {hostname:<20} | vendor: {vendor:<15} | os: {os_guess:<10}"
DEVICE_SCAN_FORMAT_ADVANCED = "{ip:<15} - {mac:<17} - {name:<30} | ping: {ping:>4}ms | arp: {arp:>4}ms | host: {hostname:<20} | vendor: {vendor:<15} | os: {os_guess:<10} | ports: {ports} | services: {services}"
NETWORK_SCAN_SUMMARY = "Found {count} responsive devices"
DEVICES_PROCESSED_SUMMARY = "Processed {count} devices:"

# Database messages
DB_ALREADY_INITIALIZED = "Database already initialized"
DB_NOT_INITIALIZED = "Database not initialized"
DB_INIT_FAILED = "Failed to initialize database: {error}"
DB_CLOSE_FAILED = "Failed to close database connection: {error}"

# Error messages
CONFIG_FILE_NOT_FOUND = "AppConfig file {filepath} does not exist."
CONFIG_INVALID = "Invalid configuration in {filepath}: {error}"
CONFIG_MISSING_FIELDS = "Missing required fields in {filepath}: {fields}"
UNSUPPORTED_OS = "Unsupported operating system: {system}"
PING_ERROR = "Ping error for {ip}: {error}"
ARP_ERROR = "ARP lookup error for {ip}: {error}"

# TTL-based OS detection
TTL_OS_MAPPING = {
    30: "Android",
    32: "Windows 95/98/ME",
    60: "Other Linux",
    64: "Linux/Unix/macOS", 
    128: "Windows XP/Vista/7/8/10/11",
    255: "Cisco/Network Device"
}

# Service detection
COMMON_PORTS = [
    22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 
    993, 995, 1723, 3389, 5900, 8080
]
HTTP_PORTS = [80, 443, 8080]
SSH_PORT = 22
BANNER_SERVICES = ["ftp", "smtp", "pop3", "imap"];
