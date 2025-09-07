from app import database
from app.models.category import Category


class CategoryService:
    """Service for handling category-related operations."""
    
    def get_categories(self) -> list[Category]:
        """Get all categories."""
        return database.session.query(Category).all()
    