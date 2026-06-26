import logging
import re
import time
from typing import List, Tuple

from google import genai
from google.genai import types

from src.models import Document

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a document Q&A assistant. Answer ONLY using the provided context.

Rules:
1. If the context does not contain enough information to answer, respond exactly with:
   "I cannot find this in the uploaded documents."
2. Cite sources inline using the format: [Source: filename, Page N]
3. Do not invent facts, numbers, dates, or quotes that are not in the context.
4. Be concise but complete.
5. If multiple sources support the answer, cite each relevant source."""

REFUSAL_PHRASE = "I cannot find this in the uploaded documents."


class GeminiClient:
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.1,
        max_retries: int = 3,
    ):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file.")
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries

    def generate_answer(
        self,
        question: str,
        retrieved_docs: List[Tuple[Document, float]],
        chat_history: List[dict] | None = None,
    ) -> dict:
        context_block = self._format_context(retrieved_docs)
        user_prompt = self._build_user_prompt(question, context_block, chat_history)

        answer_text = self._call_with_retry(user_prompt)
        citations = self._extract_citations(answer_text, retrieved_docs)
        grounded = REFUSAL_PHRASE not in answer_text

        return {
            "answer": answer_text.strip(),
            "citations": citations,
            "grounded": grounded,
        }

    def _format_context(self, retrieved_docs: List[Tuple[Document, float]]) -> str:
        if not retrieved_docs:
            return "No relevant context was retrieved."

        blocks: list[str] = []
        for i, (doc, score) in enumerate(retrieved_docs, start=1):
            blocks.append(
                f"[Context {i} | {doc.source} | Page {doc.page} | "
                f"Type: {doc.source_type} | score={score:.3f}]\n"
                f"{doc.text}"
            )
        return "\n\n".join(blocks)

    def _build_user_prompt(
        self,
        question: str,
        context_block: str,
        chat_history: List[dict] | None,
    ) -> str:
        history_text = ""
        if chat_history:
            recent = chat_history[-6:]
            lines = [f"{m['role'].upper()}: {m['content']}" for m in recent]
            history_text = "Previous conversation:\n" + "\n".join(lines) + "\n\n"

        return (
            f"{history_text}"
            f"Context:\n{context_block}\n\n"
            f"Question: {question}\n\n"
            "Answer using only the context above. Include inline citations."
        )

    def _call_with_retry(self, user_prompt: str) -> str:
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=self.temperature,
                    ),
                )
                if response.text:
                    return response.text
                return REFUSAL_PHRASE
            except Exception as exc:
                last_error = exc
                wait = 2 ** attempt
                logger.warning(
                    "Gemini API call failed (attempt %d/%d): %s",
                    attempt + 1, self.max_retries, exc,
                )
                if attempt < self.max_retries - 1:
                    time.sleep(wait)

        logger.error("Gemini API call failed permanently: %s", last_error)
        raise RuntimeError(
            "The AI service is temporarily unavailable. Please try again later."
        )

    def _extract_citations(
        self,
        answer: str,
        retrieved_docs: List[Tuple[Document, float]],
    ) -> list[dict]:
        pattern = r"\[Source:\s*([^,\]]+),\s*Page\s*(\d+)\]"
        matches = re.findall(pattern, answer, flags=re.IGNORECASE)

        citations: list[dict] = []
        seen: set[tuple[str, int]] = set()

        for source, page_str in matches:
            source = source.strip()
            page = int(page_str)
            key = (source, page)
            if key in seen:
                continue
            seen.add(key)

            excerpt = self._find_excerpt(source, page, retrieved_docs)
            citations.append({
                "source": source,
                "page": page,
                "excerpt": excerpt,
            })

        if not citations and retrieved_docs:
            for doc, score in retrieved_docs[:3]:
                key = (doc.source, doc.page)
                if key in seen:
                    continue
                seen.add(key)
                citations.append({
                    "source": doc.source,
                    "page": doc.page,
                    "excerpt": doc.text[:300],
                    "score": score,
                })

        return citations

    def _find_excerpt(
        self,
        source: str,
        page: int,
        retrieved_docs: List[Tuple[Document, float]],
    ) -> str:
        for doc, _ in retrieved_docs:
            if doc.source == source and doc.page == page:
                return doc.text[:300]
        return ""
