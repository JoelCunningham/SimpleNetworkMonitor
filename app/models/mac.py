"""
MAC address model.

Represents a network MAC address with associated network information.
"""
from datetime import datetime, timezone
from app import database
from app.models.base import BaseModel


class Mac(BaseModel):
    """MAC address model."""
    __tablename__ = 'mac'
    
    address = database.Column(database.String(17), nullable=False, unique=True)
    last_ip = database.Column(database.String(45), nullable=False)
    last_seen = database.Column(database.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    ping_time_ms = database.Column(database.Integer, nullable=True)
    arp_time_ms = database.Column(database.Integer, nullable=True)
    
    hostname = database.Column(database.String(255), nullable=True)
    vendor = database.Column(database.String(255), nullable=True)
    os_guess = database.Column(database.String(255), nullable=True)
    ttl = database.Column(database.Integer, nullable=True)
    
    # Foreign key
    device_id = database.Column(database.Integer, database.ForeignKey('device.id'), nullable=True)
    
    # Relationships
    device = database.relationship('Device', back_populates='macs')
    ports = database.relationship('Port', back_populates='mac', lazy='dynamic', cascade='all, delete-orphan')
    discoveries = database.relationship('Discovery', back_populates='mac', lazy='dynamic', cascade='all, delete-orphan')
