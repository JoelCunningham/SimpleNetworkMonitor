from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

import Constants
import Exceptions
from Models.CategoryModel import Category  # type: ignore[unused-import]
from Models.DeviceModel import Device  # type: ignore[unused-import]
from Models.LocationModel import Location  # type: ignore[unused-import]
from Models.MacModel import Mac  # type: ignore[unused-import]
from Models.OwnerModel import Owner  # type: ignore[unused-import]
from Objects.Injectable import Injectable
from Services.AppConfig import AppConfig


class Database(Injectable):
    _engine: Engine
    
    def __init__(self, config: AppConfig) -> None:
        try:
            self._engine = create_engine(
                config.database, 
                echo=False,
                pool_pre_ping=True,
                pool_recycle=Constants.DATABASE_POOL_RECYCLE_TIME,
            )
            
            SQLModel.metadata.create_all(self._engine)
            
        except Exception as e:
            raise Exceptions.DatabaseError(Constants.DB_INIT_FAILED.format(error=str(e))) from e

    def get_session(self) -> Session:
        return Session(self._engine)
    
    def close(self) -> None:
        try:
            self._engine.dispose()
        except Exception as e:
            raise Exceptions.DatabaseError(Constants.DB_CLOSE_FAILED.format(error=str(e))) from e
