from datetime import datetime, timezone
from typing import Any, TypeVar

from sqlalchemy import Engine
from sqlalchemy.orm import joinedload
from sqlmodel import Session, SQLModel, create_engine, select

import app.database.models  # type: ignore[unused-import]
from app.database.interfaces import DatabaseInterface, QueryInterface
from app.database.models import BaseModel

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=Any)

class Query(QueryInterface[T]):
    def __init__(self, engine: Engine, model: type[T]):
        self.engine = engine
        self.statement = select(model).options(joinedload("*"))

    def where(self, condition: Any) -> "Query[T]":
        self.statement = self.statement.where(condition)
        return self
    
    def where_in(self, column: U, values: list[U]) -> "Query[T]":
        self.statement = self.statement.where(column.in_(values))
        return self
    
    def order_by(self, *criteria: Any) -> "Query[T]":
        self.statement = self.statement.order_by(*criteria)
        return self

    def all(self) -> list[T]:
        with Session(self.engine) as session:
            return list(session.exec(self.statement).unique())
        
    def first(self) -> T | None:
        with Session(self.engine) as session:
            return session.exec(self.statement).unique().first()
        
class Database(DatabaseInterface):
    url: str
    engine: Engine

    def __init__(self, db_url: str):
        self.url = db_url
        self.engine = create_engine(self.url, connect_args={"check_same_thread": False})
        SQLModel.metadata.create_all(self.engine)
    
    def select_all(self, model: type[T]) -> Query[T]:
        return Query(self.engine, model)
    
    def select_by_id(self, model: type[T], id: int) -> Query[T]:
        return self.select_all(model).where(model.id == id)

    def create(self, instance: BaseModel) -> None:
        instance.created_at = datetime.now(timezone.utc)
        with Session(self.engine) as session:
            session.add(instance)
            session.commit()
            session.refresh(instance)
    
    def update(self, instance: BaseModel) -> None:
        instance.updated_at = datetime.now(timezone.utc)
        with Session(self.engine) as session:
            merged = session.merge(instance)
            session.commit()
            session.refresh(merged)
    
    def delete(self, instance: BaseModel) -> None:
        with Session(self.engine) as session:
            session.delete(instance)
            session.commit()