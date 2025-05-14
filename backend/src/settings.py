from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings


class Project(BaseModel):
    title: str = "Text Generation Assistant"
    description: str = (
        "Context-Aware Writing Assistant: Leveraging LLM and RAG for Enhanced Text Generation"
    )
    release_version: str = Field(default="0.1.0")


class Resume(BaseModel):
    upload_dir: str = "uploads/resumes"
    allowed_extensions: set[str] = {"pdf", "docx", "txt"}
    max_file_size_mb: int = 2
    file_uuid_namespace: str = "f495f8a0-fa6b-44b6-987d-c7277ad67973"


class Settings(BaseSettings):
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    project: Project = Project()
    base_url: str = Field(default="http://0.0.0.0:8010")
    database_url: str = Field(
        default="postgresql+asyncpg://text_generation_assistant_user:secret@db/text_generation_assistant"
    )
    resume: Resume = Resume()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


settings = Settings()
