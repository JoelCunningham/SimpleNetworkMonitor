from sqlmodel import SQLModel
import json
from typing import Any
from datetime import datetime, timezone
from decimal import Decimal


class ModelEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, SQLModel):
            data = o.model_dump()
            
            # Handle regular relationship attributes
            for attr_name in dir(o):
                # Check if this is a relationship field
                if hasattr(o.__class__, '__annotations__') and attr_name in o.__class__.__annotations__:
                    if attr_name in data:
                        continue
                    try:
                        attr_value = getattr(o, attr_name)
                        if attr_value is not None:
                            if isinstance(attr_value, SQLModel):
                                data[attr_name] = self.default(attr_value)
                            elif isinstance(attr_value, list):
                                data[attr_name] = []
                                for item in attr_value:  # type: ignore
                                    if isinstance(item, SQLModel):
                                        data[attr_name].append(self.default(item))
                                    else:
                                        data[attr_name].append(item)
                    except Exception:
                        pass
            
            # Handle properties
            for attr_name in dir(o.__class__):
                if isinstance(getattr(o.__class__, attr_name, None), property):
                    if attr_name.startswith('__') or attr_name.startswith('model_'):
                        continue
                    if attr_name in data:
                        continue
                    try:
                        attr_value = getattr(o, attr_name)
                        if attr_value is not None:
                            if isinstance(attr_value, SQLModel):
                                data[attr_name] = self.default(attr_value)
                            elif isinstance(attr_value, list):
                                data[attr_name] = []
                                for item in attr_value:  # type: ignore
                                    if isinstance(item, SQLModel):
                                        data[attr_name].append(self.default(item))
                                    else:
                                        data[attr_name].append(item)
                            else:
                                data[attr_name] = attr_value
                    except Exception:
                        pass
            
            return data
        
        if isinstance(o, datetime):
            if o.tzinfo is None:
                o = o.replace(tzinfo=timezone.utc)
            utc_dt = o.astimezone(timezone.utc)
            return utc_dt.isoformat()
        
        if isinstance(o, Decimal):
            return float(o)
        
        return json.JSONEncoder.default(self, o)