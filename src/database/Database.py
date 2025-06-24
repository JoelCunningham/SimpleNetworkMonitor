from sqlmodel import SQLModel, create_engine, Session

class BaseModel(SQLModel):
    deleted: bool = False
    
from database.models.MacModel import Mac # type: ignore[unused-import]
from database.models.DeviceModel import Device # type: ignore[unused-import]
from database.models.OwnerModel import Owner # type: ignore[unused-import]
from database.models.LocationModel import Location # type: ignore[unused-import]
from database.models.CategoryModel import Category  # type: ignore[unused-import]

sqlite_file_name = "network_monitor.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=False)

class Database:
    @staticmethod
    def init():
        SQLModel.metadata.create_all(engine)

    @staticmethod
    def get_session():
        return Session(engine)


