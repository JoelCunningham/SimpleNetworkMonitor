
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
database = Database(config.database_url)
container = Container()

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

    # Mount API app
    from api import create_api_app
    api_app = create_api_app()
    app.mount("/api", api_app)

    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=start_scanning_task, daemon=True)
    thread.start()
    yield
    
def start_scanning_task():
    time.sleep(5)
    container.scanning_service().start_continuous_scan()