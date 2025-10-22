import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.database import Database
from app.models import Category
from app.services import CategoryService


def test_get_categories_empty():
    database = Database("sqlite:///:memory:")
    service = CategoryService(database)

    categories = service.get_categories()
    assert isinstance(categories, list)
    assert len(categories) == 0


def test_get_categories_after_create():
    database = Database("sqlite:///:memory:")
    service = CategoryService(database)

    category = Category(name="Routers")
    database.create(category)

    categories = service.get_categories()
    assert len(categories) == 1
    assert categories[0].name == "Routers"
