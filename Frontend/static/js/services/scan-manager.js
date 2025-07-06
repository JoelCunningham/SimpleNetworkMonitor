class ScanManager {
  constructor() {
    this.isScanning = false;
    this.progressContainer = document.getElementById("progressContainer");
    this.progressBar = document.getElementById("progressBar");
    this.logs = document.getElementById("logs");
    this.logEntries = document.getElementById("logEntries");
    this.scanningStatus = document.getElementById("lastScanTime");

    this.previousScanTime = document.getElementById("lastScanTime").textContent;

    this.setupSocketListeners();
  }

  setupSocketListeners() {
    const socket = io();

    socket.on("scan_update", (data) => {
      window.logger.addLogEntry(data.message, data.type);
    });

    socket.on("scan_progress", (data) => {
      const percent = data.progress;
      if (this.progressBar) {
        this.progressBar.style.width = percent + "%";
      }
    });

    socket.on("scan_complete", (data) => {
      window.logger.addLogEntry(data.message, data.type);
      this.scanningStatus.textContent =
        "Last scan: " + new Date().toLocaleString();
      this.progressContainer.style.display = "none";
      this.isScanning = false;
      window.deviceManager.loadDevices();
    });

    socket.on("scan_error", (data) => {
      window.logger.addLogEntry(data.message, data.type);
      this.scanningStatus.textContent = this.previousScanTime;
      this.progressContainer.style.display = "none";
      this.isScanning = false;
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
        this.scanningStatus.textContent = "Starting scan...";
        this.progressContainer.style.display = "block";
        this.progressBar.style.width = "0%";
      })
      .catch((error) => {
        console.error("Error starting scan:", error);
        alert("Failed to start scan");
      });
  }
}
