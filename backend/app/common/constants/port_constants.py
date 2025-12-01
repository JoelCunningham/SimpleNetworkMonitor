from typing import Final

# Port service constants
MAX_WORKERS: Final[int] = 20
OPEN_PORT_RESULT: Final[int] = 0
UNKNOWN_PORT_NAME: Final[str] = "unknown"
TCP_PROTOCOL: Final[str] = "tcp"
UDP_PROTOCOL: Final[str] = "udp"
PORT_SERVICE_MAP: Final[dict[int, str]] = {
    # File Transfer
    20: "ftp-data",
    21: "ftp",
    69: "tftp",
    
    # Remote Access
    22: "ssh",
    23: "telnet",
    3389: "rdp",
    5900: "vnc",
    5901: "vnc-1",
    
    # Email
    25: "smtp",
    110: "pop3",
    143: "imap",
    465: "smtps",
    587: "smtp-submission",
    993: "imaps",
    995: "pop3s",
    
    # Web
    80: "http",
    443: "https",
    8000: "http-alt",
    8080: "http-proxy",
    8443: "https-alt",
    8888: "http-alt",
    
    # DNS
    53: "dns",
    
    # Directory Services
    389: "ldap",
    636: "ldaps",
    
    # Windows Services
    135: "msrpc",
    139: "netbios-ssn",
    445: "microsoft-ds",
    
    # Databases
    1433: "mssql",
    3306: "mysql",
    5432: "postgresql",
    6379: "redis",
    9200: "elasticsearch",
    9300: "elasticsearch-cluster",
    27017: "mongodb",
    27018: "mongodb-shard",
    27019: "mongodb-config",
    
    # Message Queues
    5672: "amqp",
    15672: "rabbitmq-mgmt",
    9092: "kafka",
    61616: "activemq",
    
    # VPN
    1194: "openvpn",
    1723: "pptp",
    
    # Monitoring & Management
    161: "snmp",
    162: "snmp-trap",
    9090: "prometheus",
    3000: "grafana",
    
    # Container & Orchestration
    2375: "docker",
    2376: "docker-tls",
    8500: "consul",
    
    # Other Common
    1900: "ssdp",
    5353: "mdns",
    11211: "memcached",
}