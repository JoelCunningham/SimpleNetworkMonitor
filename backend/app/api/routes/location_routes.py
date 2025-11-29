"""
API interface routes (FastAPI version).
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api.response import ErrorResponse, LocationResponse
from app.container import get_location_service
from app.services.interfaces import LocationServiceInterface

location_router = APIRouter()

@location_router.get("", response_model=List[LocationResponse], responses={500: {"model": ErrorResponse}})
async def get_locations(location_service: LocationServiceInterface = Depends(get_location_service)):
    """Get all device locations."""
    try:
        return location_service.get_locations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get locations: {str(e)}")
    
    