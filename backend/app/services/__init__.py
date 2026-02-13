from app.services.document_service import DocumentService
from app.services.qa_service import QAService

def init_services(app):
    app.document_service = DocumentService(app.qdrant_handler)
    app.qa_service = QAService(app.qdrant_handler)