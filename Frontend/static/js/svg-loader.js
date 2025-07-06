class SvgLoader {
  constructor() {
    this.cache = new Map();
  }

  async loadSvg(path) {
    // Check cache first
    if (this.cache.has(path)) {
      return this.cache.get(path);
    }

    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`Failed to load SVG: ${response.status}`);
      }

      const svgContent = await response.text();

      // Cache the content
      this.cache.set(path, svgContent);

      return svgContent;
    } catch (error) {
      console.error(`Error loading SVG from ${path}:`, error);
    }
  }

  async getDeviceIcon(deviceType) {
    const path = `/static/icons/devices/${deviceType.toLowerCase()}.svg`;
    return await this.loadSvg(path);
  }

  /**
   * Create a device icon element with proper styling
   * @param {string} deviceType - Type of device
   * @param {string} className - CSS class to apply to the container
   * @returns {Promise<HTMLElement>} - Promise that resolves to the icon element
   */
  async createDeviceIcon(deviceType, className = "device-icon") {
    const svgContent = await this.getDeviceIcon(deviceType);

    const container = document.createElement("div");
    container.className = className;
    container.innerHTML = svgContent;

    return container;
  }
}

// Create a global instance
window.svgLoader = new SvgLoader();
