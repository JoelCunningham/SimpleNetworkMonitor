"""
API interface routes (FastAPI version).
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.response import ErrorResponse, MacResponse
from app.container import get_mac_service
from app.services.interfaces import MacServiceInterface

mac_router = APIRouter()

@mac_router.get("", response_model=list[MacResponse], responses={500: {"model": ErrorResponse}})
async def get_macs(mac_service: MacServiceInterface = Depends(get_mac_service)):
    """Get all known devices from the latest scan."""
    try:      
        return mac_service.get_unassigned()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get devices: {str(e)}")