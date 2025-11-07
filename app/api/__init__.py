from fastapi import APIRouter

from app.api.routes import *


def create_api_app() -> APIRouter:
	router = APIRouter()

	router.include_router(device_router, prefix="/devices", tags=["devices"])
	router.include_router(owner_router, prefix="/owners", tags=["owners"])
	router.include_router(category_router, prefix="/categories", tags=["categories"])
	router.include_router(location_router, prefix="/locations", tags=["locations"])
	router.include_router(mac_router, prefix="/macs", tags=["macs"])

	return router
