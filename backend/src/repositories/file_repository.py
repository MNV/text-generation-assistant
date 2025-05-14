from typing import Type

from models.file import FileResume
from repositories.base_repository import BaseRepository


class FileResumeRepository(BaseRepository):

    @property
    def model(self) -> Type[FileResume]:
        return FileResume
