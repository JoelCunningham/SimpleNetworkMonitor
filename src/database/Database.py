from typing import Optional

from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel, create_engine

import Constants
import Exceptions
from objects.AppConfig import AppConfig


class BaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True)
    deleted: bool = False

class Database:
    _engine: Optional[Engine] = None
    @classmethod
    def init(cls, config: AppConfig) -> None:
        if cls._engine is not None:
            raise Exceptions.DatabaseError(Constants.DB_ALREADY_INITIALIZED)
        
        try:
            cls._engine = create_engine(
                config.database, 
                echo=False,
                pool_pre_ping=True,
                pool_recycle=Constants.DATABASE_POOL_RECYCLE_TIME,
            )
            
            from database.models.CategoryModel import Category  # type: ignore[unused-import]
            from database.models.DeviceModel import Device  # type: ignore[unused-import]
            from database.models.LocationModel import Location  # type: ignore[unused-import]
            from database.models.MacModel import Mac  # type: ignore[unused-import]
            from database.models.OwnerModel import Owner  # type: ignore[unused-import]
            
            SQLModel.metadata.create_all(cls._engine)
        except Exception as e:
            raise Exceptions.DatabaseError(Constants.DB_INIT_FAILED.format(error=str(e))) from e

    @classmethod
    def get_session(cls) -> Session:
        if cls._engine is None:
            raise Exceptions.DatabaseError(Constants.DB_NOT_INITIALIZED)
        return Session(cls._engine)
    
    @classmethod
    def close(cls) -> None:
        if cls._engine is not None:
            try:
                cls._engine.dispose()
                cls._engine = None
            except Exception as e:
                raise Exceptions.DatabaseError(Constants.DB_CLOSE_FAILED.format(error=str(e))) from e


