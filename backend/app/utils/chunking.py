import re
import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.constants import EMBEDDING_MODEL, MAX_ALLOWED

class ChunkingService:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.tokenizer = self.model.tokenizer
        self.chunk_size = settings.CHUNK_SIZE
        self.overlap = settings.CHUNK_OVERLAP

    def _token_count(self, text: str) -> int:
        """Calculates the number of tokens in a text string."""
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def _preprocess(self, text: str) -> str:
        """Normalizes line breaks and whitespace."""
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def _split_sentences(self, text: str) -> list[str]:
        """Splits text into sentences using regex lookbehind."""
        return re.split(r'(?<=[.!?])\s+', text)

    def _add_contextual_prefix(self, content: str, document_name: str) -> str:
        """Formats the text with the document name."""
        return f"Document: {document_name}\n\n{content}"

    def _create_chunk_entry(
        self,
        content: str,
        document_name: str,
        doc_id: str,
        index: int,
        guest_id: str
    ) -> dict:
        """Format the chunk metadata dictionary."""
        return {
            "chunk_id": str(uuid.uuid4()),
            "document_id": doc_id,
            "document_name": document_name,
            "chunk_index": index,
            "text": content,
            "upload_timestamp": datetime.utcnow().isoformat(),
            "guest_id": guest_id
        }

    def _generate_processing_units(self, text: str) -> list[str]:
        """
        Break text down into the smallest possible units 
        (paragraphs, sentences, or sub-token strings).
        """
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        units = []

        for para in paragraphs:
            if self._token_count(para) <= MAX_ALLOWED:
                units.append(para)
                continue

            sentences = self._split_sentences(para)
            for sentence in sentences:
                if self._token_count(sentence) <= MAX_ALLOWED:
                    units.append(sentence)
                else:
                    tokens = self.tokenizer.encode(sentence, add_special_tokens=False)
                    for i in range(0, len(tokens), MAX_ALLOWED):
                        sub_tokens = tokens[i : i + MAX_ALLOWED]
                        units.append(self.tokenizer.decode(sub_tokens))
        return units

    def _aggregate_units_into_chunks(
        self,
        units: list[str],
        document_name: str,
        doc_id: str,
        guest_id: str
    ):
        """
        Group atomic units into larger chunks, managing 
        token limits and sliding window overlap.
        """
        chunks_metadata = []
        chunk_texts_for_embedding = []
        
        current_buffer: list[str] = []
        current_tokens_count = 0
        chunk_index = 0

        for unit in units:
            unit_token_count = self._token_count(unit)

            # Check if adding this unit exceeds the chunk size
            if current_tokens_count + unit_token_count > self.chunk_size and current_buffer:
                # Finalize the current chunk
                chunk_content = "\n\n".join(current_buffer)
                prefixed_content = self._add_contextual_prefix(chunk_content, document_name)
                
                chunk_texts_for_embedding.append(prefixed_content)
                chunks_metadata.append(
                    self._create_chunk_entry(chunk_content, document_name, doc_id, chunk_index, guest_id)
                )
                chunk_index += 1

                # Calculate Overlap for the next chunk
                overlap_buffer: list[str] = []
                overlap_tokens_count = 0
                
                for prev_unit in reversed(current_buffer):
                    prev_unit_tokens = self._token_count(prev_unit)
                    if overlap_tokens_count + prev_unit_tokens > self.overlap:
                        break
                    overlap_buffer.insert(0, prev_unit)
                    overlap_tokens_count += prev_unit_tokens

                # Reset buffer
                current_buffer = overlap_buffer
                current_tokens_count = overlap_tokens_count

            current_buffer.append(unit)
            current_tokens_count += unit_token_count

        # Handle the final buffer
        if current_buffer:
            chunk_content = "\n\n".join(current_buffer)
            prefixed_content = self._add_contextual_prefix(chunk_content, document_name)

            chunk_texts_for_embedding.append(prefixed_content)
            chunks_metadata.append(
                self._create_chunk_entry(chunk_content, document_name, doc_id, chunk_index, guest_id)
            )

        return chunks_metadata, chunk_texts_for_embedding

    def _attach_embeddings(self, chunks_metadata: list[dict], chunk_texts: list[str]) -> list[dict]:
        """Generate vector embeddings for text and attach them to metadata."""
        if not chunk_texts:
            return chunks_metadata

        embeddings = self.model.encode(
            chunk_texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        for i, embedding in enumerate(embeddings):
            chunks_metadata[i]["embedding"] = embedding.tolist()
            
        return chunks_metadata

    def create_chunks(self, raw_text: str, document_name: str, guest_id: str) -> list[dict]:
        """Coordinates the pipeline of cleaning, splitting, grouping, and embedding."""
        text = self._preprocess(raw_text)
        processing_units = self._generate_processing_units(text)
        doc_id = str(uuid.uuid4())

        chunks_metadata, texts_for_embedding = self._aggregate_units_into_chunks(
            processing_units, document_name, doc_id, guest_id
        )

        final_chunks = self._attach_embeddings(chunks_metadata, texts_for_embedding)

        return final_chunks