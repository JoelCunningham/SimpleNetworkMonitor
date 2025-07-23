// Unknown names
export const UNK_FIELD = "-";
export const UNK_DEVICE = "Unknown Device";
export const UNK_PORT = "Unknown Port";
export const UNK_SERVICE = "Unknown Service";
export const UNK_STATUS = "Unknown";

// Titles
export const HTTP_LINK_TITLE = (url) => `Open ${url} in new tab`;

// Scan status text
export const BASE_SCAN_TEXT = "Last scan: ";
export const SCANNING_TEXT = "Scanning now...";
export const NO_SCAN_TEXT = "Never";

// Device status text
export const STATUS_ONLINE = "Online";
export const STATUS_AWAY = "Away";
export const STATUS_OFFLINE = "Offline";

// Status value map
export const STATUS_LABELS = {
  online: STATUS_ONLINE,
  away: STATUS_AWAY,
  offline: STATUS_OFFLINE,
};

export const DEVICE_GRID_SIZES = [4, 5, 6];
export const DEFAULT_GRID_SIZE = DEVICE_GRID_SIZES[0];

// File extensions
export const ICON_EXT = ".svg";

// API Endpoints
export const ENDPOINT_DEVICES = "/api/devices";
export const ENDPOINT_SCAN_STATUS = "/api/scan/status";
export const ENDPOINT_DEVICE_ICONS = "/api/icons/devices";

// Directories
export const DIRECTORY_DEVICES = "/static/icons/devices/";
