from typing import List, Dict
from repositories.user_entity_repository import UserEntityRepository
from services.entity_research_service import EntityResearchService


class UserEntityService:
    def __init__(
        self,
        user_entity_repo: UserEntityRepository,
        research_service: EntityResearchService,
    ):
        self.user_entity_repo = user_entity_repo
        self.research_service = research_service

    async def save_user_selections(self, user_id: str, entities: List[Dict[str, str]]):
        """Save user selections and trigger research for selected entities."""
        await self.user_entity_repo.save_user_selection(user_id, entities)
        entity_texts = [entity["text"] for entity in entities]
        await self.research_service.research_entities(entity_texts, user_id)

    async def get_user_selections(self, user_id: str) -> List[Dict[str, str]]:
        """Retrieve user-selected entities."""
        selections = await self.user_entity_repo.get_user_selections(user_id)
        return [{"entity": sel.entity, "type": sel.entity_type} for sel in selections]
