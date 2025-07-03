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

socket.on("device_found", (device) => {
  addDeviceToGrid(device);
  discoveredDevices.push(device);
  updateDeviceCount();
});

socket.on("scan_complete", (data) => {
  addLogEntry(data.message, data.type);
  statusText.textContent = data.message;
  isScanning = false;
  progressContainer.style.display = "none";
  progressText.style.display = "none";
});

socket.on("scan_error", (data) => {
  addLogEntry(data.message, data.type);
  statusText.textContent = "Scan failed: " + data.message;
  isScanning = false;
  progressContainer.style.display = "none";
  progressText.style.display = "none";
});

// Functions
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

function addDeviceToGrid(device) {
  const deviceCard = document.createElement("div");
  deviceCard.className = "device-card";

  let portsHtml = "";
  if (device.ports && device.ports.length > 0) {
    portsHtml = `
            <div class="device-ports">
                <strong>Open Ports:</strong><br>
                ${device.ports
                  .map((port) => `<span class="badge port">${port}</span>`)
                  .join("")}
            </div>
        `;
  }

  let servicesHtml = "";
  if (device.services && device.services.length > 0) {
    servicesHtml = `
            <div class="device-services">
                <strong>Services:</strong><br>
                ${device.services
                  .map(
                    (service) => `<span class="badge service">${service}</span>`
                  )
                  .join("")}
            </div>
        `;
  }

  deviceCard.innerHTML = `
        <div class="device-ip">${device.ip_address}</div>
        <div class="device-info">
            ${
              device.mac_address
                ? `<div><strong>MAC:</strong> ${device.mac_address}</div>`
                : ""
            }
            ${
              device.hostname
                ? `<div><strong>Hostname:</strong> ${device.hostname}</div>`
                : ""
            }
            ${
              device.mac_vendor
                ? `<div><strong>Vendor:</strong> ${device.mac_vendor}</div>`
                : ""
            }
            ${
              device.os_guess
                ? `<div><strong>OS:</strong> ${device.os_guess}</div>`
                : ""
            }
            <div><strong>Response Time:</strong> ${device.ping_time_ms}ms</div>
            ${
              device.arp_time_ms > 0
                ? `<div><strong>ARP Time:</strong> ${device.arp_time_ms}ms</div>`
                : ""
            }
        </div>
        ${portsHtml}
        ${servicesHtml}
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
  startScan();
});
