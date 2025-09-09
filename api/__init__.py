
from fastapi import FastAPI

from api.routes.category_routes import router as category_router
from api.routes.device_routes import router as device_router
from api.routes.location_routes import router as location_router
from api.routes.owner_routes import router as owner_router


def create_api_app() -> FastAPI:
	app = FastAPI(title="SimpleNetworkMonitor API", docs_url="/docs", openapi_url="/openapi.json")

	app.include_router(device_router, prefix="/devices", tags=["devices"])
	app.include_router(owner_router, prefix="/owners", tags=["owners"])
	app.include_router(category_router, prefix="/categories", tags=["categories"])
	app.include_router(location_router, prefix="/locations", tags=["locations"])

	return app
