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
  getDeviceStatus(device) {
    if (!device.primary_mac || !device.primary_mac.last_seen) {
      return "offline";
    }

    const lastSeen = new Date(device.primary_mac.last_seen);
    const now = new Date();
    const minutesSinceLastSeen = (now - lastSeen) / 60000;

    if (minutesSinceLastSeen < 5) {
      return "online";
    } else if (minutesSinceLastSeen < 10) {
      return "away";
    } else {
      return "offline";
    }
  }

  // Format last seen time for display
  getLastSeenText(device) {
    if (!device.primary_mac || !device.primary_mac.last_seen) {
      return "Never seen";
    }

    const lastSeen = new Date(device.primary_mac.last_seen);
    const now = new Date();
    const minutesSinceLastSeen = (now - lastSeen) / (1000 * 60);

    if (minutesSinceLastSeen < 1) {
      return "Just now";
    } else if (minutesSinceLastSeen < 60) {
      return `${Math.floor(minutesSinceLastSeen)}m ago`;
    } else if (minutesSinceLastSeen < 1440) {
      return `${Math.floor(minutesSinceLastSeen / 60)}h ago`;
    } else {
      return `${Math.floor(minutesSinceLastSeen / 1440)}d ago`;
    }
  }

  // Check if device has HTTP ports and return appropriate URL
  getDeviceHttpUrl(device) {
    if (!device.primary_mac || !device.primary_mac.last_ip) {
      return null;
    }

    const ip = device.primary_mac.last_ip;
    let httpPorts = [];

    if (device.macs && Array.isArray(device.macs)) {
      device.macs.forEach((mac) => {
        if (mac.ports && Array.isArray(mac.ports)) {
          mac.ports.forEach((port) => {
            if (port && typeof port === "object") {
              const portNumber = port.port;
              const service = port.service?.toLowerCase() || "";

              if (
                portNumber === 80 ||
                portNumber === 8080 ||
                portNumber === 443 ||
                portNumber === 8443 ||
                service.includes("http")
              ) {
                httpPorts.push({
                  port: portNumber,
                  isHttps:
                    portNumber === 443 ||
                    portNumber === 8443 ||
                    service.includes("https"),
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
      if (a.port === 80) return -1;
      if (b.port === 80) return 1;
      if (a.port === 443) return -1;
      if (b.port === 443) return 1;
      return a.port - b.port;
    });

    const selectedPort = sortedPorts[0];
    const protocol = selectedPort.isHttps ? "https" : "http";
    const portSuffix =
      (selectedPort.port === 80 && !selectedPort.isHttps) ||
      (selectedPort.port === 443 && selectedPort.isHttps)
        ? ""
        : `:${selectedPort.port}`;

    return `${protocol}://${ip}${portSuffix}`;
  }

  async updateDeviceDisplay(devices = this.devices) {
    if (!devices || devices.length === 0) return;

    this.devices = devices;
    this.devicesGrid.innerHTML = "";

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
      const status = this.getDeviceStatus(device);
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
    const deviceCard = document.createElement("div");
    deviceCard.className = `device-card ${status}`;

    // Use MAC address as identifier
    if (device.primary_mac && device.primary_mac.address) {
      deviceCard.setAttribute("data-mac-address", device.primary_mac.address);
    }

    // Add last seen time for hover tooltip
    const lastSeenText = this.getLastSeenText(device);
    deviceCard.setAttribute("data-last-seen", lastSeenText);

    const deviceInfo = document.createElement("div");
    deviceInfo.className = "device-info";

    const iconElement = document.createElement("div");
    iconElement.className = "device-icon";

    if (device.category && device.category.name) {
      let svgContent = null;
      if (window.svgLoader.isIconCached(device.category.name)) {
        svgContent = window.svgLoader.getDeviceIcon(device.category.name);
      } else {
        svgContent = await window.svgLoader.getDeviceIconAsync(
          device.category.name
        );
      }

      if (svgContent) {
        iconElement.innerHTML = svgContent;
      } else {
        iconElement.innerHTML = `<div class="unknown-device">?</div>`;
      }
    } else {
      iconElement.innerHTML = `<div class="unknown-device">?</div>`;
    }

    const deviceName = document.createElement("div");
    deviceName.className = "device-name";
    deviceName.innerHTML = `<strong>${device.name}</strong>`;

    deviceInfo.appendChild(iconElement);
    deviceInfo.appendChild(deviceName);
    deviceCard.appendChild(deviceInfo);

    const httpUrl = this.getDeviceHttpUrl(device);
    if (httpUrl) {
      const linkButton = document.createElement("button");
      linkButton.className = "device-link-btn";
      linkButton.title = `Open ${httpUrl} in new tab`;
      linkButton.innerHTML = `
      <img
      src="/static/icons/external-link.svg"
      alt="Open device portal"
      class="external-link-icon"
      />
      `;

      linkButton.addEventListener("click", (e) => {
        e.stopPropagation(); // Prevent opening device modal
        window.open(httpUrl, "_blank");
      });

      deviceCard.appendChild(linkButton);
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

    // Update button title to show current grid size
    const updateButtonTitle = () => {
      gridSizeBtn.title = `Change grid size (currently ${this.currentGridSize} columns)`;
    };
    updateButtonTitle();

    // Add click event listener
    gridSizeBtn.addEventListener("click", () => {
      // Cycle to next grid size
      const currentIndex = DEVICE_GRID_SIZES.indexOf(this.currentGridSize);
      const nextIndex = (currentIndex + 1) % DEVICE_GRID_SIZES.length;
      this.currentGridSize = DEVICE_GRID_SIZES[nextIndex];

      // Update button title
      updateButtonTitle();

      // Update the device grid
      const gridClass = `device-grid grid-${this.currentGridSize}`;
      this.devicesGrid.className = gridClass;

      // Add visual feedback
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
} from "../constants.js";
