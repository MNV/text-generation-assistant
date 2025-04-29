from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class ResumeInfo(BaseModel):
    file_id: UUID
    url: Optional[HttpUrl] = None


class Personality(BaseModel):
    name: Optional[str] = None
    resume: ResumeInfo


class Personalities(BaseModel):
    principal: Personality
    grantee: Personality
    circumstances: Optional[str] = None


class RecommendationType(str, Enum):
    enrollment = "enrollment"
    job = "job"
    visa = "visa"


class RecommendationDetails(BaseModel):
    type: RecommendationType
    directives: Optional[str] = None


class RecommendationRequest(BaseModel):
    personalities: Personalities
    recommendation: RecommendationDetails
