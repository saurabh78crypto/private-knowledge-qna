from typing import List, Dict, Any, Tuple
import json
from fastapi import HTTPException
from google import genai
from qdrant_client.models import ScoredPoint

from app.config import settings
from app.utils.chunking import ChunkingService
from app.dbhandlers.qdrant_handler import QdrantHandler
from app.constants import LLM_MODEL

client = genai.Client(api_key=settings.GEMINI_API_KEY)

class QAService:
    def __init__(self, qdrant: QdrantHandler):
        self.qdrant = qdrant
        self.chunking = ChunkingService()

    async def ask(self, question: str, guest_id: str) -> Dict[str, Any]:
        merged_results = self._search_knowledge_base(question, guest_id)

        if not merged_results:
            return {
                "answer": "I don't have enough relevant information to answer this question.",
                "sources": []
            }

        answer, excerpt = self._generate_llm_response(question, merged_results)

        sources = self._build_sources(merged_results, excerpt)

        return {"answer": answer, "sources": sources}

    def _search_knowledge_base(self, question: str, guest_id: str) -> List[ScoredPoint]:
        clean_q = question.strip()
        query_text = f"Represent this sentence for searching relevant passages: {clean_q}"
        query_vec = self.chunking.model.encode(query_text, normalize_embeddings=True).tolist()

        results = self.qdrant.search(query_vec, guest_id=guest_id, limit=settings.TOP_K)
        filtered = [r for r in results if r.score > settings.SCORE_THRESHOLD]
        return self._merge_consecutive(filtered)

    def _parse_llm_response(self, raw_text: str) -> Tuple[str, str]:
        """Safely parse JSON output."""
        try:
            data = json.loads(raw_text.strip())
            answer = data.get("answer", raw_text).strip()
            excerpt = data.get("excerpt", "").strip()
            return answer, excerpt
        except Exception:
            return raw_text.strip(), ""

    def _generate_llm_response(self, question: str, context_results: List[ScoredPoint]) -> Tuple[str, str]:
        """Builds prompt, calls Gemini, and returns (answer, excerpt)."""
        
        context_str = "\n\n---\n\n".join([
            f"Source: {r.payload['document_name']}\n{r.payload['text']}"
            for r in context_results
        ])

        prompt = f"""
        You are a precise assistant. Answer the question using ONLY the provided context.

        Context:
        {context_str}

        Question: {question}

        Return **ONLY** valid JSON. No markdown, no code blocks, no extra text.

        {{
          "answer": "your final answer here",
          "excerpt": "the exact 2-4 sentences from the context that best support the answer"
        }}

        Rules:
        - The excerpt must be copied exactly from the context (do not rephrase).
        - excerpt must be 2 to 4 sentences long (not just one sentence)
        - if no relevant information, set answer to "I'm unable to provide an answer from the given sources."
        """

        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
        )

        raw_text = response.text.strip()
        return self._parse_llm_response(raw_text)

    def _build_sources(self, results: List[ScoredPoint], excerpt: str) -> List[Dict[str, str]]:
        """Build sources using the exact excerpt returned by LLM."""
        seen = set()
        formatted = []

        for r in results:
            doc_name = r.payload["document_name"]
            if doc_name in seen:
                continue
            seen.add(doc_name)

            formatted.append({
                "document_name": doc_name,
                "excerpt": excerpt or r.payload["text"][:500] + "..."
            })
        return formatted

    def _merge_consecutive(self, results: List[ScoredPoint]) -> List[ScoredPoint]:
        if not results:
            return []

        sorted_results = sorted(
            results,
            key=lambda x: (x.payload["document_id"], x.payload["chunk_index"])
        )

        merged = []
        current_chunk = sorted_results[0]
        current_text = current_chunk.payload["text"]

        for next_chunk in sorted_results[1:]:
            is_same_doc = next_chunk.payload["document_id"] == current_chunk.payload["document_id"]
            is_next_index = next_chunk.payload["chunk_index"] == current_chunk.payload["chunk_index"] + 1

            if is_same_doc and is_next_index:
                current_text += "\n\n" + next_chunk.payload["text"]
                current_chunk.payload["text"] = current_text
            else:
                merged.append(current_chunk)
                current_chunk = next_chunk
                current_text = current_chunk.payload["text"]

        merged.append(current_chunk)
        return merged