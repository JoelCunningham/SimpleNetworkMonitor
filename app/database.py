from typing import Any, Generic, Type, TypeVar

from sqlalchemy import Engine
from sqlalchemy.orm import joinedload
from sqlmodel import Session, SQLModel, create_engine, select

from app.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=Any)

class Query(Generic[T]):
    def __init__(self, engine: Engine, model: Type[T]):
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
        
class Database:
    url: str
    engine: Engine

    def __init__(self, db_url: str):
        self.url = db_url
        self.engine = create_engine(self.url, connect_args={"check_same_thread": False})

        import app.models.category  # type: ignore[unused-import]
        import app.models.device  # type: ignore[unused-import]
        import app.models.discovery  # type: ignore[unused-import]
        import app.models.location  # type: ignore[unused-import]
        import app.models.mac  # type: ignore[unused-import]
        import app.models.owner  # type: ignore[unused-import]
        import app.models.port  # type: ignore[unused-import]

        SQLModel.metadata.create_all(self.engine)
    
    def select_all(self, model: Type[T]) -> Query[T]:
        """Return a query object for all rows of the given model."""
        return Query(self.engine, model)
    
    def select_by_id(self, model: Type[T], id: int) -> Query[T]:
        """Return a Query pre-filtered by primary key."""
        return self.select_all(model).where(model.id == id)

    def create(self, instance: BaseModel) -> None:
        """Add an instance to the database."""
        with Session(self.engine) as session:
            session.add(instance)
            session.commit()
    
    def update(self, instance: BaseModel) -> None:
        """Update an existing instance in the database."""
        with Session(self.engine) as session:
            session.merge(instance)
            session.commit()
    
    def delete(self, instance: BaseModel) -> None:
        """Delete an instance from the database."""
        with Session(self.engine) as session:
            session.delete(instance)
            session.commit()