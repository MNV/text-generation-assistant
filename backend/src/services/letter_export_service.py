import io
import uuid
from pathlib import Path

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from models import FileGeneratedLetter
from repositories.letter_repository import FileGeneratedLetterRepository


class LetterExportService:
    def __init__(
        self,
        letters_dir: str = "./uploads/letters",
        session: AsyncSession = Depends(get_session),
    ):
        self.letters_dir = Path(letters_dir)
        self.letters_dir.mkdir(parents=True, exist_ok=True)
        self.letter_repository = FileGeneratedLetterRepository(session)

    async def get_file_path(self, file_id: str) -> Path:
        return self.letters_dir / f"{file_id}.docx"

    async def create_file(self, letter_text: str) -> str:
        document = Document()
        paragraph_texts = [p.strip() for p in letter_text.split("\n\n") if p.strip()]
        total_paragraphs = len(paragraph_texts)

        for idx, paragraph_text in enumerate(paragraph_texts):
            paragraph = document.add_paragraph(paragraph_text)

            if not (idx < 2 or idx == total_paragraphs - 1):
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        file_buffer = io.BytesIO()
        document.save(file_buffer)
        file_content = file_buffer.getvalue()

        file_id = str(uuid.uuid4())
        file_path = await self.get_file_path(file_id)
        with open(file_path, "wb") as f:
            f.write(file_content)

        return file_id

    async def save_file_metadata(
        self, letter_id: str, resume_id: str, filename: str, file_extension: str
    ) -> None:
        model = FileGeneratedLetter(
            letter_id=letter_id,
            resume_id=resume_id,
            filename=filename,
            file_extension=file_extension,
        )
        await self.letter_repository.create_model(model)

    async def list_letters_by_resume(self, resume_id: str) -> list[dict]:
        letters = await self.letter_repository.find_all_by(
            limit=100,
            resume_id=resume_id,
            order_by=self.letter_repository.get_attr("created_at").desc(),
        )
        return [
            {
                "letter_id": str(letter.letter_id),
                "filename": letter.filename,
                "file_extension": letter.file_extension,
                "created_at": (
                    letter.created_at.isoformat() if letter.created_at else None
                ),
            }
            for letter in letters
        ]

    async def delete_letter(self, letter_id: uuid.UUID) -> None:
        letter_record = await self.letter_repository.find_all_by(
            letter_id=str(letter_id), limit=1
        )
        if letter_record and letter_record[0]:
            await self.letter_repository.delete_by(id=letter_record[0].id)

        file_path = await self.get_file_path(str(letter_id))
        if file_path and file_path.exists():
            file_path.unlink()
