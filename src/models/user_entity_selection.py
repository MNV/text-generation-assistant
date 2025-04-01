from sqlmodel import SQLModel, Field
from typing import Optional
from models.mixins import TimeStampMixin


class UserEntitySelection(SQLModel, TimeStampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    entity: str = Field(nullable=False)
    entity_type: str = Field(nullable=False)
    selected: bool = Field(default=True)
