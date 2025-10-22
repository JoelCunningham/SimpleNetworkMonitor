from app.database import Database
from app.models import Category
from app.services.interfaces import CategoryServiceInterface


class CategoryService(CategoryServiceInterface):
    def __init__(self, database: Database) -> None:
        self.database = database

    def get_categories(self) -> list[Category]:
        return self.database.select_all(Category).all()