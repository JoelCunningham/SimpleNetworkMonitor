import AddDeviceSelect from "../elements/add-device-select.js";
import NewDeviceForm from "../elements/new-device-form.js";
import PortalButton from "../elements/portal-button.js";
import {
  formatDateTime,
  formatPingTime,
  getDeviceName,
  getElement,
  getElements,
  getPortName,
  getServiceName,
  getStatusText,
  setElementText,
} from "../common.js";
import { UNK_FIELD } from "../constants.js";

class DeviceModal {
  constructor() {
    this.element = getElement("#deviceModal");
    this.title = getElement("#modalDeviceName");
    this.device = null;

    this.closeButton = getElement("#modalClose");
    this.portalButton = new PortalButton(getElement("#modalLinkBtn"));

    this.newDeviceButton = getElement("#newDeviceButton");
    this.addDeviceSelect = new AddDeviceSelect(getElement("#addDeviceSelect"));
    this.newDeviceForm = new NewDeviceForm(getElement("#deviceForm"));

    this.actionsBar = getElement(".actions-bar");
    this.generalSection = getElement("#generalSection");
    this.networkSection = getElement("#Network");
    this.generalArrow = getElement("#arrow-General");
    this.networkArrow = getElement("#arrow-Network");

    this.elementOnClick = event => {
      if (event.target === this.element) {
        this.clean();
      }
    };
    this.closeButtonOnClick = () => {
      this.clean();
    };
    this.newDeviceButtonOnClick = async () => {
      const onCancel = () => {
        this.actionsBar.style.display = "";
      };
      const onSuccess = device => {
        window.deviceManager.refreshDevices();
        this.populateGeneralInfo(device);
        this.title.textContent = getDeviceName(device);
        this.generalSection.style.display = "";
      };
      await this.newDeviceForm.init(this.device.macs, onCancel, onSuccess);
      this.actionsBar.style.display = "none";
    };
    this.documentOnKeyDown = event => {
      if (event.key === "Escape" && this.getStatus() === ModalStatus.OPEN) {
        this.clean();
      }
    };
  }

  /* Construction methods --------------------------------------------------- */

  async init(device) {
    this.device = device;
    
    this.clean();
    this.title.textContent = getDeviceName(device);
    
    this.portalButton.init(window.deviceManager.getDeviceHttpUrl(device));

    // Adjust sections for unknown devices
    if (!device.id) {
      this.actionsBar.style.display = "";
      this.generalSection.style.display = "none";
      this.networkSection.classList.remove("closed");
      this.networkArrow.classList.remove("closed");

      this.addDeviceSelect.init(window.deviceManager.getCurrentDevices());
    }

    this.populateGeneralInfo(device);
    this.populateNetworkInfo(device);
    this.populatePorts(device);
    this.populateServices(device);

    this.element.classList.add("show");
    document.body.style.overflow = "hidden";

    this.element.addEventListener("click", this.elementOnClick);
    this.closeButton.addEventListener("click", this.closeButtonOnClick);
    this.newDeviceButton.addEventListener("click", this.newDeviceButtonOnClick);
    document.addEventListener("keydown", this.documentOnKeyDown);
  }

  /* Populate methods -------------------------------------------------------- */

  populateGeneralInfo(device) {
    setElementText("#modalDeviceNameValue", device.name || UNK_FIELD);
    setElementText("#modalCategory", device.category?.name || UNK_FIELD);
    setElementText("#modalOwner", device.owner?.name || UNK_FIELD);
    setElementText("#modalLocation", device.location?.name || UNK_FIELD);
    setElementText("#modalModel", device.model || UNK_FIELD);
    setElementText("#modalStatus", getStatusText(device));
  }

