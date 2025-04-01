from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from integrations.db.session import get_session
from models.user_entity_selection import UserEntitySelection


class UserEntityRepository:
    def __init__(self, session: AsyncSession = get_session()):
        self.session = session

    async def save_user_selection(self, user_id: str, entities: list[dict]):
        """Save user-selected entities to the database."""
        for entity in entities:
            selection = UserEntitySelection(
                user_id=user_id,
                entity=entity["text"].lower(),
                entity_type=entity["label"].upper(),
                selected=True,
            )
            self.session.add(selection)
        await self.session.commit()

    async def get_user_selections(self, user_id: str) -> list[UserEntitySelection]:
        """Retrieve selected entities for a user."""
        query = select(UserEntitySelection).where(
            UserEntitySelection.user_id == user_id, UserEntitySelection.selected == True
        )
        result = await self.session.execute(query)
        return result.scalars().all()
