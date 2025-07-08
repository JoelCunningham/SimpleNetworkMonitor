class ScanManager {
  constructor() {
    this.isScanning = false;
    this.scanningStatus = document.getElementById("lastScanTime");
    this.scanButton = document.getElementById("scanButton");
  }

  startScan() {
    if (this.isScanning) return;

    this.isScanning = true;
    this.updateUI();

    fetch("/api/scan/start", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          return;
        }

        // Update devices directly with scan results
        if (data.devices) {
          window.deviceManager.updateDeviceDisplay(data.devices);
        }

        this.setLastScanTime();
      })
      .catch((error) => {
        console.error("Error during scan:", error);
        alert("Failed to complete scan");
      })
      .finally(() => {
        this.isScanning = false;
        this.updateUI();
      });
  }

  updateUI() {
    if (this.isScanning) {
      if (this.scanButton) {
        this.scanButton.disabled = true;
        this.scanButton.textContent = "Scanning...";
      }
    } else {
      if (this.scanButton) {
        this.scanButton.disabled = false;
        this.scanButton.innerHTML = `
          <img
            src="/static/icons/refresh.svg"
            alt="Refresh"
            class="scan-icon"
            style="width: 1em; height: 1em; vertical-align: middle"
          />
          Start Scan
        `;
      }
    }
  }

  setLastScanTime() {
    fetch("/api/scan/latest")
      .then((response) => response.json())
      .then((data) => {
        if (data.latest_scan) {
          this.scanningStatus.textContent =
            "Last scan: " + new Date(data.latest_scan).toLocaleString();
        } else {
          this.scanningStatus.textContent = "Last scan: Never";
        }
      });
  }
}
