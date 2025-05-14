from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field


def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TimeStampMixin(BaseModel):
    created_at: Optional[datetime] = Field(
        default_factory=utc_now_naive,
        nullable=False,
    )
    updated_at: Optional[datetime] = Field(
        default_factory=utc_now_naive,
        nullable=True,
    )
