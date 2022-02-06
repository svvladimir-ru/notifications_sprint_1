from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class QueryModel(BaseModel):
    base: str

    def format(self, attrs: Optional[list] = None, **kwargs) -> str:
        query = self.base
        if attrs:
            for name in attrs:
                attr = getattr(self, name)
                query += f" {attr}"

        query += ";"

        return query.format(**kwargs)


class ReadQueryModel(QueryModel):
    filter: str


class Queries(BaseModel):
    create: QueryModel
    read: ReadQueryModel


class TableModel(BaseModel):
    t_schema: str = Field(alias='schema')
    name: str
    fields: str
    filter_filed: Optional[str] = None


class Tables(BaseModel):
    templates: TableModel
    others: TableModel


class Event(BaseModel):
    template_id: UUID
    title: str
    description: str

    def for_create(self):
        return {
            "values": f"'{self.template_id}', '{self.title}', '{self.description}'"
        }


class EventModel(BaseModel):
    title: str
    description: str


class EventsFileModel(BaseModel):
    events: list[EventModel]
