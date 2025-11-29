from typing import Final

# Ping service constants
PLATFORM_WINDOWS: Final[str] = "Windows"
PLATFORM_LINUX: Final[str] = "Linux"
PLATFORM_MACOS: Final[str] = "Darwin"
SUCCESSFUL_PING_EXIT_CODE: Final[int] = 0
TTL_REGEX: Final[str] = r'[tT][tT][lL][=](\d+)'
ROUTER_TTL_TEMPLATE: Final[str] = "{os_name} (via router)"
UNKNOWN_OS_TEMPLATE: Final[str] = "Unknown (TTL: {ttl})"
TTL_OS_MAPPING: Final[dict[int, str]] = {
    30: "Android",
    32: "Windows 95/98/ME",
    60: "Other Linux",
    64: "Linux/Unix/macOS",
    128: "Windows XP/Vista/7/8/10/11",
    255: "Cisco/Network Device",
}