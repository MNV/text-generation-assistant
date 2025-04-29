import asyncio
import io
from pathlib import Path

import aiofiles
import docx
import pypdf

from baml_client.async_client import b
from baml_client.types import Resume
from fastapi import HTTPException


class ResumeParserService:
    async def get_resume_text(self, file_id: str) -> str:
        file_path = Path(f"./uploads/resumes/{file_id}.pdf")

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Resume file not found.")

        text = await self.parse_resume(file_path=file_path)
        return text

    async def parse_resume(self, file_path: Path) -> str:
        """Parses resume, extracts text, runs entity recognition, and triggers entity research."""

        file_extension = file_path.suffix.lower()
        async with aiofiles.open(file_path, "rb") as file:
            file_content = await file.read()

        return await self._extract_text(file_content, file_extension)

    async def _extract_text(self, file_content: bytes, file_extension: str) -> str:
        """Extract text from a given file content based on its extension."""

        extraction_methods = {
            ".pdf": self._extract_text_from_pdf,
            ".docx": self._extract_text_from_docx,
            ".txt": self._extract_text_from_txt,
        }

        extract_method = extraction_methods.get(file_extension)
        if not extract_method:
            raise ValueError(
                f"Unsupported file type: {file_extension}. Only PDF, DOCX, and TXT are allowed."
            )

        return await extract_method(file_content)

    async def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from a PDF file."""
        reader = pypdf.PdfReader(io.BytesIO(file_content))
        tasks = [self._extract_page_text(page) for page in reader.pages]
        extracted_texts = await asyncio.gather(*tasks)
        return "\n".join(filter(None, extracted_texts)).strip()

    @staticmethod
    async def _extract_page_text(page) -> str:
        """Extract text from a single PDF page."""
        return page.extract_text() or ""

    async def _extract_text_from_docx(self, file_content: bytes) -> str:
        """Extract text from a DOCX file."""
        return await asyncio.to_thread(self._read_docx, file_content)

    @staticmethod
    def _read_docx(file_content: bytes) -> str:
        """Read DOCX content."""
        text = []
        doc = docx.Document(io.BytesIO(file_content))
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return "\n".join(text).strip()

    @staticmethod
    async def _extract_text_from_txt(file_content: bytes) -> str:
        """Extract text from a TXT file."""
        return file_content.decode("utf-8").strip()

    @staticmethod
    async def extract_facts(text: str) -> Resume:
        """Extract structured information using BAML API."""
        return await b.ExtractResume(text)
