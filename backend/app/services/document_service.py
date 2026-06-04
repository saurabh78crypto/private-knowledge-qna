from fastapi import HTTPException, UploadFile

from app.utils.chunking import ChunkingService
from app.dbhandlers.qdrant_handler import QdrantHandler

class DocumentService:
    def __init__(self, qdrant: QdrantHandler):
        self.qdrant = qdrant
        self.chunking = ChunkingService()

    async def upload_documents(self, files: list[UploadFile], guest_id: str):
        for file in files:
            if not file.filename.endswith(".txt"):
                raise HTTPException(400, f"Only .txt files allowed: {file.filename}")

            content = await file.read()
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                raise HTTPException(400, f"Invalid text file: {file.filename}")

            chunks = self.chunking.create_chunks(text, file.filename, guest_id)
            self.qdrant.upsert_chunks(chunks)

        return {"message": f"Successfully uploaded {len(files)} document(s)"}

    def list_documents(self, guest_id: str):
        return self.qdrant.get_unique_documents(guest_id)

    def delete_document(self, document_id: str, guest_id: str) -> dict:
        """Delete a document and all its chunks from the vector store.

        Raises 404 if the document does not exist for this guest.
        """
        # Confirm the document exists for this guest before deleting
        existing = self.qdrant.get_unique_documents(guest_id)
        doc_ids = [d["document_id"] for d in existing]

        if document_id not in doc_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Document '{document_id}' not found for this guest."
            )

        deleted_count = self.qdrant.delete_document(document_id, guest_id)
        return {
            "message": "Document deleted successfully.",
            "document_id": document_id,
            "chunks_removed": deleted_count,
        }