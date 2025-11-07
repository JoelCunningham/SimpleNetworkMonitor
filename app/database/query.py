from typing import Any, TypeVar

from sqlalchemy import Engine
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

import app.database.models  # type: ignore[unused-import]
from app.database.interfaces import QueryInterface
from app.database.models import BaseModel

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=Any)

class Query(QueryInterface[T]):
    def __init__(self, engine: Engine, model: type[T]):
        self.engine = engine
        self.model = model
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
        
    def by_id(self, id: int) -> T | None:
        with Session(self.engine) as session:
            statement = select(self.model).options(joinedload("*")).where(self.model.id == id)
            return session.exec(statement).unique().first()
        