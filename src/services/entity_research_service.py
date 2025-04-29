from fastapi import Depends
from pydantic import UUID5
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from models.ner import NEREntityResearch
from repositories.user_entity_repository import NEREntitySelectionRepository
from repositories.user_entity_research_repository import NEREntityResearchRepository

from baml_client.async_client import b

from services.vector_store_service import VectorStoreService


class EntityResearchService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.ner_research_repository = NEREntityResearchRepository(session)
        self.selection_repository = NEREntitySelectionRepository(session)
        self.vector_store_service = VectorStoreService()

    async def research_entities(self, resume_id: UUID5) -> dict[str, str]:
        """Research selected entities and store results."""

        selections = await self.selection_repository.find_all_by(
            limit=10, resume_id=resume_id, researched=False
        )

        if not selections:
            return {}

        research_results: dict[str, str] = {}

        entity_map = {selection.entity: selection.id for selection in selections}
        entities_to_research = list(entity_map.keys())
        research_output = await b.ResearchEntities(entities_to_research)

        for entity, result in research_output.items():
            selection_id = entity_map.get(entity)
            if not selection_id:
                continue

            await self.ner_research_repository.upsert_model(
                NEREntityResearch(
                    resume_id=resume_id,
                    entity_id=selection_id,
                    research=result,
                ),
                conflict_fields=["resume_id", "entity_id"],
            )

            await self.selection_repository.update_model(selection_id, researched=True)
            research_results[entity] = result

            await self.vector_store_service.add_document(
                text=result,
                metadata={
                    "resume_id": str(resume_id),
                    "type": "entity_research",
                    "entity": entity,
                },
            )

        return research_results
