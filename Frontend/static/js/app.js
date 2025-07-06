const socket = io();

// UI Elements
const statusText = document.getElementById("statusText");
const progressContainer = document.getElementById("progressContainer");
const progressBar = document.getElementById("progressBar");
const progressText = document.getElementById("progressText");
const logs = document.getElementById("logs");
const logEntries = document.getElementById("logEntries");
const devicesContainer = document.getElementById("devicesContainer");
const deviceCount = document.getElementById("deviceCount");

let discoveredDevices = [];
let isScanning = false;

// Socket.IO event handlers
socket.on("scan_update", (data) => {
  addLogEntry(data.message, data.type);
  statusText.textContent = data.message;
});

socket.on("scan_progress", (data) => {
  const percent = data.progress;
  progressBar.style.width = percent + "%";
  progressText.textContent = `Processing device ${data.current} of ${data.total} (${percent}%)`;
});

socket.on("scan_complete", (data) => {
  addLogEntry(data.message, data.type);
  statusText.textContent = data.message;
  isScanning = false;
  progressContainer.style.display = "none";
  progressText.style.display = "none";
  loadDevices();
});

socket.on("scan_error", (data) => {
  addLogEntry(data.message, data.type);
  statusText.textContent = "Scan failed: " + data.message;
  isScanning = false;
  progressContainer.style.display = "none";
  progressText.style.display = "none";
});

function startScan() {
  if (isScanning) return;

  fetch("/api/scan/start", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
        return;
      }

      isScanning = true;
      statusText.textContent = "Starting scan...";

      // Clear previous results
      discoveredDevices = [];
      devicesContainer.innerHTML = "";
      updateDeviceCount();

      // Show progress elements
      progressContainer.style.display = "block";
      progressText.style.display = "block";
      logs.style.display = "block";
      progressBar.style.width = "0%";
      logEntries.innerHTML = "";
    })
    .catch((error) => {
      console.error("Error starting scan:", error);
      alert("Failed to start scan");
    });
}

async function loadDevices() {
  try {
    const response = await fetch("/api/devices");
    const data = await response.json();

    if (data.error) {
      addLogEntry(`Failed to load devices: ${data.error}`, "error");
      return;
    }

    console.log("Loaded devices:", data.devices);
    discoveredDevices = data.devices;

    // Clear the container completely
    devicesContainer.innerHTML = "";

    if (data.devices.length === 0) {
      // Show empty state
      devicesContainer.innerHTML = `
        <div class="empty-state">
          <svg fill="currentColor" viewBox="0 0 20 20">
            <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
          </svg>
          <p>No devices discovered yet. Start a scan to find devices on your network.</p>
        </div>
      `;
    } else {
      // Add devices to grid (process them sequentially to avoid race conditions)
      for (const device of data.devices) {
        await addDeviceToGrid(device);
      }
    }

    updateDeviceCount();
    addLogEntry(`Loaded ${data.devices.length} devices from database`, "info");
  } catch (error) {
    console.error("Error loading devices:", error);
    addLogEntry("Failed to load devices", "error");
  }
}

async function addDeviceToGrid(device) {
  const deviceCard = document.createElement("div");
  deviceCard.className = "device-card";

  const primaryMac = device.primary_mac;

  let portsHtml = "";
  if (primaryMac && primaryMac.ports && primaryMac.ports.length > 0) {
    portsHtml = `
      <div class="device-ports">
          <strong>Open Ports:</strong><br>
          ${primaryMac.ports
            .map(
              (port) =>
                `<span class="badge port">${port.port}/${port.protocol}</span>`
            )
            .join("")}
      </div>
    `;
  }

  let servicesHtml = "";
  if (
    primaryMac &&
    primaryMac.discoveries &&
    primaryMac.discoveries.length > 0
  ) {
    servicesHtml = `
      <div class="device-services">
          <strong>Services:</strong><br>
          ${primaryMac.discoveries
            .map(
              (discovery) =>
                `<span class="badge service">${
                  discovery.device_type || discovery.protocol
                }</span>`
            )
            .join("")}
      </div>
    `;
  }

  const deviceInfo = document.createElement("div");
  deviceInfo.className = "device-info";

  let iconElement;
  if (device.category && device.category.name) {
    try {
      iconElement = await window.svgLoader.createDeviceIcon(
        device.category.name
      );
    } catch (error) {
      console.warn(`Failed to load icon for ${device.category.name}:`, error);
      iconElement = document.createElement("div");
      iconElement.className = "device-icon";
      iconElement.innerHTML = `<div class="unknown-device">?</div>`;
    }
  } else {
    iconElement = document.createElement("div");
    iconElement.className = "device-icon";
    iconElement.innerHTML = `<div class="unknown-device">?</div>`;
  }

  const deviceName = document.createElement("div");
  deviceName.className = "device-name";
  deviceName.innerHTML = `<strong>${device.name}</strong>`;

  deviceInfo.appendChild(iconElement);
  deviceInfo.appendChild(deviceName);
  deviceCard.appendChild(deviceInfo);

  // if (portsHtml) {
  //   deviceCard.insertAdjacentHTML("beforeend", portsHtml);
  // }
  // if (servicesHtml) {
  //   deviceCard.insertAdjacentHTML("beforeend", servicesHtml);
  // }

  devicesContainer.appendChild(deviceCard);
}

function updateDeviceCount() {
  deviceCount.textContent = discoveredDevices.length;
}

function addLogEntry(message, type = "info") {
  const entry = document.createElement("div");
  entry.className = `log-entry ${type}`;
  entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  logEntries.appendChild(entry);
  logEntries.scrollTop = logEntries.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function () {
  loadDevices();
});
