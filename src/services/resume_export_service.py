from pathlib import Path

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


class ResumeExportService:
    def __init__(self, letters_dir: str = "./uploads/letters"):
        self.letters_dir = Path(letters_dir)
        self.letters_dir.mkdir(parents=True, exist_ok=True)

    async def get_file_path(self, file_id: str) -> Path:
        return self.letters_dir / f"{file_id}.docx"

    async def create_file(self, file_id: str, letter_text: str) -> Path:
        file_path = await self.get_file_path(file_id)

        document = Document()
        for paragraph_text in letter_text.split("\n\n"):
            paragraph = document.add_paragraph(paragraph_text.strip())
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        document.save(str(file_path))

        return file_path
