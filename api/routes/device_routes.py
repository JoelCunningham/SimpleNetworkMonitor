"""
API interface routes (FastAPI version).
"""
from fastapi import APIRouter, HTTPException

from api.request.device_request import DeviceRequest
from api.response.device_response import DeviceResponse
from api.response.error_response import ErrorResponse
from app.container import Container
from common.objects.device_input import DeviceInput

router = APIRouter()
container = Container()

@router.get("", response_model=list[DeviceResponse], responses={500: {"model": ErrorResponse}})
async def get_devices():
    """Get all known devices from the latest scan."""
    try:      
        return container.device_service().get_current_devices()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get devices: {str(e)}")

@router.post("", response_model=DeviceResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def save_device(device: DeviceRequest):
    """Save a device to the database."""
    try:
        dto = DeviceInput(**device.model_dump())
        return container.device_service().add_device(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save device: {str(e)}")

@router.put("/{id}", response_model=DeviceResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def update_device(id: int, device: DeviceRequest):
    """Update a device by ID."""
    try:
        dto = DeviceInput(**device.model_dump())
        return container.device_service().update_device(id, dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update device: {str(e)}")