  populateNetworkInfo(device) {
    const last_seen = device.primary_mac.last_seen || UNK_FIELD;
    const ping_time = device.primary_mac.ping_time_ms || UNK_FIELD;
    setElementText("#modalMacAddress", device.primary_mac.address || UNK_FIELD);
    setElementText("#modalIpAddress", device.primary_mac.last_ip || UNK_FIELD);
    setElementText("#modalHostname", device.primary_mac.hostname || UNK_FIELD);
    setElementText("#modalVendor", device.primary_mac.vendor || UNK_FIELD);
    setElementText("#modalOsGroup", device.primary_mac.os_guess || UNK_FIELD);
    setElementText("#modalTtl", device.primary_mac.ttl || UNK_FIELD);
    setElementText("#modalLastSeen", formatDateTime(last_seen) || UNK_FIELD);
    setElementText("#modalPingTime", formatPingTime(ping_time) || UNK_FIELD);
  }

  populatePorts(device) {
    const container = getElement("#modalPorts");
    const template = getElement("#portTagTemplate");
    const message = getElement(".no-data", container);

    const data = [];
    if (device.macs && Array.isArray(device.macs)) {
      device.macs.forEach(mac => {
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

    this.populateTags(data, container, template, message, getPortName);
  }

  populateServices(device) {
    const container = getElement("#modalServices");
    const template = getElement("#serviceTagTemplate");
    const message = getElement(".no-data", container);

    const data = [];
    if (device.macs && Array.isArray(device.macs)) {
      device.macs.forEach(mac => {
        if (mac.discoveries && Array.isArray(mac.discoveries)) {
          data.push(...mac.discoveries);
        }
      });
    }
    data.sort(
      (a, b) =>
        (a.device_name || "").localeCompare(b.device_name || "") ||
        (a.service_name || "").localeCompare(b.service_name || "")
    );

    this.populateTags(data, container, template, message, getServiceName);
  }

  populateTags(items, container, tagTemplate, noDataElem, getTagText) {
    if (!items || items.length === 0) {
      noDataElem.style.display = "";
      return;
    }
    noDataElem.style.display = "none";

    items.forEach(item => {
      const tag = tagTemplate.cloneNode(true);
      tag.textContent = getTagText(item);
      tag.style.display = "";
      tag.id = "";
      container.appendChild(tag);
    });
  }

  /* Action methods --------------------------------------------------------- */

  getStatus() {
    if (this.element.classList.contains("show")) {
      return ModalStatus.OPEN;
    }
    return ModalStatus.CLOSED;
  }

  toggleSectionCollapse(sectionId) {
    getElement(`#${sectionId}`).classList.toggle("closed");
    getElement(`#arrow-${sectionId}`).classList.toggle("closed");
  }

  /* Clean up methods ------------------------------------------------------- */

  clean() {
    if (this.portalButton.isInitialised()) this.portalButton.clean();
    if (this.newDeviceForm.isInitialised()) this.newDeviceForm.clean();
    if (this.addDeviceSelect.isInitialised()) this.addDeviceSelect.clean();

    this.actionsBar.style.display = "none";
    this.generalSection.style.display = "";

    this.generalSection.classList.remove("closed");
    this.generalArrow.classList.remove("closed");
    this.networkSection.classList.add("closed");
    this.networkArrow.classList.add("closed");

    getElements(".port-tag").forEach(tag => !tag.id && tag.remove());
    getElements(".service-tag").forEach(tag => !tag.id && tag.remove());
    getElements(".no-data").forEach(elem => {
      elem.style.display = "";
    });

    this.element.removeEventListener("click", this.elementOnClick);
    this.closeButton.removeEventListener("click", this.closeButtonOnClick);
    this.newDeviceButton.removeEventListener("click", this.newDeviceButtonOnClick);
    document.removeEventListener("keydown", this.documentOnKeyDown);

    this.element.classList.remove("show");
    document.body.style.overflow = "";
  }
}

const ModalStatus = {
  OPEN: "open",
  CLOSED: "closed",
};

// Create global instance
window.deviceModal = new DeviceModal();
