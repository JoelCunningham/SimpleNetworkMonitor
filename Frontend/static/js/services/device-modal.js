class DeviceModal {
  constructor() {
    this.modal = document.getElementById("deviceModal");
    this.modalClose = document.getElementById("modalClose");
    this.currentDevice = null;

    this.initializeModal();
  }

  initializeModal() {
    // Close modal when clicking the X button
    this.modalClose.addEventListener("click", () => {
      this.closeModal();
    });

    // Close modal when clicking outside the modal content
    this.modal.addEventListener("click", (event) => {
      if (event.target === this.modal) {
        this.closeModal();
      }
    });

    // Close modal when pressing ESC key
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && this.modal.classList.contains("show")) {
        this.closeModal();
      }
    });

    this.initializeDeviceCardListeners();
  }

  initializeDeviceCardListeners() {
    document.addEventListener("click", (event) => {
      const deviceCard = event.target.closest(".device-card");
      if (deviceCard) {
        const macAddress = deviceCard.getAttribute("data-mac-address");
        if (macAddress) {
          this.showDeviceDetails(macAddress);
        }
      }
    });
  }

  async showDeviceDetails(macAddress) {
    try {
      const device = window.deviceManager.devices.find(
        (d) => d.primary_mac && d.primary_mac.address === macAddress
      );
      if (!device) {
        console.error("Device not found with MAC address:", macAddress);
        return;
      }

      this.currentDevice = device;
      this.populateModal(device);
      this.openModal();
    } catch (error) {
      console.error("Error showing device details:", error);
    }
  }

  populateModal(device) {
    // Update modal title
    document.getElementById("modalDeviceName").textContent =
      device.name || "Unknown Device";

    // General Information
    document.getElementById("modalDeviceNameValue").textContent =
      device.name || "-";
    document.getElementById("modalCategory").textContent =
      device.category?.name || "-";
    document.getElementById("modalOwner").textContent =
      device.owner?.name || "-";
    document.getElementById("modalLocation").textContent =
      device.location?.name || "-";
    document.getElementById("modalModel").textContent = device.model || "-";
    document.getElementById("modalStatus").textContent =
      this.getStatusText(device);

    // Network Information
    const primaryMac = device.primary_mac;
    if (primaryMac) {
      document.getElementById("modalMacAddress").textContent =
        primaryMac.address || "-";
      document.getElementById("modalIpAddress").textContent =
        primaryMac.last_ip || "-";
      document.getElementById("modalHostname").textContent =
        primaryMac.hostname || "-";
      document.getElementById("modalVendor").textContent =
        primaryMac.vendor || "-";
      document.getElementById("modalOsGuess").textContent =
        primaryMac.os_guess || "-";
      document.getElementById("modalTtl").textContent = primaryMac.ttl || "-";
      document.getElementById("modalLastSeen").textContent =
        this.formatDateTime(primaryMac.last_seen);
      document.getElementById("modalPingTime").textContent =
        primaryMac.ping_time_ms ? `${primaryMac.ping_time_ms}ms` : "-";
    } else {
      document.getElementById("modalMacAddress").textContent = "-";
      document.getElementById("modalIpAddress").textContent = "-";
      document.getElementById("modalHostname").textContent = "-";
      document.getElementById("modalVendor").textContent = "-";
      document.getElementById("modalOsGuess").textContent = "-";
      document.getElementById("modalTtl").textContent = "-";
      document.getElementById("modalLastSeen").textContent = "-";
      document.getElementById("modalPingTime").textContent = "-";
    }

    this.populatePorts(device);
    this.populateServices(device);
  }

  populatePorts(device) {
    const portsContainer = document.getElementById("modalPorts");

    const allPorts = [];
    if (device.macs && Array.isArray(device.macs)) {
      device.macs.forEach((mac) => {
        if (mac.ports && Array.isArray(mac.ports)) {
          allPorts.push(...mac.ports);
        }
      });
    }

    if (allPorts.length === 0) {
      portsContainer.innerHTML = '<p class="no-data">No open ports found</p>';
      return;
    }

    const portsByProtocol = {};
    allPorts.forEach((port) => {
      if (!port || typeof port !== "object") return;

      const protocol = port.protocol || "tcp";
      if (!portsByProtocol[protocol]) {
        portsByProtocol[protocol] = [];
      }
      portsByProtocol[protocol].push(port);
    });

    Object.keys(portsByProtocol).forEach((protocol) => {
      portsByProtocol[protocol].sort((a, b) => (a.port || 0) - (b.port || 0));
    });

    let portsHtml = "";

    Object.keys(portsByProtocol)
      .sort()
      .forEach((protocol) => {
        const ports = portsByProtocol[protocol];

        if (Object.keys(portsByProtocol).length > 1) {
          portsHtml += `<div class="protocol-section">`;
          portsHtml += `<h5 style="margin: 1rem 0 0.5rem 0; color: var(--text-muted); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">${protocol.toUpperCase()} Ports</h5>`;
          portsHtml += `<div class="ports-container">`;
        }

        ports.forEach((port) => {
          if (!port || typeof port !== "object") return;

          const portNumber = port.port || "Unknown";
          const service = port.service ? ` (${port.service})` : "";

          portsHtml += `<span class="port-tag" style="background: #17a2b8; color: white;">${portNumber}${service}</span>`;
        });

        if (Object.keys(portsByProtocol).length > 1) {
          portsHtml += `</div></div>`;
        }
      });

    if (Object.keys(portsByProtocol).length === 1) {
      portsHtml = `<div class="ports-container">${portsHtml}</div>`;
    }

    portsContainer.innerHTML = portsHtml;
  }

  populateServices(device) {
    const servicesContainer = document.getElementById("modalServices");

    const allServices = [];
    if (device.macs && Array.isArray(device.macs)) {
      device.macs.forEach((mac) => {
        if (mac.discoveries && Array.isArray(mac.discoveries)) {
          allServices.push(...mac.discoveries);
        }
      });
    }

    if (allServices.length === 0) {
      servicesContainer.innerHTML =
        '<p class="no-data">No services discovered</p>';
      return;
    }

    let servicesHtml = '<div class="services-container">';

    allServices.forEach((service) => {
      if (!service || typeof service !== "object") return;

      const serviceName =
        service.device_name || service.device_type || "Unknown Service";
      let serviceDetails = [];

      if (service.manufacturer) {
        serviceDetails.push(`Mfg: ${service.manufacturer}`);
      }
      if (service.model) {
        serviceDetails.push(`Model: ${service.model}`);
      }
      if (service.protocol) {
        serviceDetails.push(`via ${service.protocol}`);
      }

      const serviceText =
        serviceDetails.length > 0
          ? `${serviceName} (${serviceDetails.join(", ")})`
          : serviceName;

      servicesHtml += `<span class="service-tag">${serviceText}</span>`;
    });

    servicesHtml += "</div>";
    servicesContainer.innerHTML = servicesHtml;
  }

  getStatusText(device) {
    const status = window.deviceManager.getDeviceStatus(device);
    switch (status) {
      case "online":
        return "Online";
      case "away":
        return "Away";
      case "offline":
        return "Offline";
      default:
        return "Unknown";
    }
  }

  formatDateTime(dateTimeString) {
    if (!dateTimeString) return "-";

    try {
      const date = new Date(dateTimeString);
      return date.toLocaleString();
    } catch (error) {
      return dateTimeString;
    }
  }

  openModal() {
    this.modal.classList.add("show");
    document.body.style.overflow = "hidden"; // Prevent background scrolling
  }

  closeModal() {
    this.modal.classList.remove("show");
    document.body.style.overflow = ""; // Restore scrolling
    this.currentDevice = null;
  }
}

// Create global instance
window.deviceModal = new DeviceModal();
