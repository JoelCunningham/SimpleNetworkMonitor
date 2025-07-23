"""
Category model.

Represents device categories for organization.
"""
from app import database
from app.models.base import BaseModel


class Category(BaseModel):
    """Device category model."""
    __tablename__ = 'category'
    
    name = database.Column(database.String(100), nullable=False, unique=True)
    
    # Relationships
    devices = database.relationship('Device', back_populates='category')
