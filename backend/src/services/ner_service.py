from __future__ import annotations

from collections import defaultdict
from typing import List, Dict, Set

from baml_client.types import Resume
from fastapi import Depends
from pydantic import UUID5
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from models import NEREntity
from repositories.ner_repository import NERRepository
from schemas.ner import NERResult, Entity


class NERService:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.ner_repository = NERRepository(session)

    async def store_facts(self, resume_id: UUID5, facts: Resume) -> None:
        """Persist or update the parsed facts for the specified resume ID."""
        existing = await self.ner_repository.find_all_by(limit=1, resume_id=resume_id)

        if existing:
            await self.ner_repository.update_model(
                primary_key=existing[0].id, facts=facts.model_dump(exclude_none=True)
            )
        else:
            model = NEREntity(
                resume_id=resume_id,
                entities={},
                facts=facts.model_dump(exclude_none=True),
            )
            await self.ner_repository.create_model(model)

    async def extract_entities(
        self, resume_id: UUID5, facts: Resume, language: str = "ru"
    ) -> NERResult:
        """
        Extract named entities from facts.
        """

        entity_dict: Dict[str, List[Entity]] = defaultdict(list)
        seen: Set[str] = set()

        def add(label: str, value: str | None):
            if not value:
                return
            text = value.strip().lower()
            if text and text not in seen:
                entity_dict[label].append(
                    Entity(label=label, text=text, language=language)
                )
                seen.add(text)

        for skill in facts.skills or []:
            add("SKILL", skill)

        for project in facts.projects or []:
            add("PROJECT", project.title)
            for tech in project.technologies or []:
                add("SKILL", tech)

        for exp in facts.experience or []:
            add("ORG", exp.company)

        for edu in facts.education or []:
            add("ORG", edu.institution)

        for cert in facts.certifications or []:
            add("CERTIFICATION", cert)

        for achievement in facts.achievements or []:
            add("ACHIEVEMENT", achievement)

        for pub in facts.publications or []:
            add("ACHIEVEMENT", pub.title)

        for ref in facts.references or []:
            add("PERSON", ref.name)

        add("GPE", facts.location)

        result = NERResult(entities=dict(entity_dict))

        await self.store_entities(resume_id=resume_id, entities=result)

        return result

    async def store_entities(self, resume_id: UUID5, entities: NERResult) -> None:
        """
        Persist or update the NER result for the specified resume ID.
        """

        existing = await self.ner_repository.find_all_by(limit=1, resume_id=resume_id)
        if existing:
            return await self.ner_repository.update_model(
                primary_key=existing[0].id, entities=entities.model_dump()["entities"]
            )
        else:
            model = NEREntity(
                resume_id=resume_id, entities=entities.model_dump()["entities"]
            )
            await self.ner_repository.create_model(model)

    async def get_entities(self, resume_id: UUID5) -> dict | None:
        existing = await self.ner_repository.find_all_by(resume_id=resume_id, limit=1)

        return existing[0].entities if existing else None
