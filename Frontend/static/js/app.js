document.addEventListener("DOMContentLoaded", async function () {
  await window.svgLoader.preloadCommonIcons();

  await window.deviceManager.loadDevices();
  window.deviceManager.initializeGridSize();
  window.updateManager.startDeviceStatusUpdates();

  new ScanManager().setLastScanTime();
});

function startScan() {
  new ScanManager().startScan();
}
