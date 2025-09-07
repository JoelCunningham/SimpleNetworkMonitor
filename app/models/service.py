"""
Service model.

Represents services discovered on network devices.
"""
from app import database
from app.models.base import BaseModel


class Service(BaseModel):
    """Service information model."""
    __tablename__ = 'service'
    
    name = database.Column(database.String(100), nullable=False)
    port = database.Column(database.Integer, nullable=True)
    protocol = database.Column(database.String(10), nullable=True)
    version = database.Column(database.String(255), nullable=True)
    description = database.Column(database.Text, nullable=True)
    
    # Foreign key
    discovery_id = database.Column(database.Integer, database.ForeignKey('discovery.id'), nullable=False)
    
    # Relationships
    discovery = database.relationship('Discovery', back_populates='services')

#TODO Remove this