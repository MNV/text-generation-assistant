from datetime import datetime

from baml_client.async_client import b
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from repositories.ner_repository import NERRepository
from repositories.user_entity_research_repository import NEREntityResearchRepository
from schemas.recommendation import RecommendationRequest
from services.vector_store_service import VectorStoreService


class RecommendationService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.research_repository = NEREntityResearchRepository(session)
        self.entity_repository = NERRepository(session)
        self.vector_store_service = VectorStoreService()

    async def generate(self, request: RecommendationRequest):
        principal_resume_id = request.personalities.principal.resume.file_id
        grantee_resume_id = request.personalities.grantee.resume.file_id
        circumstances = request.personalities.circumstances or ""
        directives = request.recommendation.directives or ""
        recommendation_type = request.recommendation.type.value

        principal_resume_facts = await self.entity_repository.find_all_by(
            resume_id=principal_resume_id, limit=1
        )
        grantee_resume_facts = await self.entity_repository.find_all_by(
            resume_id=grantee_resume_id, limit=1
        )

        if not principal_resume_facts or not grantee_resume_facts:
            raise ValueError("Resume facts not found in the database.")

        principal_facts = principal_resume_facts[0].facts
        grantee_facts = grantee_resume_facts[0].facts

        principal_researches = list(
            await self.research_repository.find_all_with_selection_by_resume(
                resume_id=principal_resume_id
            )
        )
        grantee_researches = list(
            await self.research_repository.find_all_with_selection_by_resume(
                resume_id=grantee_resume_id
            )
        )
        research_map = {
            res.selection.entity: res.research
            for res in principal_researches + grantee_researches
            if res.selection is not None
        }

        principal_context = await self.vector_store_service.retrieve(
            query="Key strengths, achievements, and professional background to recommend.",
            resume_id=str(principal_resume_id),
        )
        grantee_context = await self.vector_store_service.retrieve(
            query="Key achievements, skills, and potential for recommendation.",
            resume_id=str(grantee_resume_id),
        )

        return await b.GenerateRecommendationLetter(
            principal_facts=principal_facts,
            grantee_facts=grantee_facts,
            principal_context="\n\n".join(principal_context).strip(),
            grantee_context="\n\n".join(grantee_context).strip(),
            recommendation_type=recommendation_type,
            directives=directives,
            circumstances=circumstances,
            entity_research=research_map,
            extra={"current_date": datetime.today().strftime("%Y-%m-%d")},
        )
