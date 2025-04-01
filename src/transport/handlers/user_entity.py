from fastapi import APIRouter, HTTPException, Depends
from services.user_entity_service import UserEntityService
from typing import List, Dict

router = APIRouter()


@router.post("/entities/select")
async def select_entities(
    user_id: str, entities: List[Dict[str, str]], service: UserEntityService = Depends()
):
    """Allow users to select entities for research and RAG."""
    if not entities:
        raise HTTPException(status_code=400, detail="Entity list cannot be empty.")

    await service.save_user_selections(user_id, entities)
    return {"status": "success", "message": "Entities selected and research initiated."}


@router.get("/entities/selected")
async def get_selected_entities(user_id: str, service: UserEntityService = Depends()):
    """Retrieve user-selected entities."""
    selections = await service.get_user_selections(user_id)

    return {"status": "success", "data": selections}
