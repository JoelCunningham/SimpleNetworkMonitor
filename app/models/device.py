"""
Device model.

Represents network devices discovered during scans.
"""
from app import database
from app.models.base import BaseModel
from app.models.mac import Mac

UNKNOWN_DEVICE_NAME = "Unknown Device"


class Device(BaseModel):
    """Device model representing a network device."""
    __tablename__ = 'device'
    
    model = database.Column(database.String(200), nullable=True)
    
    # Foreign keys
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'), nullable=True)
    location_id = database.Column(database.Integer, database.ForeignKey('location.id'), nullable=True)
    owner_id = database.Column(database.Integer, database.ForeignKey('owner.id'), nullable=True)
    
    # Relationships
    category = database.relationship('Category', back_populates='devices')
    location = database.relationship('Location', back_populates='devices')
    owner = database.relationship('Owner', back_populates='devices')
    macs = database.relationship('Mac', back_populates='device', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def name(self) -> str:
        """Return the display name for the device."""
        device_name = ""
        
        device_name += self.owner.name + "'s " if self.owner else ""
        device_name += self.location.name + " " if self.location else ""
        device_name += self.category.name if self.category else ""
    
        return device_name.strip() or UNKNOWN_DEVICE_NAME
    
    @property
    def primary_mac(self) -> Mac | None:
        """Get the primary MAC address (most recently seen)."""
        if not self.macs:
            return None
        return max(self.macs.all(), key=lambda mac: mac.last_seen or 0)