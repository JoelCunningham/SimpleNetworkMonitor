class DeviceManager {
  constructor() {
    this.devices = [];
    this.devicesGrid = document.getElementById("devicesGrid");
    this.emptyState = document.getElementById("emptyState");
    this.deviceCount = document.getElementById("deviceCount");
    this.currentGridSize = DEFAULT_GRID_SIZE;
  }

  // Update devices
  async refreshDevices() {
    const response = await fetch(ENDPOINT_DEVICES);
    const data = await response.json();
    if (data.devices) {
      window.deviceManager.updateDeviceDisplay(data.devices);
    }
  }

  // Device status calculation
  getDeviceStatusText(device) {
    if (!device.primary_mac || !device.primary_mac.last_seen) {
      return STATUS_OFFLINE;
    }

    const now = new Date();
    const lastSeen = new Date(device.primary_mac.last_seen);
    const minutesSinceLastSeen = (now - lastSeen) / 60000;

    if (minutesSinceLastSeen < 5) {
      return STATUS_ONLINE;
    } else if (minutesSinceLastSeen < 10) {
      return STATUS_AWAY;
    } else {
      return STATUS_OFFLINE;
    }
  }

  // Format last seen time for display
  getLastSeenText(device) {
    if (!device.primary_mac || !device.primary_mac.last_seen) {
      return STATUS_NEVER;
    }

    const now = new Date();
    const lastSeen = new Date(device.primary_mac.last_seen);
    const minutesSinceLastSeen = (now - lastSeen) / 60000;

    if (minutesSinceLastSeen < 1) {
      return STATUS_NOW;
    } else if (minutesSinceLastSeen < 60) {
      return `${Math.floor(minutesSinceLastSeen)}${STATUS_MINUTE}`;
    } else if (minutesSinceLastSeen < 1440) {
      return `${Math.floor(minutesSinceLastSeen / 60)}${STATUS_HOUR}`;
    } else {
      return `${Math.floor(minutesSinceLastSeen / 1440)}${STATUS_DAY}`;
    }
  }

  // Check if device has HTTP ports and return appropriate URL
  getDeviceHttpUrl(device) {
    if (!device.primary_mac || !device.primary_mac.last_ip) {
      return null;
    }

    const ip = device.primary_mac.last_ip;
    let httpPorts = [];

    if (device.macs) {
      device.macs.forEach((mac) => {
        if (mac.ports) {
          mac.ports.forEach((port) => {
            if (port) {
              const portNumber = port.port;
              const service = port.service?.toLowerCase() || "";
              if (HTTP_PORTS.includes(portNumber) || service.includes(HTTP)) {
                httpPorts.push({
                  port: portNumber,
                  isHttps:
                    HTTPS_PORTS.includes(portNumber) || service.includes(HTTPS),
                });
              }
            }
          });
        }
      });
    }

    if (httpPorts.length === 0) {
      return null;
    }

    // Prefer HTTP, then HTTPS, then others
    const sortedPorts = httpPorts.sort((a, b) => {
      if (!a.isHttps && b.isHttps) return -1;
      if (a.isHttps && !b.isHttps) return 1;
      if (a.port === HTTP_PORT) return -1;
      if (b.port === HTTP_PORT) return 1;
      if (a.port === HTTPS_PORT) return -1;
      if (b.port === HTTPS_PORT) return 1;
      return a.port - b.port;
    });

    const selectedPort = sortedPorts[0];
    const protocol = selectedPort.isHttps ? HTTPS : HTTP;
    const portSuffix =
      (selectedPort.port === HTTP_PORT && !selectedPort.isHttps) ||
      (selectedPort.port === HTTPS_PORT && selectedPort.isHttps)
        ? ""
        : `:${selectedPort.port}`;

    return `${protocol}${SCHEME_DELIM}${ip}${portSuffix}`;
  }

  async updateDeviceDisplay(devices = this.devices) {
    if (!devices || devices.length === 0) return;

    this.devices = devices;
    const template = document.getElementById("deviceCardTemplate");
    this.devicesGrid.innerHTML = "";
    if (template) {
      this.devicesGrid.appendChild(template);
    }

    const gridClass = `device-grid grid-${this.currentGridSize}`;
    this.devicesGrid.className = gridClass;

    const sortedDevices = [...devices].sort((a, b) => {
      const lastSeenA = a.primary_mac?.last_seen
        ? new Date(a.primary_mac.last_seen)
        : new Date(0);
      const lastSeenB = b.primary_mac?.last_seen
        ? new Date(b.primary_mac.last_seen)
        : new Date(0);
      return lastSeenB - lastSeenA;
    });

    // Add all devices to the single grid
    for (const device of sortedDevices) {
      const status = this.getDeviceStatusText(device);
      const deviceCard = await this.createDeviceCard(device, status);
      this.devicesGrid.appendChild(deviceCard);
    }

    // Update total device count
    this.deviceCount.textContent = devices.length;

    // Show/hide empty state
    if (devices.length === 0) {
      this.emptyState.style.display = "block";
      this.devicesGrid.style.display = "none";
    } else {
      this.emptyState.style.display = "none";
      this.devicesGrid.style.display = "grid";
    }
  }

  async createDeviceCard(device, status) {
    const template = document.getElementById("deviceCardTemplate");
    const deviceCard = template.cloneNode(true);
    deviceCard.style.display = "";
    deviceCard.id = "";
    deviceCard.className = `device-card ${status.toLowerCase()}`;

    // Set MAC address and last seen
    if (device.primary_mac && device.primary_mac.address) {
      deviceCard.setAttribute("data-mac-address", device.primary_mac.address);
    }
    const lastSeenText = this.getLastSeenText(device);
    deviceCard.setAttribute("data-last-seen", lastSeenText);

    // Device icon
    const iconElement = deviceCard.querySelector(".device-icon");
    const unknownIcon = iconElement.querySelector(".unknown-device");
    if (device.category && device.category.name) {
      let icon = null;
      if (window.svgLoader.isIconCached(device.category.name)) {
        icon = window.svgLoader.getDeviceIcon(device.category.name);
      } else {
        icon = await window.svgLoader.getDeviceIconAsync(device.category.name);
      }
      iconElement.innerHTML = icon;
    } else {
      unknownIcon.style.display = "";
    }

    // Device name
    const deviceName = deviceCard.querySelector(".device-name strong");
    deviceName.textContent = device.name;

    // Device link button
    const httpUrl = this.getDeviceHttpUrl(device);
    const linkButton = deviceCard.querySelector(".device-link-btn");
    if (httpUrl) {
      linkButton.style.display = "";
      linkButton.title = HTTP_LINK_TITLE(httpUrl);
      linkButton.onclick = (e) => {
        e.stopPropagation();
        window.open(httpUrl, "_blank");
      };
    } else {
      linkButton.style.display = "none";
    }

    return deviceCard;
  }

  clearDevices() {
    this.devices = [];
    this.devicesGrid.innerHTML = "";
    this.deviceCount.textContent = "0";
  }

  initializeGridSize() {
    const gridSizeBtn = document.getElementById("gridSizeBtn");

    if (!gridSizeBtn) return;

    const updateButtonTitle = () => {
      gridSizeBtn.title = GRID_SIZE_TITLE(this.currentGridSize);
    };
    updateButtonTitle();

    gridSizeBtn.addEventListener("click", () => {
      const currentIndex = DEVICE_GRID_SIZES.indexOf(this.currentGridSize);
      const nextIndex = (currentIndex + 1) % DEVICE_GRID_SIZES.length;
      this.currentGridSize = DEVICE_GRID_SIZES[nextIndex];

      updateButtonTitle();

      const gridClass = `device-grid grid-${this.currentGridSize}`;
      this.devicesGrid.className = gridClass;

      gridSizeBtn.style.transform = "scale(0.95)";
      setTimeout(() => {
        gridSizeBtn.style.transform = "";
      }, 100);
    });
  }
}

// Create global instance
window.deviceManager = new DeviceManager();

import {
  DEFAULT_GRID_SIZE,
  DEVICE_GRID_SIZES,
  ENDPOINT_DEVICES,
  GRID_SIZE_TITLE,
  HTTP,
  HTTP_LINK_TITLE,
  HTTP_PORT,
  HTTP_PORTS,
  HTTPS,
  HTTPS_PORT,
  HTTPS_PORTS,
  SCHEME_DELIM,
  STATUS_AWAY,
  STATUS_DAY,
  STATUS_HOUR,
  STATUS_MINUTE,
  STATUS_NEVER,
  STATUS_NOW,
  STATUS_OFFLINE,
  STATUS_ONLINE,
} from "./constants.js";
