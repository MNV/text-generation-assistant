from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    Response,
    status,
)
from fastapi.openapi.models import Tag
from fastapi.responses import JSONResponse, FileResponse
from pydantic import UUID5

from schemas.files import FileUploadResponse
from services.ner_service import NERService
from services.resume_parser_service import ResumeParserService
from services.resume_service import ResumeService
from services.user_entity_service import UserEntityService
from services.vector_store_service import VectorStoreService
from settings import settings

router = APIRouter()


tag_files = Tag(
    name="files",
    description="Uploading files.",
)


@router.get("/resume", response_model=list[dict])
async def list_uploaded_resumes(resume_service: ResumeService = Depends()):
    return await resume_service.list_resumes()


@router.post(
    "/resume", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED
)
async def upload_resume(
    file: UploadFile = File(...), resume_service: ResumeService = Depends()
) -> JSONResponse:
    file_extension = Path(file.filename).suffix.lower().lstrip(".")
    if file_extension not in settings.resume.allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Only {', '.join(settings.resume.allowed_extensions)} allowed.",
        )

    file_content = await file.read()
    file_size_mb = len(file_content) / (1024 * 1024)

    if file_size_mb > settings.resume.max_file_size_mb:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File is too large. Maximum allowed size is {settings.resume.max_file_size_mb}MB.",
        )

    file_id, created = await resume_service.save_file(file_content, file_extension)
    if created:
        await resume_service.save_file_metadata(
            file_id, Path(file.filename).stem, file_extension
        )

    status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

    return JSONResponse(
        content=FileUploadResponse(file_id=file_id).model_dump(),
        status_code=status_code,
    )


@router.get("/resume/{file_id}")
async def get_resume(file_id: UUID5, resume_service: ResumeService = Depends()):
    if file_path := await resume_service.get_file_path(file_id):
        return FileResponse(file_path, filename=file_path.name)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")


@router.delete("/resume/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    file_id: UUID5,
    resume_service: ResumeService = Depends(),
) -> Response:
    await resume_service.delete_resume(file_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/resume/{file_id}/parse", response_model=dict)
async def parse_resume(
    file_id: UUID5,
    resume_service: ResumeService = Depends(),
    resume_parser_service: ResumeParserService = Depends(),
    ner_service: NERService = Depends(),
    vector_store_service: VectorStoreService = Depends(),
):
    file_path = await resume_service.get_file_path(file_id)
    if not file_path or not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found."
        )

    text = await resume_parser_service.parse_resume(file_path)
    facts = await resume_parser_service.extract_facts(text)

    await ner_service.store_facts(file_id, facts)

    await vector_store_service.refresh_document(
        text=text, metadata={"resume_id": str(file_id), "type": "resume_text"}
    )

    entities = await ner_service.extract_entities(
        file_id,
        facts,
        language="ru",
    )

    return {
        "entities": entities.entities,
    }


@router.get("/resume/{file_id}/entities", response_model=dict)
async def parse_resume(
    file_id: UUID5,
    resume_service: ResumeService = Depends(),
    ner_service: NERService = Depends(),
    resume_parser_service: ResumeParserService = Depends(),
    vector_store_service: VectorStoreService = Depends(),
    user_entity_service: UserEntityService = Depends(),
):
    if entities := await ner_service.get_entities(file_id):
        selections = await user_entity_service.get_user_selections(file_id)
        selected_map = {}
        for row in selections:
            selected_map.setdefault(row.entity_type, []).append(
                {
                    "text": row.entity,
                    "label": row.entity_type,
                }
            )

        return {"entities": entities, "selected": selected_map}

    file_path = await resume_service.get_file_path(file_id)
    if not file_path or not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found"
        )

    text = await resume_parser_service.parse_resume(file_path)
    facts = await resume_parser_service.extract_facts(text)

    await ner_service.store_facts(file_id, facts)
    await vector_store_service.refresh_document(
        text=text, metadata={"resume_id": str(file_id), "type": "resume_text"}
    )

    entities = await ner_service.extract_entities(file_id, facts, language="ru")

    return {"entities": entities.entities, "selected": {}}


@router.get("/resume/{file_id}/context", response_model=dict)
async def get_resume_context(
    file_id: UUID5,
    vector_store_service: VectorStoreService = Depends(),
):
    documents = await vector_store_service.get_documents(str(file_id))

    return {
        "chunks": [doc.page_content for doc in documents],
    }
