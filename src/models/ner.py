from typing import Optional

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from models.mixins import TimeStampMixin


class NEREntity(SQLModel, TimeStampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    entities: dict = Field(sa_type=JSONB, nullable=False)
