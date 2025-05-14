from __future__ import annotations

from pydantic import BaseModel, Field


class Entity(BaseModel):
    label: str
    text: str
    language: str | None = Field(default=None)


class NERResult(BaseModel):
    entities: dict[str, list[Entity]]
