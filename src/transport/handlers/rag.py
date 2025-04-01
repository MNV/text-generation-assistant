from fastapi import APIRouter, HTTPException, Depends
from services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()


@router.post("/rag/store")
async def store_document(document: str, metadata: dict):
    """Store documents in ChromaDB."""
    rag_service.store_document(document, metadata)

    return {"status": "success", "message": "Document stored successfully."}


@router.post("/rag/generate")
async def generate_recommendation(query: str, user_id: str):
    """Generate a recommendation letter using RAG."""
    result = rag_service.generate_recommendation(query, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No relevant information found.")

    return {"recommendation": result}
