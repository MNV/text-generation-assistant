from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from models.mixins import TimeStampMixin


class FileResume(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "file_resume"

    id: Optional[int] = Field(default=None, primary_key=True)
    file_id: UUID = Field(nullable=False, unique=True)
    filename: str = Field(nullable=False, max_length=255)
    file_extension: str = Field(nullable=False, max_length=10)

    ner_entities: list["NEREntity"] = Relationship(
        back_populates="resume", cascade_delete=True
    )
    ner_selections: list["NEREntitySelection"] = Relationship(
        back_populates="resume", cascade_delete=True
    )
    ner_researches: list["NEREntityResearch"] = Relationship(
        back_populates="resume", cascade_delete=True
    )
    generated_letters: list["FileGeneratedLetter"] = Relationship(
        back_populates="resume", cascade_delete=True
    )


class FileGeneratedLetter(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "file_generated_letter"

    id: Optional[int] = Field(default=None, primary_key=True)
    letter_id: UUID = Field(nullable=False, unique=True)
    resume_id: UUID = Field(
        foreign_key="file_resume.file_id", index=True, nullable=False
    )
    filename: str = Field(nullable=False, max_length=255)
    file_extension: str = Field(nullable=False, max_length=10)

    resume: Optional["FileResume"] = Relationship(back_populates="generated_letters")
