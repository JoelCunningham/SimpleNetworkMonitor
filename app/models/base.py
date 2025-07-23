"""
Base model class with common functionality.
"""
from datetime import datetime, timezone

from app import database


class BaseModel(database.Model):
    """Base model class that provides common fields and methods."""
    __abstract__ = True
    
    id = database.Column(database.Integer, primary_key=True)
    deleted = database.Column(database.Boolean, default=False, nullable=False)
    created_at = database.Column(database.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = database.Column(database.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    def save(self):
        """Save the model to the database."""
        database.session.add(self)
        database.session.commit()
        return self
    
    def delete(self):
        """Soft delete the model."""
        self.deleted = True
        database.session.commit()
    
    def hard_delete(self):
        """Hard delete the model from the database."""
        database.session.delete(self)
        database.session.commit()
    
    @classmethod
    def get_active(cls):
        """Get all non-deleted records."""
        return cls.query.filter_by(deleted=False)
