import { UNK_DEVICE, UNK_PORT, UNK_SERVICE, UNK_STATUS } from "./constants.js";

/* Formatting Functions -------------------------------------------- */

export function getPortName(port) {
  const portNumber = port.port || UNK_PORT;
  const service = port.service ? ` (${port.service})` : "";
  return `${portNumber}${service}`;
}

export function getServiceName(service) {
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

export function getStatusText(device) {
  const status = window.deviceManager.getDeviceStatusText(device);
  return status || UNK_STATUS;
}

export function getDeviceName(device) {
  return device.name || UNK_DEVICE;
}

export function formatDateTime(dateTimeString) {
  try {
    const date = new Date(dateTimeString);
    return date.toLocaleString();
  } catch (error) {
    return false;
  }
}

export function formatPingTime(pingTimeMs) {
  return pingTimeMs ? `${pingTimeMs}ms` : false;
}

/* JS Extentions -------------------------------------------------- */

export function getElement(selector, context = document) {
  const element = selector.startsWith("#")
    ? document.getElementById(selector.slice(1))
    : context.querySelector(selector);
  if (!element) throw new Error(`Element not found for selector: ${selector}`);
  return element;
}

export function getElements(selector, context = document) {
  if (selector.startsWith("#")) {
    throw new Error("getElements cannot use ID selector");
  }
  return context.querySelectorAll(selector);
}

export function setElementText(selector, text, context = document) {
  const element = getElement(selector, context);
  if (element) {
    element.textContent = text;
  }
}