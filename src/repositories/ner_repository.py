from typing import Type

from models.ner import NEREntity
from repositories.base_repository import BaseRepository


class NERRepository(BaseRepository):

    @property
    def model(self) -> Type[NEREntity]:
        return NEREntity
