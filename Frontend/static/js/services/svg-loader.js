class SvgLoader {
  constructor() {
    this.DEVICE_DIR = "/static/icons/devices/";
    this.cache = new Map();
    this.loadingPromises = new Map();
  }

  async preloadCommonIcons() {
    try {
      const response = await fetch("/api/icons/devices");
      if (!response.ok) return;

      const data = await response.json();

      const loadPromises = data.icons.map((filename) => {
        const fullPath = `${this.DEVICE_DIR}${filename}`;
        return this.loadSvg(fullPath);
      });

      await Promise.all(loadPromises);
    } catch (error) {
      console.error("Failed to preload icons:", error);
    }
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

  getDeviceIcon(deviceType) {
    const path = `${this.DEVICE_DIR}${deviceType.toLowerCase()}.svg`;
    return this.cache.get(path) || null;
  }

  async getDeviceIconAsync(deviceType) {
    const path = `${this.DEVICE_DIR}${deviceType.toLowerCase()}.svg`;
    return await this.loadSvg(path);
  }

  isIconCached(deviceType) {
    const path = `${this.DEVICE_DIR}${deviceType.toLowerCase()}.svg`;
    return this.cache.has(path);
  }
}

window.svgLoader = new SvgLoader();
