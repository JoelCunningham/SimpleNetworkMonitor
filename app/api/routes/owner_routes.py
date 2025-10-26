"""
API interface routes (FastAPI version).
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api.request import OwnerRequest
from app.api.response import ErrorResponse, OwnerResponse
from app.container import get_owner_service
from app.services.interfaces import OwnerServiceInterface

owner_router = APIRouter()

@owner_router.get("", response_model=List[OwnerResponse], responses={500: {"model": ErrorResponse}})
async def get_owners(owner_service: OwnerServiceInterface = Depends(get_owner_service)):
    """Get all device owners."""
    try:
        return owner_service.get_owners()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get owners: {str(e)}")

@owner_router.post("", response_model=OwnerResponse, status_code=201, responses={500: {"model": ErrorResponse}})
async def save_owner(owner: OwnerRequest, owner_service: OwnerServiceInterface = Depends(get_owner_service)):
    """Save a new owner."""
    try:
        return owner_service.add_owner(owner.toOwnerInput())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save owner: {str(e)}")

@owner_router.put("/{owner_id}", response_model=OwnerResponse, responses={500: {"model": ErrorResponse}})
async def update_owner(owner_id: int, owner: OwnerRequest, owner_service: OwnerServiceInterface = Depends(get_owner_service)):
    """Update an existing owner."""
    try:
        return owner_service.update_owner(owner_id, owner.toOwnerInput())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update owner: {str(e)}")

@owner_router.delete("/{owner_id}", status_code=204, responses={500: {"model": ErrorResponse}})
async def delete_owner(owner_id: int, owner_service: OwnerServiceInterface = Depends(get_owner_service)):
    """Delete an owner by their ID."""
    try:
        owner_service.delete_owner(owner_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete owner: {str(e)}")