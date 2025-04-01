from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, UUID5
from typing import Optional, List, Dict


class Entity(BaseModel):
    text: str = Field(..., description="Extracted entity text")
    label: str = Field(
        ..., description="Type of entity, e.g., SKILL, PROJECT, CERTIFICATION"
    )


class ResearchedContent(BaseModel):
    entity: str = Field(..., description="Entity text")
    summary: str = Field(..., description="Summary of researched content")
    source_url: Optional[HttpUrl] = Field(
        default=None, description="Source URL for the researched content"
    )


class EnrichedContext(BaseModel):
    principal_context: List[ResearchedContent] = Field(
        default_factory=list, description="Enriched context for the principal"
    )
    grantee_context: List[ResearchedContent] = Field(
        default_factory=list, description="Enriched context for the grantee"
    )


class Resume(BaseModel):
    url: Optional[HttpUrl] = Field(default=None, description="Link to resume")
    file_id: Optional[UUID5] = Field(default=None, description="Resume text")


class Personality(BaseModel):
    name: str = Field(..., description="Full name of the person")
    resume: Resume = Field(default_factory=Resume, description="Resume details")
    selected_entities: List[Entity] = Field(
        default_factory=list, description="User-selected entities for research"
    )
    researched_content: List[ResearchedContent] = Field(
        default_factory=list,
        description="Researched content for user-selected entities",
    )


class RecommendationType(str, Enum):
    ENROLLMENT = "enrollment"
    JOB = "job"
    VISA = "visa"


class Recommendation(BaseModel):
    type: RecommendationType = Field(..., description="Type of recommendation")
    directives: Optional[str] = Field(
        default=None, description="Directives for the recommendation"
    )


class Personalities(BaseModel):
    principal: Personality = Field(..., description="Principal personality")
    grantee: Personality = Field(..., description="Grantee personality")
    circumstances: Optional[str] = Field(
        default=None, description="Circumstances of the meeting of persons"
    )


class RecommendationDataRequest(BaseModel):
    personalities: Personalities = Field(..., description="Personalities involved")
    recommendation: Recommendation = Field(..., description="Recommendation details")
    enriched_context: Optional[EnrichedContext] = Field(
        default=None, description="Enriched context based on researched data"
    )
