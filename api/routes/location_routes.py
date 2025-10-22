"""
API interface routes (FastAPI version).
"""
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from api.response import ErrorResponse, LocationResponse
from app.container import get_location_service
from app.services.location_service import LocationService

router = APIRouter()

@router.get("", response_model=List[LocationResponse], responses={500: {"model": ErrorResponse}})
async def get_locations(location_service: LocationService = Depends(get_location_service)):
    """Get all device locations."""
    try:
        return location_service.get_locations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get locations: {str(e)}")
    
    