class Logger {
  constructor() {
    this.logEntries = document.getElementById("logEntries");
  }

  addLogEntry(message, type = "info") {
    const entry = document.createElement("div");
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    this.logEntries.appendChild(entry);
    this.logEntries.scrollTop = this.logEntries.scrollHeight;
  }
}

// Create global instance
window.logger = new Logger();
