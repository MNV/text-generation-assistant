from __future__ import annotations

from typing import Any, Sequence

from fastapi import Depends
from pydantic import UUID5
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from models import NEREntitySelection
from repositories.user_entity_repository import NEREntitySelectionRepository
from schemas.ner import Entity


class UserEntityService:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.ner_entity_selection_repository = NEREntitySelectionRepository(session)

    async def save_user_selections(
        self, resume_id: UUID5, entities: dict[str, list[Entity]]
    ) -> None:
        """
        Store selected entities for a specific resume.
        First deletes all previous selections for that resume and recreates them from the new list.
        """

        await self.ner_entity_selection_repository.delete_all_by(resume_id=resume_id)

        new_entries = [
            NEREntitySelection(
                resume_id=resume_id,
                entity=entity.text,
                entity_type=entity.label,
                researched=False,
            )
            for entity_list in entities.values()
            for entity in entity_list
        ]

        for entry in new_entries:
            await self.ner_entity_selection_repository.create_model(entry)

    async def get_user_selections(
        self, resume_id: UUID5
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        Retrieve selected entities for a specific resume.
        """

        return await self.ner_entity_selection_repository.find_all_by(
            limit=1000, resume_id=resume_id
        )
