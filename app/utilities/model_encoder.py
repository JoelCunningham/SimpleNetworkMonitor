import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Set, Dict

from app.models.base import BaseModel


class ModelEncoder(json.JSONEncoder):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._serialized_objects: Set[int] = set()
    
    def default(self, o: Any) -> Any:
        if isinstance(o, BaseModel):
            # Check for circular references
            obj_id = id(o)
            if obj_id in self._serialized_objects:
                # Return a minimal representation to break the cycle
                return {
                    'id': getattr(o, 'id', None),
                    '__circular_ref__': True,
                    '__class__': o.__class__.__name__
                }
            self._serialized_objects.add(obj_id)
            
            try:
                data: Dict[str, Any] = {}
                
                if hasattr(o, '__table__'):
                    for column in o.__table__.columns:  # type: ignore
                        value = getattr(o, column.name)  # type: ignore
                        if isinstance(value, datetime):
                            data[column.name] = self._format_datetime(value) # type: ignore
                        else:
                            data[column.name] = value  # type: ignore
                
                # Handle relationships and properties
                for attr_name in dir(o):
                    if attr_name.startswith('_') or attr_name in data:
                        continue
                    
                    try:
                        attr_value = getattr(o, attr_name)
                        
                        # Skip methods and unwanted attributes
                        if callable(attr_value) or attr_name in ['metadata', 'query', 'registry']:
                            continue
                            
                        # Handle SQLAlchemy relationships
                        if hasattr(o.__class__, attr_name):
                            class_attr = getattr(o.__class__, attr_name)
                            if hasattr(class_attr, 'property') and hasattr(class_attr.property, '_is_relationship'):
                                # This is a relationship
                                if attr_value is not None:
                                    if isinstance(attr_value, BaseModel):
                                        data[attr_name] = self.default(attr_value)
                                    elif hasattr(attr_value, '__iter__') and not isinstance(attr_value, str):
                                        # Handle dynamic relationships and collections
                                        try:
                                            items = list(attr_value)
                                            data[attr_name] = [self.default(item) if isinstance(item, BaseModel) else item for item in items]
                                        except Exception:
                                            # If we can't iterate, skip it
                                            continue
                            elif isinstance(class_attr, property):
                                # This is a property
                                if attr_value is not None:
                                    if isinstance(attr_value, BaseModel):
                                        data[attr_name] = self.default(attr_value)
                                    elif hasattr(attr_value, '__iter__') and not isinstance(attr_value, str):
                                        try:
                                            items = list(attr_value)
                                            data[attr_name] = [self.default(item) if isinstance(item, BaseModel) else item for item in items]
                                        except Exception:
                                            data[attr_name] = str(attr_value)
                                    else:
                                        data[attr_name] = attr_value
                    except Exception:
                        # Skip attributes that cause errors
                        continue
                
                return data
            finally:
                self._serialized_objects.discard(obj_id)
        
        if isinstance(o, datetime):
            return self._format_datetime(o)
        
        if isinstance(o, Decimal):
            return float(o)
        
        return json.JSONEncoder.default(self, o)
    
    def _format_datetime(self, dt: datetime) -> str:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        utc_dt = dt.astimezone(timezone.utc)
        return utc_dt.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'