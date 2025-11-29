
"""
SimpleNetworkMonitor FastAPI Application

A network monitoring tool that discovers and tracks devices on your network.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.container import container_lifespan


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="SimpleNetworkMonitor", lifespan=container_lifespan)

    # Set up CORS for frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"http://.*:4200",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    from app.api import create_api_app
    api_app = create_api_app()
    app.include_router(api_app, prefix="/api")

    return app
