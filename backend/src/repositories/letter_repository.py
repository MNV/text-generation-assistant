from typing import Type

from models.file import FileGeneratedLetter
from repositories.base_repository import BaseRepository


class FileGeneratedLetterRepository(BaseRepository):

    @property
    def model(self) -> Type[FileGeneratedLetter]:
        return FileGeneratedLetter
