<div align="center">

# 🌐 SimpleNetworkMonitor

### _Comprehensive Network Discovery & Device Management_

[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Angular](https://img.shields.io/badge/Angular-20.1.0-DD0031?style=for-the-badge&logo=angular)](https://angular.io/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

A powerful network monitoring and device discovery tool that automatically scans your local network, tracks MAC addresses, identifies open ports, and gathers comprehensive device information through multiple discovery protocols.

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Configuration](#-configuration) • [Documentation](#-api-documentation)

</div>

---

## ✨ Features

<table>
<tr>
<td>

### 🔍 **Network Discovery**

- 🔄 Automated periodic scanning
- 📡 Multi-protocol discovery (mDNS, UPnP, SSDP, LLDP)
- 🎯 ICMP ping & ARP resolution
- 🌐 Subnet-wide device detection

</td>
<td>

### 📊 **Device Management**

- 📝 Comprehensive device tracking
- 🏷️ Categories, locations & owners
- 🔖 MAC address vendor lookup
- 📈 Real-time status monitoring

</td>
</tr>
<tr>
<td>

### 🔐 **Port & Service Analysis**

- 🚪 Open port detection
- 🔎 Service identification
- ⚡ Fast multi-threaded scanning

</td>
<td>

### 💻 **Modern Interface**

- 🎨 Angular 20 reactive UI
- 📱 Real-time updates
- 🔗 RESTful API with docs
- 🧩 Modular component design

</td>
</tr>
</table>

---

## 🏗️ Architecture

### 🐍 Backend (Python/FastAPI)

<details open>
<summary><b>Technology Stack</b></summary>

- **Framework**: FastAPI with Uvicorn ASGI server
- **Database**: SQLAlchemy 2.0 + SQLModel (SQLite default)
- **Network Scanning**: Scapy for low-level packet operations
- **DI Container**: Custom service container pattern

</details>

<details>
<summary><b>🔧 Core Services</b></summary>

| Service               | Description                                              |
| --------------------- | -------------------------------------------------------- |
| 🔍 `ScanService`      | Orchestrates network scanning operations                 |
| 📡 `PingService`      | ICMP ping operations for device reachability             |
| 🏷️ `MacService`       | MAC address lookup and vendor identification             |
| 🚪 `PortService`      | Port scanning and service detection                      |
| 📡 `DiscoveryService` | Multi-protocol device discovery (mDNS, UPnP, SSDP, LLDP) |
| 💾 `DeviceService`    | Device CRUD operations and management                    |
| 👥 `OwnerService`     | Owner management and assignment                          |
| 📂 `CategoryService`  | Device categorization                                    |
| 📍 `LocationService`  | Location tracking and management                         |

</details>

<details>
<summary><b>🛣️ API Endpoints</b></summary>

```
📍 /api/devices      - Device management (GET, POST, PUT, DELETE)
👥 /api/owners       - Owner management
📂 /api/categories   - Device categories
📍 /api/locations    - Device locations
🏷️ /api/macs         - MAC address information
```

Interactive API docs available at: `http://localhost:8000/docs` 📚

</details>

<details>
<summary><b>🗄️ Database Schema</b></summary>

| Model       | Purpose                                      |
| ----------- | -------------------------------------------- |
| `Device`    | Tracked network devices                      |
| `Mac`       | MAC addresses with vendor and discovery data |
| `Port`      | Open ports and detected services             |
| `Discovery` | Protocol-specific discovery information      |
| `Owner`     | Device ownership tracking                    |
| `Category`  | Device type categorization                   |
| `Location`  | Physical/logical location data               |

</details>

### 🅰️ Frontend (Angular)

<details open>
<summary><b>Technology Stack</b></summary>

- **Framework**: Angular 20 with standalone components
- **State Management**: RxJS observables and BehaviorSubjects
- **HTTP**: Angular HttpClient with typed responses
- **Styling**: SCSS with component-scoped styles

</details>

<details>
<summary><b>🎨 Component Architecture</b></summary>

```
📱 Panels:
   ├── DevicesPanel        - Main device grid
   ├── OwnersPanel         - Owner management
   ├── StatusPanel         - Network status
   └── UnknownDevicesPanel - Unassigned MACs

🔧 Services:
   ├── DeviceService       - Device data management
   ├── MacService          - MAC address handling
   ├── OwnerService        - Owner operations
   ├── CategoryService     - Category management
   ├── LocationService     - Location management
   └── UtilitiesService    - Helper utilities
```

</details>

---

## 📋 Requirements

### 💻 Windows

- **[npcap](https://npcap.com/#download)** (required for Windows)
- Administrator privileges for packet capture

### 🐳 Docker / TrueNAS SCALE

```bash
--cap-add=NET_RAW
```

---

## 🚀 Quick Start

### 🐍 Backend Setup

**1️⃣ Create Virtual Environment**

```bash
python -m venv venv
```

**2️⃣ Activate Environment**

```bash
.\venv\Scripts\activate
```

**3️⃣ Install Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**4️⃣ Configure (Optional)**

Create `.env` in backend directory:

```env
SUBNET=192.168.0
MIN_SCAN_IP=1
MAX_SCAN_IP=254
BACKGROUND_SCAN_INTERVAL_S=60
DATABASE_URL=sqlite:///network_monitor.db
```

**5️⃣ Launch Backend**

```bash
uvicorn app:create_app --factory --reload
```

✅ API: `http://localhost:8000/api`  
📚 Docs: `http://localhost:8000/docs`

### 🅰️ Frontend Setup

```bash
cd frontend
npm install
npm start
```

🎉 UI: `http://localhost:4200`

---

## ⚙️ Configuration

Configuration options in `backend/app/config.py`:

### 🌐 Network Settings

| Setting       | Default     | Description                     |
| ------------- | ----------- | ------------------------------- |
| `subnet`      | `192.168.0` | Network subnet to scan          |
| `min_scan_ip` | `1`         | First IP in scan range (1-254)  |
| `max_scan_ip` | `254`       | Last IP in scan range (1-254)   |
| `max_threads` | `254`       | Maximum concurrent scan threads |

### ⏱️ Scan Intervals

| Setting                           | Default | Description                             |
| --------------------------------- | ------- | --------------------------------------- |
| `background_scan_interval_s`      | `60`    | Quick scan interval (seconds)           |
| `background_full_scan_interval_s` | `300`   | Full scan with port detection (seconds) |

### ⏰ Timeout Settings (milliseconds)

| Setting                        | Default | Description                 |
| ------------------------------ | ------- | --------------------------- |
| `ping_timeout_ms`              | `2000`  | ICMP ping timeout           |
| `arp_timeout_ms`               | `1000`  | ARP resolution timeout      |
| `hostname_timeout_ms`          | `1000`  | DNS hostname lookup timeout |
| `port_scan_timeout_ms`         | `1000`  | Port scan timeout per port  |
| `service_detection_timeout_ms` | `2000`  | Service banner grab timeout |
| `discovery_timeout_ms`         | `3000`  | Protocol discovery timeout  |

### 💾 Database

| Setting           | Default                        | Description             |
| ----------------- | ------------------------------ | ----------------------- |
| `database_url`    | `sqlite:///network_monitor.db` | SQLAlchemy database URL |
| `sqlalchemy_echo` | `False`                        | Log all SQL queries     |

> 💡 **Tip**: Override any setting via `.env` file in the backend directory

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest app/tests/
```

---

## 🗄️ Database

- **Default**: SQLite (`network_monitor.db`)
- **Example DB**: `backend/network_monitor.db.example`
- **Custom DB**: Modify `database_url` in `.env`

Supports any SQLAlchemy-compatible database (PostgreSQL, MySQL, etc.)

---

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Interactive documentation with example requests and responses for all endpoints.

---

## 📖 Style Guide

| Type      | Convention         | Example            |
| --------- | ------------------ | ------------------ |
| Variables | `snake_case`       | `device_name`      |
| Functions | `snake_case`       | `get_devices()`    |
| Classes   | `PascalCase`       | `DeviceService`    |
| Files     | `PascalCase`       | `DeviceService.py` |
| Modules   | `PascalCase`       | `DeviceModule`     |
| Constants | `UPPER_SNAKE_CASE` | `MAX_THREADS`      |

---

## 🔧 Technology Stack

### Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)

| Package           | Version | Purpose               |
| ----------------- | ------- | --------------------- |
| FastAPI           | 0.116.1 | Web framework         |
| SQLAlchemy        | 2.0.43  | Database ORM          |
| SQLModel          | 0.0.24  | Pydantic + SQLAlchemy |
| Scapy             | 2.6.1   | Network scanning      |
| Pydantic          | 2.11.7  | Data validation       |
| mac-vendor-lookup | 0.1.12  | MAC vendor database   |
| Uvicorn           | 0.35.0  | ASGI server           |
| pytest            | 7.4.0+  | Testing framework     |

### Frontend

![Angular](https://img.shields.io/badge/Angular-DD0031?style=flat&logo=angular&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![RxJS](https://img.shields.io/badge/RxJS-B7178C?style=flat&logo=reactivex&logoColor=white)
![SCSS](https://img.shields.io/badge/SCSS-CC6699?style=flat&logo=sass&logoColor=white)

| Package    | Version | Purpose              |
| ---------- | ------- | -------------------- |
| Angular    | 20.1.0  | Frontend framework   |
| TypeScript | 5.8.2   | Type-safe JavaScript |
| RxJS       | 7.8.0   | Reactive programming |
| Jasmine    | 5.8.0   | Testing framework    |
| Karma      | 6.4.0   | Test runner          |
