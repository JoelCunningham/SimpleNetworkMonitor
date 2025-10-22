"""
API interface routes (FastAPI version).
"""
from typing import List

from fastapi import APIRouter, HTTPException

from api.response.category_response import CategoryResponse
from api.response.error_response import ErrorResponse
from app import container

router = APIRouter()

@router.get("", response_model=List[CategoryResponse], responses={500: {"model": ErrorResponse}})
async def get_categories():
    """Get all device categories."""
    try:
        return container.category_service().get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories: {str(e)}")