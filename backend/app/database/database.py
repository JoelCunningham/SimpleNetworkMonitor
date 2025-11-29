from datetime import datetime
from typing import TypeVar

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

import app.database.models  # type: ignore[unused-import]
from app.database.interfaces import DatabaseInterface
from app.database.models import BaseModel
from app.database.query import Query

T = TypeVar("T", bound=BaseModel)

class Database(DatabaseInterface):
    url: str
    engine: Engine

    def __init__(self, db_url: str):
        self.url = db_url
        self.engine = create_engine(self.url, connect_args={"check_same_thread": False})
        SQLModel.metadata.create_all(self.engine)
    
    def select(self, model: type[T]) -> Query[T]:
        return Query(self.engine, model).where(model.deleted == False)  

    def create(self, instance: BaseModel) -> None:
        instance.created_at = datetime.now()
        with Session(self.engine) as session:
            session.add(instance)
            session.commit()
            session.refresh(instance)
    
    def update(self, instance: BaseModel) -> None:
        instance.updated_at = datetime.now()
        with Session(self.engine) as session:
            merged = session.merge(instance)
            session.commit()
            session.refresh(merged)
    
    def delete(self, instance: BaseModel) -> None:
        instance.updated_at = datetime.now()
        instance.deleted = True
        with Session(self.engine) as session:
            merged = session.merge(instance)
            session.commit()
            session.refresh(merged)
            
    def hard_delete(self, instance: BaseModel) -> None:
        with Session(self.engine) as session:
            merged = session.merge(instance)
            session.delete(merged)
            session.commit()