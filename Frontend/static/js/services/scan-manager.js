class ScanManager {
  constructor() {
    this.isScanning = false;
    this.scanningStatus = document.getElementById("lastScanTime");
    this.scanButton = document.getElementById("scanButton");
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
        this.updateUI();

        // Poll for completion
        this.pollScanStatus();
      })
      .catch((error) => {
        console.error("Error starting scan:", error);
        alert("Failed to start scan");
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

  pollScanStatus() {
    const checkStatus = () => {
      fetch("/api/scan/status")
        .then((response) => response.json())
        .then((data) => {
          if (!data.scanning) {
            this.isScanning = false;
            this.updateUI();
            this.setLastScanTime();
            window.deviceManager.loadDevices(); // Refresh devices
          } else {
            setTimeout(checkStatus, 1000); // Check again in 1 second
          }
        })
        .catch((error) => {
          console.error("Error checking scan status:", error);
          this.isScanning = false;
          this.updateUI();
          this.setLastScanTime();
        });
    };
    checkStatus();
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
