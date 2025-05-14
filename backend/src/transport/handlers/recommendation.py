from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import FileResponse
from pydantic import UUID5

from schemas.recommendation import RecommendationRequest
from services.recommendation_service import RecommendationService
from services.letter_export_service import LetterExportService

router = APIRouter()


@router.post("")
async def generate_recommendation(
    request: RecommendationRequest,
    recommendation_service: RecommendationService = Depends(),
    letter_service: LetterExportService = Depends(),
):
    letter_text = await recommendation_service.generate(request)
    letter_id = await letter_service.create_file(letter_text)
    await letter_service.save_file_metadata(
        letter_id=letter_id,
        resume_id=str(request.personalities.grantee.resume.file_id),
        filename=f"Recommendation Letter for {request.recommendation.type.value.capitalize()}",
        file_extension="docx",
    )

    return {"letter_id": letter_id}


@router.get("/letter/{file_id}")
async def get_recommendation(
    file_id: UUID,
    letter_service: LetterExportService = Depends(),
):
    if file_path := await letter_service.get_file_path(str(file_id)):
        return FileResponse(
            file_path,
            filename=file_path.name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")


@router.delete("/letter/{letter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_letter(
    letter_id: UUID,
    letter_service: LetterExportService = Depends(),
):
    await letter_service.delete_letter(letter_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/resume/{resume_id}/letters")
async def list_generated_letters(
    resume_id: UUID5,
    letter_service: LetterExportService = Depends(),
):
    """
    List all generated letters associated with the grantee resume.
    """
    return {"letters": await letter_service.list_letters_by_resume(resume_id)}
