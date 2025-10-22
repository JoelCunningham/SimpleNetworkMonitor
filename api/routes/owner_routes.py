"""
API interface routes (FastAPI version).
"""
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from api.request import OwnerRequest
from api.response import ErrorResponse, OwnerResponse
from app.container import get_owner_service
from app.services.owner_service import OwnerService
from common.objects import OwnerInput

router = APIRouter()

@router.get("", response_model=List[OwnerResponse], responses={500: {"model": ErrorResponse}})
async def get_owners(owner_service: OwnerService = Depends(get_owner_service)):
    """Get all device owners."""
    try:
        return owner_service.get_owners()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get owners: {str(e)}")

@router.post("", response_model=OwnerResponse, status_code=201, responses={500: {"model": ErrorResponse}})
async def save_owner(owner: OwnerRequest, owner_service: OwnerService = Depends(get_owner_service)):
    """Save a new owner."""
    try:
        dto = OwnerInput(**owner.model_dump())
        return owner_service.add_owner(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save owner: {str(e)}")

@router.put("/{owner_id}", response_model=OwnerResponse, responses={500: {"model": ErrorResponse}})
async def update_owner(owner_id: int, owner: OwnerRequest, owner_service: OwnerService = Depends(get_owner_service)):
    """Update an existing owner."""
    try:
        dto = OwnerInput(**owner.model_dump())
        return owner_service.update_owner(owner_id, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update owner: {str(e)}")

@router.delete("/{owner_id}", status_code=204, responses={500: {"model": ErrorResponse}})
async def delete_owner(owner_id: int, owner_service: OwnerService = Depends(get_owner_service)):
    """Delete an owner by their ID."""
    try:
        owner_service.delete_owner(owner_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete owner: {str(e)}")