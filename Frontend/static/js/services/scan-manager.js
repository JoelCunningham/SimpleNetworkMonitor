class ScanManager {
  constructor() {
    this.previousScanTime = null;
    this.scanningStatus = document.getElementById("lastScanTime");
    this.viewModeToggle = document.getElementById("viewModeToggle");
    this.liveMode = true;
  }

  async updateScanStatus() {
    const BASE_TEXT = "Last scan: ";

    const response = await fetch("/api/scan/status");
    const scanStatus = await response.json();

    if (scanStatus.is_scanning) {
      this.scanningStatus.textContent = BASE_TEXT + "Scanning now...";
    } else if (scanStatus.last_scan_time) {
      const dateText = new Date(scanStatus.last_scan_time).toLocaleString();
      this.scanningStatus.textContent = BASE_TEXT + dateText;
    } else {
      this.scanningStatus.textContent = BASE_TEXT + "Never";
    }

    if (this.previousScanTime !== scanStatus.last_scan_time) {
      this.previousScanTime = scanStatus.last_scan_time;
      return true;
    }
    return false;
  }

  toggleViewMode() {
    this.liveMode = !this.liveMode;

    if (this.liveMode) {
      this.viewModeToggle.classList.add("active");
      window.deviceManager.refreshDevices();
    } else {
      this.viewModeToggle.classList.remove("active");
    }
  }

  isLiveMode() {
    return this.liveMode;
  }
}

// Create a global instance
window.scanManager = new ScanManager();
