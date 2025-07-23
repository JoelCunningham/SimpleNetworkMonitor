"""
Port model.

Represents an open network port on a MAC address.
"""
from app import database
from app.models.base import BaseModel


class Port(BaseModel):
    """Network port model."""
    __tablename__ = 'port'
    
    port = database.Column(database.Integer, nullable=False)
    protocol = database.Column(database.String(10), default='tcp', nullable=False)
    service = database.Column(database.String(100), nullable=True)
    banner = database.Column(database.Text, nullable=True)
    state = database.Column(database.String(20), default='open', nullable=False)
    
    # Foreign key
    mac_id = database.Column(database.Integer, database.ForeignKey('mac.id'), nullable=False)
    
    # Relationships
    mac = database.relationship('Mac', back_populates='ports')
