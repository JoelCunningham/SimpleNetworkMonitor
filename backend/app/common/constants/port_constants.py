from typing import Final

# Port service constants
MAX_WORKERS: Final[int] = 20
OPEN_PORT_RESULT: Final[int] = 0
UNKNOWN_PORT_TEMPLATE: Final[str] = "unknown-{port}"
PORT_SERVICE_MAP: Final[dict[int, str]] = {
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
    8080: "http-alt",
    8443: "https-alt",
}