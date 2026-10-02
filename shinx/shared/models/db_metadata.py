from pydantic import BaseModel

class Extension(BaseModel):
    name: str
    default_version: str | None = None
    installed_version: str | None = None
    comment: str | None = None

class Column(BaseModel):
    name: str
    data_type: str
    is_nullable: str
    column_default: str

class Constraint(BaseModel):
    name: str
    type: str

class Index(BaseModel):
    name: str
    indexdef: str

class TableMetaData(BaseModel):
    name: str
    schema_name: str
    columns: list[Column]
    constraints: list[Constraint]
    indexes: list[Index]

class ViewColumn(BaseModel):
    column_name: str
    ordinal_position: int
    data_type: str
    is_nullable: str

class View(BaseModel):
    name: str
    schema_name: str
    owner: str | None = None
    definition: str | None = None
    is_updatable: bool | None = None
    is_insertable_into: bool | None = None
    is_trigger_updatable: bool | None = None
    is_trigger_deletable: bool | None = None
    is_trigger_insertable: bool | None = None
    is_materialized: bool | None = None
    description: str | None = None
    columns: list[ViewColumn] = []

class DBMetadata(BaseModel):
    version: str
    extensions: list[Extension]
    tables: list[TableMetaData]
    views: list[View]