import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TEST_DIR = ROOT / "instance" / "test"
TEST_DIR.mkdir(parents=True, exist_ok=True)

TEST_DB = TEST_DIR / "network_monitor_test.db"

if TEST_DB.exists():
    try:
        TEST_DB.unlink()
    except Exception:
        pass

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"
