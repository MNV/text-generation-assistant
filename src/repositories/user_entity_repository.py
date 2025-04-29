from typing import Type

from models import NEREntitySelection
from repositories.base_repository import BaseRepository


class NEREntitySelectionRepository(BaseRepository):

    @property
    def model(self) -> Type[NEREntitySelection]:
        return NEREntitySelection
