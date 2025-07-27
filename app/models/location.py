"""
Location model.

Represents physical locations for devices.
"""
from app import database
from app.models.base import BaseModel


class Location(BaseModel):
    """Device location model."""
    __tablename__ = 'location'
    
    name = database.Column(database.String(100), nullable=False, unique=True)
    
    # Relationships
    devices = database.relationship('Device', back_populates='location')
    