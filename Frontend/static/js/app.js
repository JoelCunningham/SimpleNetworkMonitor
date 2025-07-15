document.addEventListener("DOMContentLoaded", async function () {
  await window.svgLoader.preloadCommonIcons();

  // Load initial device data
  await window.deviceManager.refreshDevices();

  window.scanManager.updateScanStatus();
  window.deviceManager.initializeGridSize();

  // Check scan status every 3 seconds
  this.statusUpdateInterval = setInterval(async () => {
    if (window.scanManager.isLiveMode()) {
      newScan = await window.scanManager.updateScanStatus();
      if (newScan) {
        await window.deviceManager.refreshDevices();
      }
    } else {
      window.deviceManager.updateDeviceDisplay();
    }
  }, 3000);
});

function toggleViewMode() {
  window.scanManager.toggleViewMode();
}

function refreshDevices() {
  window.deviceManager.refreshDevices();
}
