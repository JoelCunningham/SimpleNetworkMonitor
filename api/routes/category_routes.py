"""
API interface routes (FastAPI version).
"""
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from api.response import CategoryResponse, ErrorResponse
from app.container import get_category_service
from app.services.category_service import CategoryService

router = APIRouter()

@router.get("", response_model=List[CategoryResponse], responses={500: {"model": ErrorResponse}})
async def get_categories(category_service: CategoryService = Depends(get_category_service)):
    """Get all device categories."""
    try:
        return category_service.get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories: {str(e)}")