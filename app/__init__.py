
"""
SimpleNetworkMonitor FastAPI Application

A network monitoring tool that discovers and tracks devices on your network.
"""
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Config
from app.container import Container
from app.database import Database

config = Config()


def create_app() -> FastAPI:
    app = FastAPI(title="SimpleNetworkMonitor", lifespan=lifespan)

    # Set up CORS for frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    from api import create_api_app
    api_app = create_api_app()
    app.include_router(api_app, prefix="/api")

    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(config.database_url)
    app.state.container = Container(database=database)
    thread = threading.Thread(target=start_scanning_task, args=(app.state.container,), daemon=True)
    thread.start()

    try:
        yield
    finally:
        db = getattr(app.state.container, "_database", None)
        try:
            if db is not None and hasattr(db, "dispose"):
                db.dispose()
        except Exception:
            pass

def start_scanning_task(container: Container):
    time.sleep(5)
    try:
        container.scanning_service().start_continuous_scan()
    except Exception:
        return