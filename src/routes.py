from fastapi import FastAPI

from transport.handlers import recommendation, files
from transport.handlers.files import tag_files
from transport.handlers.recommendation import tag_recommendations

metadata_tags = [tag_recommendations, tag_files]


def setup_routes(app: FastAPI) -> None:
    app.include_router(
        recommendation.router,
        prefix="/api/v1/recommendations",
        tags=[tag_recommendations.name],
    )
    app.include_router(files.router, prefix="/api/v1/files", tags=[tag_files])
