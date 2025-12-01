# Backend Dockerfile for SimpleNetworkMonitor
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for Scapy and network operations
RUN apt-get update && apt-get install -y \
    gcc \
    tcpdump \
    libpcap-dev \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY network_monitor.db.example ./network_monitor.db

# Create instance directory for database
RUN mkdir -p /app/instance

# Expose port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
