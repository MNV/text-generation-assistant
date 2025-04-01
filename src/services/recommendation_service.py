import logging.config

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session

# from repositories.recommendation_repository import RecommendationRepository
from schemas.generation import RecommendationDataRequest

logging.config.fileConfig("logging.conf")
logger = logging.getLogger()


class RecommendationService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        # self.recommendation_repository = RecommendationRepository(session)

    async def generate(self, data: RecommendationDataRequest) -> str:
        return f"Accepted: {data}"
