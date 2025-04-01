from __future__ import annotations

import hashlib
import uuid
from pathlib import Path

from pydantic.v1 import UUID5

from logger import logger
from settings import settings


class ResumeService:
    def __init__(self):
        self.upload_dir = Path(settings.resume.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(
        self, file_content: bytes, file_extension: str
    ) -> tuple[str, bool]:
        """
        Save file only if it does not exist.
        """

        file_id = await self._generate_file_id(file_content)
        new_filename = f"{file_id}{file_extension}"
        file_path = self.upload_dir / new_filename

        if file_path.exists():
            logger.info("Uploaded file exists. Skipping.")
            return file_id, False

        with open(file_path, "wb") as f:
            logger.info("Uploaded file has been saved.")
            f.write(file_content)

        return file_id, True

    async def get_file_path(self, file_id: UUID5) -> Path | None:
        """
        Retrieve the file path based on file_id.
        """

        file_id_str = str(file_id)
        for file in self.upload_dir.iterdir():
            if file.stem == file_id_str:
                return file

        return None

    @staticmethod
    async def _generate_file_id(file_content: bytes) -> str:
        """
        Generate a UUID5 based on the SHA-256 hash of file content.
        """

        content_hash = hashlib.sha256(file_content).hexdigest()
        return str(
            uuid.uuid5(uuid.UUID(settings.resume.file_uuid_namespace), content_hash)
        )
