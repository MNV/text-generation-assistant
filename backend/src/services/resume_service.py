from __future__ import annotations

import hashlib
import uuid
from pathlib import Path

from fastapi import Depends
from pydantic.v1 import UUID5
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from logger import logger
from models.file import FileResume
from repositories.file_repository import FileResumeRepository
from settings import settings


class ResumeService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.upload_dir = Path(settings.resume.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.file_resume_repository = FileResumeRepository(session)

    async def save_file(
        self, file_content: bytes, file_extension: str
    ) -> tuple[str, bool]:
        """
        Save file only if it does not exist.
        """

        file_id = await self._generate_file_id(file_content)
        new_filename = f"{file_id}.{file_extension}"
        file_path = self.upload_dir / new_filename

        if file_path.exists():
            logger.info("Uploaded file exists. Skipping.")
            return file_id, False

        with open(file_path, "wb") as f:
            logger.info("Uploaded file has been saved.")
            f.write(file_content)

        return file_id, True

    async def save_file_metadata(
        self, file_id: str, filename: str, file_extension: str
    ) -> None:
        existing = await self.file_resume_repository.find_all_by(
            limit=1,
            file_id=file_id,
        )

        if existing:
            await self.file_resume_repository.update_model(
                primary_key=existing[0].id,
                filename=filename,
                file_extension=file_extension,
            )
        else:
            model = FileResume(
                file_id=file_id,
                filename=filename,
                file_extension=file_extension,
            )
            await self.file_resume_repository.create_model(model)

    async def get_file_path(self, file_id: UUID5) -> Path | None:
        """
        Retrieve the file path based on file_id.
        """

        file_id_str = str(file_id)
        for file in self.upload_dir.iterdir():
            if file.stem == file_id_str:
                return file

        return None

    async def list_resumes(self) -> list[dict]:
        file_records = await self.file_resume_repository.find_all_by(
            limit=100,
            order_by=self.file_resume_repository.get_attr("created_at").desc(),
        )

        return [
            {
                "file_id": str(file.file_id),
                "filename": file.filename,
                "file_extension": file.file_extension,
                "created_at": file.created_at.isoformat() if file.created_at else None,
            }
            for file in file_records
        ]

    async def delete_resume(self, file_id: UUID5) -> None:
        file_record = await self.file_resume_repository.find_all_by(
            file_id=str(file_id), limit=1
        )
        if file_record and file_record[0]:
            await self.file_resume_repository.delete_by(id=file_record[0].id)

        file_path = await self.get_file_path(file_id)
        if file_path and file_path.exists():
            file_path.unlink()

    @staticmethod
    async def _generate_file_id(file_content: bytes) -> str:
        """
        Generate a UUID5 based on the SHA-256 hash of file content.
        """

        content_hash = hashlib.sha256(file_content).hexdigest()
        return str(
            uuid.uuid5(uuid.UUID(settings.resume.file_uuid_namespace), content_hash)
        )
