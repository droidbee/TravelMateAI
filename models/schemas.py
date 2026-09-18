from pydantic import BaseModel


class Destination(BaseModel):
    name: str
    country: str
    type: list[str]
    best_for: list[str]
    description: str