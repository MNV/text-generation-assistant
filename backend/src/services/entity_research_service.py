from baml_client.async_client import b
from fastapi import Depends
from pydantic import UUID5
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from models.ner import NEREntityResearch
from repositories.user_entity_repository import NEREntitySelectionRepository
from repositories.user_entity_research_repository import NEREntityResearchRepository
from services.vector_store_service import VectorStoreService


class EntityResearchService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.ner_research_repository = NEREntityResearchRepository(session)
        self.selection_repository = NEREntitySelectionRepository(session)
        self.vector_store_service = VectorStoreService()

    async def research_entities(self, resume_id: UUID5) -> dict[str, str]:
        """Research unresearched selected entities."""

        all_selections = await self.selection_repository.find_all_by(
            limit=1000, resume_id=resume_id
        )

        if not all_selections:
            return {}

        to_research = [s for s in all_selections if not s.researched]
        entity_map = {sel.entity: sel.id for sel in to_research}
        research_results = {}

        if entity_map:
            new_research_output = await b.ResearchEntities(list(entity_map.keys()))

            for entity, result in new_research_output.items():
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

                await self.selection_repository.update_model(
                    selection_id, researched=True
                )
                research_results[entity] = result

                await self.vector_store_service.add_document(
                    text=result,
                    metadata={
                        "resume_id": str(resume_id),
                        "type": "entity_research",
                        "entity": entity,
                    },
                )

        all_researches = await self.ner_research_repository.find_all_by(
            resume_id=resume_id, limit=10
        )

        full_results: dict[str, str] = {}
        for r in all_researches:
            if r.selection:
                full_results[r.selection.entity] = r.research

        return full_results
