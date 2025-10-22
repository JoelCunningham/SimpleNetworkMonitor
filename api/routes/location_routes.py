"""
API interface routes (FastAPI version).
"""
from typing import List

from fastapi import APIRouter, HTTPException

from api.response import ErrorResponse, LocationResponse
from app import container

router = APIRouter()

@router.get("", response_model=List[LocationResponse], responses={500: {"model": ErrorResponse}})
async def get_locations():
    """Get all device locations."""
    try:
        return container.location_service().get_locations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get locations: {str(e)}")
    
    