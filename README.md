# SimpleNetworkMonitor

To run on windows, requires npcap https://npcap.com/#download

If using SCALE, make sure the container or app has proper capabilities (e.g., --cap-add=NET_RAW if in Docker)

## Setup

Create virtual environment:

```bash
python -m venv venv
```

Enter virtual environment:

```bash
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Save virtual environment dependencies:

```bash
pip freeze > requirements.txt
```

## Style Guide

| Type           | Case             |
| -------------- | ---------------- |
| Variable names | snake_case       |
| Function names | snake_case       |
| Class names    | PascalCase       |
| File names     | PascalCase       |
| Module names   | PascalCase       |
| Constant names | UPPER_SNAKE_CASE |
