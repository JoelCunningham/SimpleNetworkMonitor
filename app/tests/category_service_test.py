import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app import database
from app.models import Category
from app.services import CategoryService


def test_get_categories_empty():
    svc = CategoryService(database)

    cats = svc.get_categories()
    assert isinstance(cats, list)
    assert len(cats) == 0


def test_get_categories_after_create():
    svc = CategoryService(database)

    cat = Category(name="Routers")
    database.create(cat)

    cats = svc.get_categories()
    assert len(cats) == 1
    assert cats[0].name == "Routers"
