from fastapi import APIRouter, HTTPException, Depends
from services.entity_research_service import EntityResearchService

router = APIRouter()
research_service = EntityResearchService()


@router.post("/research/entities")
async def research_entities(user_id: str, entities: list[str]):
    """Research selected entities using Perplexity API."""
    if not entities:
        raise HTTPException(status_code=400, detail="Entity list cannot be empty.")
    researched_content = await research_service.research_entities(entities, user_id)
    return {"status": "success", "data": researched_content}
