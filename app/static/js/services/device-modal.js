import { initSelect, cleanSelect } from "../elements/select.js";

class DeviceModal {
  constructor() {
    this.modal = document.getElementById("deviceModal");
    this.modalClose = document.getElementById("modalClose");
    this.currentDevice = null;

    // Initialize the modal close listeners
    this.modalClose.addEventListener("click", () => {
      this._close();
    });
    this.modal.addEventListener("click", (event) => {
      if (event.target === this.modal) {
        this._close();
      }
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && this.modal.classList.contains("show")) {
        this._close();
      }
    });

    // Initialize device card click listeners
    document.addEventListener("click", (event) => {
      const deviceCard = event.target.closest(".device-card");
      if (deviceCard) {
        const macAddress = deviceCard.getAttribute("data-mac-address");
        this.initDeviceModal(macAddress);
      }
    });
  }

  async initDeviceModal(macAddress) {
    const device = window.deviceManager.devices.find(
      (d) => d.primary_mac && d.primary_mac.address === macAddress
    );
    this.currentDevice = device;
    this._populateModal(device);
    this._populateAddDeviceDropdown();
    this._open();
  }

  _populateAddDeviceDropdown() {
    const select = document.getElementById("addDeviceSelect");
    const devices = window.deviceManager.devices || [];

    let options = [
      ...devices
        .filter((device) => device.id && device.name)
        .map((device) => ({ value: device.id, label: device.name })),
    ];

    options = [
      { value: "1", label: "Device 1" },
      { value: "2", label: "Device 2" },
    ];

    const onChange = (value) => {
      if (value) {
        // TODO: Implement logic for adding to device
      }
    };

    this.select = initSelect(select, options, onChange, "Add to device");
  }

  toggleSectionCollapse(sectionId) {
    const section = document.getElementById(sectionId);
    const arrow = document.getElementById(`arrow-${sectionId}`);

    const isClosed = section.classList.contains("closed");

    arrow.classList.toggle("closed", !isClosed);
    section.classList.toggle("closed", !isClosed);
  }

  _populateModal(device) {
    // Set modal title
    document.getElementById("modalDeviceName").textContent =
      device.name || UNK_DEVICE;

    // Handle HTTP link button
    const modalLinkBtn = document.getElementById("modalLinkBtn");
    const httpUrl = window.deviceManager.getDeviceHttpUrl(device);
    if (httpUrl && modalLinkBtn) {
      modalLinkBtn.style.display = "flex";
      modalLinkBtn.title = HTTP_LINK_TITLE(httpUrl);

      const newLinkBtn = modalLinkBtn.cloneNode(true);
      modalLinkBtn.parentNode.replaceChild(newLinkBtn, modalLinkBtn);

      newLinkBtn.addEventListener("click", (e) => {
        e.preventDefault();
        window.open(httpUrl, "_blank");
      });
    } else if (modalLinkBtn) {
      modalLinkBtn.style.display = "none";
    }

    // Adjust sections for unknown devices
    if (!device.id) this._formatUnknownDevice();

    // General Information
    document.getElementById("modalDeviceNameValue").textContent =
      device.name || UNK_FIELD;
    document.getElementById("modalCategory").textContent =
      device.category?.name || UNK_FIELD;
    document.getElementById("modalOwner").textContent =
      device.owner?.name || UNK_FIELD;
    document.getElementById("modalLocation").textContent =
      device.location?.name || UNK_FIELD;
    document.getElementById("modalModel").textContent =
      device.model || UNK_FIELD;
    document.getElementById("modalStatus").textContent =
      this._getStatusText(device);

    // Network Information
    const primaryMac = device.primary_mac;
    document.getElementById("modalMacAddress").textContent =
      primaryMac.address || UNK_FIELD;
    document.getElementById("modalIpAddress").textContent =
      primaryMac.last_ip || UNK_FIELD;
    document.getElementById("modalHostname").textContent =
      primaryMac.hostname || UNK_FIELD;
    document.getElementById("modalVendor").textContent =
      primaryMac.vendor || UNK_FIELD;
    document.getElementById("modalOsGuess").textContent =
      primaryMac.os_guess || UNK_FIELD;
    document.getElementById("modalTtl").textContent =
      primaryMac.ttl || UNK_FIELD;
    document.getElementById("modalLastSeen").textContent =
      this._formatDateTime(primaryMac.last_seen) || UNK_FIELD;
    document.getElementById("modalPingTime").textContent =
      this._formatPingTime(primaryMac.ping_time) || UNK_FIELD;

    // Ports and Services
    this._populatePorts(device);
    this._populateServices(device);
  }

  _populatePorts(device) {
    const container = document.getElementById("modalPorts");
    const template = document.getElementById("portTagTemplate");
    const message = container.querySelector(".no-data");

    const data = [];
    if (device.macs && Array.isArray(device.macs)) {
      device.macs.forEach((mac) => {
        if (mac.ports && Array.isArray(mac.ports)) {
          data.push(...mac.ports);
        }
      });
    }
    data.sort(
      (a, b) =>
        (a.protocol || "").localeCompare(b.protocol || "") ||
        (a.port || 0) - (b.port || 0)
    );

    this._populateTags(data, container, template, message, this._getPortName);
  }

  _populateServices(device) {
    const container = document.getElementById("modalServices");
    const template = document.getElementById("serviceTagTemplate");
    const message = container.querySelector(".no-data");
    const data = [];

    if (device.macs && Array.isArray(device.macs)) {
      device.macs.forEach((mac) => {
        if (mac.discoveries && Array.isArray(mac.discoveries)) {
          data.push(...mac.discoveries);
        }
      });
    }

    this._populateTags(
      data,
      container,
      template,
      message,
      this._getServiceName
    );
  }

  _open() {
    this.modal.classList.add("show");
    document.body.style.overflow = "hidden"; // Prevent background scrolling
  }

  _close() {
    const select = document.getElementById("addDeviceSelect");
    cleanSelect(select);

    this.modal.classList.remove("show");
    document.body.style.overflow = ""; // Restore scrolling
    this.currentDevice = null;
  }

  _getPortName(port) {
    const portNumber = port.port || UNK_PORT;
    const service = port.service ? ` (${port.service})` : "";
    return `${portNumber}${service}`;
  }

  _getServiceName(service) {
    const name = service.device_name || service.device_type || UNK_SERVICE;
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
    return serviceDetails.length > 0
      ? `${name} (${serviceDetails.join(", ")})`
      : name;
  }

  _getStatusText(device) {
    const status = window.deviceManager.getDeviceStatusText(device);
    return status || UNK_STATUS;
  }

  _formatDateTime(dateTimeString) {
    try {
      const date = new Date(dateTimeString);
      return date.toLocaleString();
    } catch (error) {
      return false;
    }
  }

  _formatPingTime(pingTimeMs) {
    return pingTimeMs ? `${pingTimeMs}ms` : false;
  }

  _populateTags(items, container, tagTemplate, noDataElem, getTagText) {
    // Remove old tags except the template and no-data
    const tagTemplateSelector = `.${tagTemplate.className}:not(#${tagTemplate.id})`;
    container.querySelectorAll(tagTemplateSelector).forEach((e) => e.remove());
    container.querySelectorAll(".protocol-section").forEach((e) => e.remove());

    // If no items, show no-data message
    if (!items || items.length === 0) {
      if (noDataElem) noDataElem.style.display = "";
      return;
    }
    if (noDataElem) noDataElem.style.display = "none";

    // Create tags for each item
    items.forEach((item) => {
      const tag = tagTemplate.cloneNode(true);
      tag.textContent = getTagText(item);
      tag.style.display = "";
      tag.id = "";
      container.appendChild(tag);
    });
  }

  _formatUnknownDevice() {
    const actionsBar = document.querySelector(".actions-bar");
    const generalSection = document.getElementById("generalSection");
    const networkSection = document.getElementById("Network");
    const networkArrow = document.getElementById("arrow-Network");

    actionsBar.style.display = "";
    generalSection.style.display = "none";
    networkSection.classList.remove("closed");
    networkArrow.classList.remove("closed");
  }
}

// Create global instance
window.deviceModal = new DeviceModal();

import {
  UNK_FIELD,
  UNK_DEVICE,
  UNK_PORT,
  UNK_SERVICE,
  UNK_STATUS,
  HTTP_LINK_TITLE,
} from "./constants.js";
