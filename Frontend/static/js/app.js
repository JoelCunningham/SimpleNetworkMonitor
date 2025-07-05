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

function loadDevices() {
  fetch("/api/devices")
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        addLogEntry(`Failed to load devices: ${data.error}`, "error");
        return;
      }
      console.log("Loaded devices:", data.devices);
      discoveredDevices = data.devices;
      devicesContainer.innerHTML = "";

      data.devices.forEach((device) => {
        addDeviceToGrid(device);
      });

      updateDeviceCount();
      addLogEntry(
        `Loaded ${data.devices.length} devices from database`,
        "info"
      );
    })
    .catch((error) => {
      console.error("Error loading devices:", error);
      addLogEntry("Failed to load devices", "error");
    });
}

function addDeviceToGrid(device) {
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

  deviceCard.innerHTML = `
      <div class="device-info">
          <div><strong>${device.name}</strong></div>
          ${
            device.category && device.category.name
              ? `<img src="/static/icons/devices/${device.category.name.toLowerCase()}.svg"</div>`
              : "?"
          }
      </div>
    `;

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
