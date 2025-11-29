from .category_routes import category_router
from .device_routes import device_router
from .location_routes import location_router
from .mac_routes import mac_router
from .owner_routes import owner_router

__all__ = [
    "category_router",
    "device_router",
    "location_router",
    "mac_router",
    "owner_router",
]