from typing import Any

from sqlmodel import Relationship


class Relation:
    def forward(self, table_name: str, foreign_name: str) -> Any:
        relation_string = f"and_({foreign_name.capitalize()}.{table_name.lower()}_id=={table_name.capitalize()}.id, {foreign_name.capitalize()}.deleted==False)"
        return Relationship(back_populates=table_name.lower(), sa_relationship_kwargs={
            "primaryjoin": relation_string
        })  
        
    def backward(self, table_name: str, foreign_name: str) -> Any:
        plural_table_name = table_name[:-1] + "ies" if table_name[-1] == "y" else table_name + "s"
        relation_string = f"and_({table_name.capitalize()}.{foreign_name.lower()}_id=={foreign_name.capitalize()}.id, {foreign_name.capitalize()}.deleted==False)"
        return Relationship(back_populates=plural_table_name.lower(), sa_relationship_kwargs={
            "primaryjoin": relation_string
        })