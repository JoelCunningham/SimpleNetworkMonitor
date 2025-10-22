from fastapi import APIRouter

from api.routes.category_routes import router as category_router
from api.routes.device_routes import router as device_router
from api.routes.location_routes import router as location_router
from api.routes.owner_routes import router as owner_router


def create_api_app() -> APIRouter:
	router = APIRouter()

	router.include_router(device_router, prefix="/devices", tags=["devices"])
	router.include_router(owner_router, prefix="/owners", tags=["owners"])
	router.include_router(category_router, prefix="/categories", tags=["categories"])
	router.include_router(location_router, prefix="/locations", tags=["locations"])

	return router
