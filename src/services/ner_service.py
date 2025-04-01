import spacy
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from integrations.db.session import get_session
from models import NEREntity
from ner.ner_patterns import (
    skill_patterns,
    certification_patterns,
    project_patterns,
    achievement_patterns,
)
from schemas.ner import NERResult, Entity
from collections import defaultdict
from typing import List, Dict
from repositories.ner_repository import NERRepository
from services.rag_service import RAGService
from services.entity_research_service import EntityResearchService
from services.user_entity_service import UserEntityService


class NERService:
    def __init__(
        self,
        rag_service: RAGService = Depends(),
        entity_research_service: EntityResearchService = Depends(),
        user_entity_service: UserEntityService = Depends(),
        session: AsyncSession = Depends(get_session),
    ):
        self.session = session
        self.nlp_en = spacy.load("en_core_web_trf")
        self.nlp_ru = spacy.load("ru_core_news_lg")
        self.ner_repository = NERRepository(session)
        self.rag_service = rag_service
        self.entity_research_service = entity_research_service
        self.user_entity_service = user_entity_service

        # Add custom patterns for skills, projects, etc.
        for nlp in [self.nlp_en, self.nlp_ru]:
            ruler = nlp.add_pipe("entity_ruler", before="ner")
            ruler.add_patterns(
                skill_patterns
                + certification_patterns
                + project_patterns
                + achievement_patterns
            )

    async def extract_entities(
        self, text: str, user_id: str, language: str = "en"
    ) -> NERResult:
        """Extract entities from text and store them in DB and ChromaDB."""
        nlp = self.nlp_en if language == "en" else self.nlp_ru
        doc = nlp(text)
        entity_dict: Dict[str, List[Entity]] = defaultdict(list)
        relevant_labels = {
            "PERSON",
            "ORG",
            "SKILL",
            "CERTIFICATION",
            "PROJECT",
            "GPE",
            "ACHIEVEMENT",
        }

        # Extract and clean entities
        for ent in doc.ents:
            if ent.label_ in relevant_labels:
                clean_text = " ".join(ent.text.strip().split())
                if clean_text:
                    entity = Entity(
                        label=ent.label_,
                        text=clean_text.lower(),
                        language=language,
                    )
                    entity_dict[ent.label_].append(entity)

        ner_result = NERResult(entities=dict(entity_dict))

        ner_model = NEREntity(user_id=user_id, entities=ner_result.model_dump())
        await self.ner_repository.create_model(ner_model)

        self.rag_service.store_document(
            document=text, metadata={"user_id": user_id, "language": language}
        )

        selected_entities = [
            {"text": entity.text, "label": entity.label}
            for label, entities in ner_result.entities.items()
            for entity in entities
        ]

        await self.user_entity_service.save_user_selections(user_id, selected_entities)
        await self.entity_research_service.research_entities(
            entities=[entity["text"] for entity in selected_entities], user_id=user_id
        )

        return ner_result

    async def get_entities(self, user_id: str) -> NERResult:
        """Retrieve stored entities for a user, including researched content."""
        if results := await self.ner_repository.find_all_by(limit=1, user_id=user_id):
            return NERResult(**results[0].entities)
        return NERResult(entities={})

    async def get_researched_content(self, user_id: str) -> Dict[str, str]:
        """Fetch researched content for user-selected entities."""
        selections = await self.user_entity_service.get_user_selections(user_id)
        entity_texts = [selection["entity"] for selection in selections]
        return await self.entity_research_service.research_entities(
            entity_texts, user_id
        )
