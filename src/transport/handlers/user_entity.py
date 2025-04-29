from fastapi import APIRouter, HTTPException, Depends
from pydantic import UUID5

from schemas.ner import Entity
from services.user_entity_service import UserEntityService

router = APIRouter()


@router.post("/resume/{resume_id}/select")
async def select_entities(
    resume_id: UUID5,
    entities: dict[str, list[Entity]],
    service: UserEntityService = Depends(),
):
    """Allow users to select entities for research and RAG."""
    if not entities:
        raise HTTPException(status_code=400, detail="Entity list cannot be empty.")

    await service.save_user_selections(resume_id, entities)
    return {"status": "success", "message": "Entities selected."}


@router.get("/resume/{resume_id}/selected")
async def get_selected_entities(
    resume_id: UUID5, service: UserEntityService = Depends()
):
    """Retrieve user-selected entities."""

    return {"data": await service.get_user_selections(resume_id)}
