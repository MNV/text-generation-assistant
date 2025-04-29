from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import UUID5

from schemas.recommendation import RecommendationRequest
from services.recommendation_service import RecommendationService
from services.resume_export_service import ResumeExportService

router = APIRouter()


@router.post("")
async def generate_recommendation(
    request: RecommendationRequest,
    recommendation_service: RecommendationService = Depends(),
    resume_export_service: ResumeExportService = Depends(),
):
    file_id = str(request.personalities.grantee.resume.file_id)
    letter_text = await recommendation_service.generate(request)
    await resume_export_service.create_file(file_id, letter_text)

    return {"text": letter_text, "file_id": file_id}


@router.get("/letter/{file_id}")
async def get_recommendation(
    file_id: UUID5,
    resume_export_service: ResumeExportService = Depends(),
):
    if file_path := await resume_export_service.get_file_path(file_id):
        return FileResponse(
            file_path,
            filename=file_path.name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
