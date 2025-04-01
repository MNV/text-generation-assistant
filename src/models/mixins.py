from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field


class TimeStampMixin(BaseModel):
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
            nullable=False,
        ),
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
            onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        ),
    )
