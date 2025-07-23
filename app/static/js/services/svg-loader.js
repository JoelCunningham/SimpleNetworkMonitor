class SvgLoader {
  constructor() {
    this.cache = new Map();
    this.loadingPromises = new Map();
  }

  async preloadCommonIcons() {
    const response = await fetch(ENDPOINT_DEVICE_ICONS);
    if (!response.ok) return;

    const data = await response.json();

    const loadPromises = data.icons.map((filename) => {
      const fullPath = `${DIRECTORY_DEVICES}${filename}`;
      return this.loadSvg(fullPath);
    });

    await Promise.all(loadPromises);
  }

  async loadSvg(path) {
    if (this.cache.has(path)) {
      return this.cache.get(path);
    }

    if (this.loadingPromises.has(path)) {
      return this.loadingPromises.get(path);
    }

    const loadingPromise = this._fetchSvg(path);
    this.loadingPromises.set(path, loadingPromise);

    try {
      const result = await loadingPromise;
      return result;
    } finally {
      this.loadingPromises.delete(path);
    }
  }

  getDeviceIcon(deviceType) {
    return this.cache.get(this._getIconPath(deviceType)) || null;
  }

  async getDeviceIconAsync(deviceType) {
    return await this.loadSvg(this._getIconPath(deviceType));
  }

  isIconCached(deviceType) {
    return this.cache.has(this._getIconPath(deviceType));
  }

  async _fetchSvg(path) {
    try {
      const response = await fetch(path);
      if (!response.ok) return null;

      const svgContent = await response.text();
      this.cache.set(path, svgContent);
      return svgContent;
    } catch (error) {
      return null;
    }
  }

  _getIconPath(deviceType) {
    return `${DIRECTORY_DEVICES}${deviceType.toLowerCase()}${ICON_EXT}`;
  }
}

// Create a global instance
window.svgLoader = new SvgLoader();

import { DIRECTORY_DEVICES, ENDPOINT_DEVICE_ICONS } from "./constants.js";
