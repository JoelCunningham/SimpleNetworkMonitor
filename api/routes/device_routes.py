"""
API interface routes (FastAPI version).
"""
from fastapi import APIRouter, HTTPException, Depends

from api.request import DeviceRequest
from api.response import DeviceResponse, ErrorResponse
from app.container import get_device_service
from common.objects import DeviceInput
from app.services.device_service import DeviceService

router = APIRouter()

@router.get("", response_model=list[DeviceResponse], responses={500: {"model": ErrorResponse}})
async def get_devices(device_service: DeviceService = Depends(get_device_service)):
    """Get all known devices from the latest scan."""
    try:      
        return device_service.get_current_devices()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get devices: {str(e)}")

@router.post("", response_model=DeviceResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def save_device(device: DeviceRequest, device_service: DeviceService = Depends(get_device_service)):
    """Save a device to the database."""
    try:
        dto = DeviceInput(**device.model_dump())
        return device_service.add_device(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save device: {str(e)}")

@router.put("/{id}", response_model=DeviceResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def update_device(id: int, device: DeviceRequest, device_service: DeviceService = Depends(get_device_service)):
    """Update a device by ID."""
    try:
        dto = DeviceInput(**device.model_dump())
        return device_service.update_device(id, dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update device: {str(e)}")
