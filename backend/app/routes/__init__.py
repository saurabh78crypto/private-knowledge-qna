from fastapi import APIRouter

from app.routes.document import document_router
from app.routes.qa import qa_router

def init_routes(app):
    api_router = APIRouter()
    app.include_router(document_router)
    app.include_router(qa_router)
    app.include_router(api_router)