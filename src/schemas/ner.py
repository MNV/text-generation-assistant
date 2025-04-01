from pydantic import BaseModel
from typing import List, Dict


class Entity(BaseModel):
    label: str
    text: str
    language: str


class NERResult(BaseModel):
    entities: Dict[str, List[Entity]]
