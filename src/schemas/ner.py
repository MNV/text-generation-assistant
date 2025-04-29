from pydantic import BaseModel


class Entity(BaseModel):
    label: str
    text: str
    language: str


class NERResult(BaseModel):
    entities: dict[str, list[Entity]]
