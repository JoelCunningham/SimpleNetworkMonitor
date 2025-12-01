from typing import Final

# Scan service constants
BANNER_SERVICE_NAMES: Final[list[str]] = ["telnet", "smtp", "pop3", "imap", "ftp"]

# Expanded list of most common TCP ports (top 100)
TCP_COMMON_PORTS: Final[list[int]] = [
    # Web services
    80, 443, 8080, 8443, 8000, 8888,
    # SSH/Telnet/Remote access
    21, 22, 23, 3389, 5900, 5901,
    # Email
    25, 110, 143, 465, 587, 993, 995,
    # DNS/DHCP
    53,
    # Database
    1433, 3306, 5432, 27017, 6379, 9200, 9300,
    # File sharing
    135, 139, 445,
    # VPN
    1194, 1723,
    # Messaging/Queue
    5672, 15672, 9092, 61616,
    # Other common services
    20, 389, 636, 873, 1521, 2049, 2181, 2375, 2376, 3000,
    3001, 3002, 3003, 4369, 5000, 5001, 5432, 5555, 5984,
    6000, 6001, 6379, 7000, 7001, 8001, 8002, 8080, 8081,
    8082, 8088, 8181, 8200, 8443, 8500, 8600, 9000, 9042,
    9090, 9091, 9092, 9093, 9200, 9300, 9418, 9999, 11211,
    27017, 27018, 27019, 50000, 50070
]

# Common UDP ports for scanning
UDP_COMMON_PORTS: Final[list[int]] = [
    53,      # DNS
    67, 68,  # DHCP
    69,      # TFTP
    123,     # NTP
    161, 162,  # SNMP
    500,     # IPSec
    514,     # Syslog
    4500,    # IPSec NAT
    # Note that ports 137, 138, 1900, and 5353 are excluded as they are handled by specific discovery services.
]

HTTP_PORTS: Final[list[int]] = [80, 443, 8080, 8443]
SSH_PORT: Final[int] = 22
MAX_MESSAGE_LENGTH: Final[int] = 80