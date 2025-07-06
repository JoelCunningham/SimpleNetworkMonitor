class UpdateManager {
  constructor() {
    this.deviceUpdateInterval = null;
  }

  startDeviceStatusUpdates() {
    // Update device status every 30 seconds
    this.deviceUpdateInterval = setInterval(async () => {
      await window.deviceManager.updateDeviceDisplay();
    }, 30000);
  }

  stopDeviceStatusUpdates() {
    if (this.deviceUpdateInterval) {
      clearInterval(this.deviceUpdateInterval);
      this.deviceUpdateInterval = null;
    }
  }
}

// Create global instance
window.updateManager = new UpdateManager();
