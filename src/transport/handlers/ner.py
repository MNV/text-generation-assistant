from fastapi import APIRouter, Depends, HTTPException
from schemas.ner import NERResult
from services.ner_service import NERService
from services.vector_store_service import VectorStoreService

router = APIRouter()


@router.post("/resume/{file_id}/ner/extract", response_model=NERResult)
async def extract_entities(file_id: str, ner_service: NERService = Depends()):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    return await ner_service.extract_entities(text, user_id, language)


@router.get("/ner/search")
async def search_entities(query: str, vector_service: VectorStoreService = Depends()):
    return await vector_service.search_entities(query)
