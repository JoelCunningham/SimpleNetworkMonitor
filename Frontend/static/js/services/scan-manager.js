class ScanManager {
  constructor() {
    this.isScanning = false;
    this.statusText = document.getElementById("statusText");
    this.progressContainer = document.getElementById("progressContainer");
    this.progressBar = document.getElementById("progressBar");
    this.progressText = document.getElementById("progressText");
    this.logs = document.getElementById("logs");
    this.logEntries = document.getElementById("logEntries");

    this.setupSocketListeners();
  }

  setupSocketListeners() {
    const socket = io();

    socket.on("scan_update", (data) => {
      window.logger.addLogEntry(data.message, data.type);
      this.statusText.textContent = data.message;
    });

    socket.on("scan_progress", (data) => {
      const percent = data.progress;
      this.progressBar.style.width = percent + "%";
      this.progressText.textContent = `Processing device ${data.current} of ${data.total} (${percent}%)`;
    });

    socket.on("scan_complete", (data) => {
      window.logger.addLogEntry(data.message, data.type);
      this.statusText.textContent = data.message;
      this.isScanning = false;
      this.progressContainer.style.display = "none";
      this.progressText.style.display = "none";
      window.deviceManager.loadDevices();
    });

    socket.on("scan_error", (data) => {
      window.logger.addLogEntry(data.message, data.type);
      this.statusText.textContent = "Scan failed: " + data.message;
      this.isScanning = false;
      this.progressContainer.style.display = "none";
      this.progressText.style.display = "none";
    });
  }

  startScan() {
    if (this.isScanning) return;

    fetch("/api/scan/start", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          return;
        }

        this.isScanning = true;
        this.statusText.textContent = "Starting scan...";

        // Clear previous results
        window.deviceManager.clearDevices();

        // Show progress elements
        this.progressContainer.style.display = "block";
        this.progressText.style.display = "block";
        this.logs.style.display = "block";
        this.progressBar.style.width = "0%";
        this.logEntries.innerHTML = "";
      })
      .catch((error) => {
        console.error("Error starting scan:", error);
        alert("Failed to start scan");
      });
  }
}

// Create global instance
window.scanManager = new ScanManager();
