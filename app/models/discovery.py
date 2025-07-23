"""
Discovery model.

Represents discovery information from network protocols.
"""
from app import database
from app.models.base import BaseModel


class Discovery(BaseModel):
    """Discovery information model."""
    __tablename__ = 'discovery'
    
    protocol = database.Column(database.String(50), default='unknown', nullable=False)
    device_name = database.Column(database.String(255), nullable=True)
    device_type = database.Column(database.String(100), nullable=True)
    manufacturer = database.Column(database.String(255), nullable=True)
    model = database.Column(database.String(255), nullable=True)
    
    # Foreign key
    mac_id = database.Column(database.Integer, database.ForeignKey('mac.id'), nullable=False)
    
    # Relationships
    mac = database.relationship('Mac', back_populates='discoveries')
    services = database.relationship('Service', back_populates='discovery', lazy='dynamic', cascade='all, delete-orphan')
