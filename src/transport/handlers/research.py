from fastapi import APIRouter, Depends
from pydantic import UUID5

from services.entity_research_service import EntityResearchService

router = APIRouter()


@router.post("/resume/{resume_id}")
async def research_entities(
    resume_id: UUID5,
    research_service: EntityResearchService = Depends(),
):
    """Research selected entities."""

    return {"data": await research_service.research_entities(resume_id=resume_id)}
