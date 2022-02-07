from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class QueryModel(BaseModel):
    base: str
    filter: str

    def return_format(self, **kwargs):
        query = f"{self.base} {self.filter};"
        return query.format(**kwargs)


class QueriesModel(BaseModel):
    read: QueryModel
    update: QueryModel


class TableModel(BaseModel):
    tables_schema: str = Field(alias='schema')
    name: str
    fields: str
    filter_filed: str


class Tables(BaseModel):
    events: TableModel
    welcome: TableModel
    others: TableModel


class TableDataModel(BaseModel):
    id: UUID
    created_at: datetime


class Events(TableDataModel):
    schema_name: str
    table_name: str
    record_id: UUID
    processed: bool

    def post_payload(self):
        return {
            "table_name": self.table_name,
            "record_id": str(self.record_id)
        }


class Welcome(TableDataModel):
    user_id: UUID
    template_id: UUID


class Others(TableDataModel):
    template_id: UUID
    title: str
    description: str
