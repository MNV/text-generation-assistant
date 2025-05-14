from typing import Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint, Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship

from models.mixins import TimeStampMixin


class NEREntity(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "ner_entity"

    id: Optional[int] = Field(default=None, primary_key=True)
    resume_id: UUID = Field(
        foreign_key="file_resume.file_id", index=True, nullable=False
    )
    facts: Optional[dict] = Field(default=None, sa_type=JSONB, nullable=True)
    entities: dict = Field(sa_type=JSONB, nullable=False)

    resume: Optional["FileResume"] = Relationship(back_populates="ner_entities")


class NEREntitySelection(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "ner_entity_selection"

    id: Optional[int] = Field(default=None, primary_key=True)
    resume_id: UUID = Field(
        foreign_key="file_resume.file_id", index=True, nullable=False
    )
    entity: str = Field(nullable=False)
    entity_type: str = Field(nullable=False)
    researched: bool = Field(default=False)

    researches: list["NEREntityResearch"] = Relationship(back_populates="selection")
    resume: Optional["FileResume"] = Relationship(back_populates="ner_selections")


class NEREntityResearch(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "ner_entity_research"
    __table_args__ = (
        UniqueConstraint("resume_id", "entity_id", name="uix_resume_id_entity_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    resume_id: UUID = Field(
        foreign_key="file_resume.file_id", index=True, nullable=False
    )
    entity_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("ner_entity_selection.id", ondelete="CASCADE")
        ),
    )
    research: str = Field(nullable=False)

    selection: Optional["NEREntitySelection"] = Relationship(
        back_populates="researches"
    )
    resume: Optional["FileResume"] = Relationship(back_populates="ner_researches")
