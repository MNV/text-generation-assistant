from typing import Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship

from models.mixins import TimeStampMixin


class NEREntity(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "ner_entity"

    id: Optional[int] = Field(default=None, primary_key=True)
    resume_id: UUID = Field(index=True, nullable=False)
    facts: Optional[dict] = Field(default=None, sa_type=JSONB, nullable=True)
    entities: dict = Field(sa_type=JSONB, nullable=False)


class NEREntitySelection(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "ner_entity_selection"

    id: Optional[int] = Field(default=None, primary_key=True)
    resume_id: UUID = Field(index=True, nullable=False)
    entity: str = Field(nullable=False)
    entity_type: str = Field(nullable=False)
    researched: bool = Field(default=False)

    researches: list["NEREntityResearch"] = Relationship(back_populates="selection")


class NEREntityResearch(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "ner_entity_research"
    __table_args__ = (
        UniqueConstraint("resume_id", "entity_id", name="uix_resume_id_entity_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    resume_id: UUID = Field(index=True, nullable=False)
    entity_id: int = Field(foreign_key="ner_entity_selection.id", nullable=False)
    research: str = Field(nullable=False)

    selection: Optional["NEREntitySelection"] = Relationship(
        back_populates="researches"
    )
