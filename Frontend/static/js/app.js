document.addEventListener("DOMContentLoaded", async function () {
  await window.svgLoader.preloadCommonIcons();

  window.scanManager.startScan(true);

  window.scanManager.setLastScanTime();
  window.deviceManager.initializeGridSize();

  this.deviceUpdateInterval = setInterval(async () => {
    await window.scanManager.startScan(false);
  }, 60000); // Update every 60 seconds

  this.deviceUpdateInterval = setInterval(async () => {
    await window.scanManager.startScan(true);
  }, 300000); // Update every 5 minutes
});

function startScan() {
  new ScanManager().startScan();
}
