from fastapi import FastAPI

from exceptions import setup_exception_handlers
from middleware import setup_middleware
from routes import setup_routes
from settings import settings


def build_app() -> FastAPI:
    app_params = {
        "debug": settings.debug,
        # "openapi_tags": metadata_tags,
        "title": settings.project.title,
        "description": settings.project.description,
        "version": settings.project.release_version,
    }
    app = FastAPI(**app_params)

    setup_middleware(app)
    setup_routes(app)
    setup_exception_handlers(app)

    return app
