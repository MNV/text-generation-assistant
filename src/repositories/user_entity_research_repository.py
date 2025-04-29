from typing import Type, Sequence

from pydantic import UUID5
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.ner import NEREntityResearch
from repositories.base_repository import BaseRepository


class NEREntityResearchRepository(BaseRepository):

    @property
    def model(self) -> Type[NEREntityResearch]:
        return NEREntityResearch

    async def find_all_with_selection_by_resume(
        self, resume_id: UUID5
    ) -> Sequence[NEREntityResearch]:
        query = (
            select(self.model)
            .options(selectinload(self.model.selection))
            .where(self.model.resume_id == resume_id)
        )
        result = await self.session.execute(query)

        return result.scalars().all()
