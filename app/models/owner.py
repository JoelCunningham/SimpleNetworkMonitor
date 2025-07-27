"""
Owner model.

Represents device owners for organization.
"""
from app import database
from app.models.base import BaseModel


class Owner(BaseModel):
    """Device owner model."""
    __tablename__ = 'owner'
    
    name = database.Column(database.String(100), nullable=False, unique=True)
    
    # Relationships
    devices = database.relationship('Device', back_populates='owner')
