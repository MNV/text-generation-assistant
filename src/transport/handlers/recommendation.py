from fastapi import APIRouter, HTTPException, Depends
from services.rag_service import RAGService
from services.ner_service import NERService
from services.entity_research_service import EntityResearchService
from services.user_entity_service import UserEntityService
from services.resume_parser_service import ResumeParserService
from schemas.generation import RecommendationRequest, RecommendationResponse

router = APIRouter()

# Dependency Injection
rag_service = RAGService()
ner_service = NERService()
research_service = EntityResearchService()
user_entity_service = UserEntityService()
resume_parser_service = ResumeParserService()


@router.post("/api/v1/recommendations", response_model=RecommendationResponse)
async def generate_recommendation(request: RecommendationRequest):
    """Generate a recommendation letter using RAG and enriched context."""
    # Extract input data
    principal_resume_id = request.personalities.principal.resume.file_id
    grantee_resume_id = request.personalities.grantee.resume.file_id
    directives = request.recommendation.directives
    circumstances = (
        request.personalities.circumstances or "No specific circumstances provided."
    )

    # Validate file IDs
    if not principal_resume_id or not grantee_resume_id:
        raise HTTPException(
            status_code=400, detail="Both resume file IDs are required."
        )

    # Parse and extract text from resumes
    principal_text = await resume_parser_service.get_resume_text(principal_resume_id)
    grantee_text = await resume_parser_service.get_resume_text(grantee_resume_id)

    if not principal_text or not grantee_text:
        raise HTTPException(
            status_code=404, detail="Could not retrieve resume content."
        )

    # Extract and store entities for both principal and grantee
    principal_entities = await ner_service.extract_entities(
        principal_text, user_id="principal", language="en"
    )
    grantee_entities = await ner_service.extract_entities(
        grantee_text, user_id="grantee", language="en"
    )

    # Store user-selected entities and trigger research for selected entities
    await user_entity_service.save_user_selections(
        "principal", principal_entities.dict()["entities"]
    )
    await user_entity_service.save_user_selections(
        "grantee", grantee_entities.dict()["entities"]
    )

    # Research selected entities for both principal and grantee
    await research_service.research_entities(
        entities=[
            entity["text"] for entity in principal_entities.dict()["entities"]["SKILL"]
        ],
        user_id="principal",
    )
    await research_service.research_entities(
        entities=[
            entity["text"] for entity in grantee_entities.dict()["entities"]["SKILL"]
        ],
        user_id="grantee",
    )

    # Generate recommendation letter using enriched context
    result = rag_service.generate_recommendation(
        query="Generate a recommendation letter.",
        principal_id="principal",
        grantee_id="grantee",
        directives=directives,
        circumstances=circumstances,
    )

    return RecommendationResponse(recommendation=result)
