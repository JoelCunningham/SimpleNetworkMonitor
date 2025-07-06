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

// Device grid element
const devicesGrid = document.getElementById("devicesGrid");
const emptyState = document.getElementById("emptyState");

let discoveredDevices = [];
let isScanning = false;
let deviceUpdateInterval;

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
      devicesGrid.innerHTML = "";
      deviceCount.textContent = "0";

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

// Device status calculation
function getDeviceStatus(device) {
  if (!device.primary_mac || !device.primary_mac.last_seen) {
    return "offline";
  }

  const lastSeen = new Date(device.primary_mac.last_seen);
  const now = new Date();
  const minutesSinceLastSeen = (now - lastSeen) / (1000 * 60);

  if (minutesSinceLastSeen < 1) {
    return "online";
  } else if (minutesSinceLastSeen < 5) {
    return "away";
  } else {
    return "offline";
  }
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

    await updateDeviceDisplay();

    addLogEntry(`Loaded ${data.devices.length} devices from database`, "info");
  } catch (error) {
    console.error("Error loading devices:", error);
    addLogEntry("Failed to load devices", "error");
  }
}

async function updateDeviceDisplay() {
  // Clear device grid
  devicesGrid.innerHTML = "";

  // Apply current grid size
  const gridClass = `device-grid grid-${currentGridSize}`;
  devicesGrid.className = gridClass;

  // Sort devices by status (online first, then away, then offline)
  const statusOrder = { online: 1, away: 2, offline: 3 };
  const sortedDevices = [...discoveredDevices].sort((a, b) => {
    const statusA = getDeviceStatus(a);
    const statusB = getDeviceStatus(b);
    return statusOrder[statusA] - statusOrder[statusB];
  });

  // Add all devices to the single grid
  for (const device of sortedDevices) {
    const status = getDeviceStatus(device);
    const deviceCard = await createDeviceCard(device, status);
    devicesGrid.appendChild(deviceCard);
  }

  // Update total device count
  deviceCount.textContent = discoveredDevices.length;

  // Show/hide empty state
  if (discoveredDevices.length === 0) {
    emptyState.style.display = "block";
    devicesGrid.style.display = "none";
  } else {
    emptyState.style.display = "none";
    devicesGrid.style.display = "grid";
  }
}

async function createDeviceCard(device, status) {
  const deviceCard = document.createElement("div");
  deviceCard.className = `device-card ${status}`;
  deviceCard.setAttribute("data-device-id", device.id);

  const deviceInfo = document.createElement("div");
  deviceInfo.className = "device-info";

  const iconElement = document.createElement("div");
  iconElement.className = "device-icon";

  if (device.category && device.category.name) {
    var svgContent = null;
    if (window.svgLoader.isIconCached(device.category.name)) {
      svgContent = await window.svgLoader.getDeviceIcon(device.category.name);
    } else {
      svgContent = window.svgLoader.getDeviceIconAsync(device.category.name);
    }
    iconElement.innerHTML = svgContent;
  } else {
    iconElement.innerHTML = `<div class="unknown-device">?</div>`;
  }

  const deviceName = document.createElement("div");
  deviceName.className = "device-name";
  deviceName.innerHTML = `<strong>${device.name}</strong>`;

  deviceInfo.appendChild(iconElement);
  deviceInfo.appendChild(deviceName);
  deviceCard.appendChild(deviceInfo);

  return deviceCard;
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

// Grid size management
let currentGridSize = 4;
const gridSizes = [4, 5, 6];

function initializeGridSize() {
  const gridSizeBtn = document.getElementById("gridSizeBtn");

  if (!gridSizeBtn) return;

  // Update button title to show current grid size
  const updateButtonTitle = () => {
    gridSizeBtn.title = `Change grid size (currently ${currentGridSize} columns)`;
  };
  updateButtonTitle();

  // Add click event listener
  gridSizeBtn.addEventListener("click", function () {
    // Cycle to next grid size
    const currentIndex = gridSizes.indexOf(currentGridSize);
    const nextIndex = (currentIndex + 1) % gridSizes.length;
    currentGridSize = gridSizes[nextIndex];

    // Update button title
    updateButtonTitle();

    // Update the device grid
    const gridClass = `device-grid grid-${currentGridSize}`;
    devicesGrid.className = gridClass;

    // Add visual feedback
    gridSizeBtn.style.transform = "scale(0.95)";
    setTimeout(() => {
      gridSizeBtn.style.transform = "";
    }, 100);
  });
}

// Auto-refresh functionality
function startDeviceStatusUpdates() {
  // Update device status every 30 seconds
  deviceUpdateInterval = setInterval(async () => {
    if (!isScanning && discoveredDevices.length > 0) {
      await updateDeviceDisplay();
    }
  }, 30000);
}

function stopDeviceStatusUpdates() {
  if (deviceUpdateInterval) {
    clearInterval(deviceUpdateInterval);
    deviceUpdateInterval = null;
  }
}

document.addEventListener("DOMContentLoaded", async function () {
  await window.svgLoader.preloadCommonIcons();

  await loadDevices();
  initializeGridSize();
  startDeviceStatusUpdates();
});
