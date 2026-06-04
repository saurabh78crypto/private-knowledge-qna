from fastapi import APIRouter, UploadFile, File, Request, Query, HTTPException

from app.utils.validation import validate_guest_id, validate_files

document_router = APIRouter(prefix="/documents", tags=["documents"])

@document_router.post("/upload")
async def upload(
    request: Request,
    guest_id: str = Query(..., description="The unique guest ID"),
    files: list[UploadFile] = File(...)
):
    validate_guest_id(guest_id)
    validate_files(files)

    app = request.app
    return await app.document_service.upload_documents(files, guest_id)

@document_router.get("")
def list_docs(
    request: Request,
    guest_id: str = Query(..., description="The unique guest ID")
):
    validate_guest_id(guest_id)

    app = request.app
    return app.document_service.list_documents(guest_id)

@document_router.delete("/{document_id}")
def delete_document(
    document_id: str,
    request: Request,
    guest_id: str = Query(..., description="The unique guest ID"),
):
    """Delete a document and all its associated chunks.

    Only the document owner (matched by guest_id) can delete their documents.
    Returns 404 if the document is not found for this guest.
    """
    validate_guest_id(guest_id)

    app = request.app
    return app.document_service.delete_document(document_id, guest_id)