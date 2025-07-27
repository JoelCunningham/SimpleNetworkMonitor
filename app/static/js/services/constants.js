// Unknown names
export const UNK_FIELD = "-";
export const UNK_DEVICE = "Unknown Device";
export const UNK_PORT = "Unknown Port";
export const UNK_SERVICE = "Unknown Service";
export const UNK_STATUS = "Unknown";

// Titles
export const GRID_SIZE_TITLE = (size) =>
  `Change grid size (currently ${size} columns)`;
export const HTTP_LINK_TITLE = (http_address) =>
  `Open ${http_address} in new tab`;

// Scan status text
export const BASE_SCAN_TEXT = "Last scan: ";
export const SCANNING_TEXT = "Scanning now...";
export const NO_SCAN_TEXT = "Never";

// Device status text
export const STATUS_ONLINE = "Online";
export const STATUS_AWAY = "Away";
export const STATUS_OFFLINE = "Offline";

// Device status suffix
export const STATUS_NOW = "Just now";
export const STATUS_MINUTE = "m ago";
export const STATUS_HOUR = "h ago";
export const STATUS_DAY = "d ago";
export const STATUS_NEVER = "Never seen";

// Device grid
export const DEVICE_GRID_SIZES = [3, 4, 5];
export const DEFAULT_GRID_SIZE = DEVICE_GRID_SIZES[1];

// HTTP
export const HTTP = "http";
export const HTTPS = "https";
export const HTTP_PORT = 80;
export const HTTPS_PORT = 443;
export const SCHEME_DELIM = "://";
export const HTTP_PORTS = [HTTP_PORT, HTTPS_PORT, 8080, 8443];
export const HTTPS_PORTS = [HTTPS_PORT, 8443];

// File extensions
export const ICON_EXT = ".svg";

// API Endpoints
export const ENDPOINT_DEVICES = "/api/devices";
export const ENDPOINT_SCAN_STATUS = "/api/scan/status";
export const ENDPOINT_DEVICE_ICONS = "/api/icons/devices";

// Directories
export const DIRECTORY_DEVICES = "/static/icons/devices/";
