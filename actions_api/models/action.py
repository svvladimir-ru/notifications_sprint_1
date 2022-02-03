from pydantic import BaseModel


class ActionModel(BaseModel):
    email: str
    action: str
    i: int
