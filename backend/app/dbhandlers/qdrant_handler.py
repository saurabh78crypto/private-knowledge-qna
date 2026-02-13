from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from app.config import settings
from app.constants import VECTOR_SIZE

class QdrantHandler:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection = settings.COLLECTION_NAME
        self._ensure_collection()

    def _ensure_collection(self):
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
            self.client.create_payload_index(self.collection, field_name="document_id", field_schema="keyword")
            self.client.create_payload_index(self.collection, field_name="document_name", field_schema="keyword")
            self.client.create_payload_index(self.collection, field_name="guest_id", field_schema="keyword")

    def _create_guest_filter(self, guest_id: str) -> Filter:
        """Create a Qdrant Filter for a specific guest ID."""
        return Filter(
            must=[
                FieldCondition(
                    key="guest_id",
                    match=MatchValue(value=guest_id)
                )
            ]
        )

    def upsert_chunks(self, chunks: list[dict]):
        points = [
            PointStruct(
                id=chunk["chunk_id"],
                vector=chunk["embedding"],
                payload={
                    "document_id": chunk["document_id"],
                    "document_name": chunk["document_name"],
                    "chunk_index": chunk["chunk_index"],
                    "text": chunk["text"],
                    "upload_timestamp": chunk["upload_timestamp"],
                    "guest_id": chunk["guest_id"]
                }
            )
            for chunk in chunks
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query_vector: list[float], guest_id: str, limit: int = 10):
        guest_filter = self._create_guest_filter(guest_id)

        return self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            query_filter=guest_filter,
            limit=limit,
            with_payload=True
        )

    def get_unique_documents(self, guest_id: str):
        guest_filter = self._create_guest_filter(guest_id)

        points, _ = self.client.scroll(
            collection_name=self.collection,
            scroll_filter=guest_filter,
            limit=10000,
            with_payload=True
        )
        docs = {}
        for point in points:
            payload = point.payload
            doc_id = payload["document_id"]
            if doc_id not in docs:
                docs[doc_id] = {
                    "document_id": doc_id,
                    "document_name": payload["document_name"],
                    "upload_timestamp": payload.get("upload_timestamp")
                }
        return list(docs.values())