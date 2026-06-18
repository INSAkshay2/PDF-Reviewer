"""Gemini LLM client for grounded answer generation."""

import logging
import re
import time

from google import genai
from google.genai import types

from src.models import ChatMessage, Citation, RAGResponse, RetrievalResult

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
    """Generate grounded answers from retrieved context using Gemini."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.1,
        max_retries: int = 3,
    ):
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries

    def generate_answer(
        self,
        question: str,
        retrieval_results: list[RetrievalResult],
        chat_history: list[ChatMessage] | None = None,
    ) -> RAGResponse:
        """Generate a grounded answer with citations from retrieved chunks."""
        context_block = self._format_context(retrieval_results)
        user_prompt = self._build_user_prompt(question, context_block, chat_history)

        answer_text = self._call_with_retry(user_prompt)
        citations = self._extract_citations(answer_text, retrieval_results)
        grounded = REFUSAL_PHRASE not in answer_text

        return RAGResponse(
            answer=answer_text.strip(),
            citations=citations,
            retrieval_results=retrieval_results,
            grounded=grounded,
        )

    def _format_context(self, retrieval_results: list[RetrievalResult]) -> str:
        if not retrieval_results:
            return "No relevant context was retrieved."

        blocks: list[str] = []
        for index, result in enumerate(retrieval_results, start=1):
            chunk = result.chunk
            blocks.append(
                f"[Context {index} | {chunk.source_file} | Page {chunk.page_number} | score={result.score:.3f}]\n"
                f"{chunk.text}"
            )
        return "\n\n".join(blocks)

    def _build_user_prompt(
        self,
        question: str,
        context_block: str,
        chat_history: list[ChatMessage] | None,
    ) -> str:
        history_text = ""
        if chat_history:
            recent = chat_history[-6:]
            history_lines = [f"{msg.role.upper()}: {msg.content}" for msg in recent]
            history_text = "Previous conversation:\n" + "\n".join(history_lines) + "\n\n"

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
                wait_seconds = 2 ** attempt
                logger.warning(
                    "Gemini API call failed (attempt %d/%d): %s",
                    attempt + 1,
                    self.max_retries,
                    exc,
                )
                if attempt < self.max_retries - 1:
                    time.sleep(wait_seconds)

        raise RuntimeError(f"Gemini API failed after {self.max_retries} attempts: {last_error}")

    def _extract_citations(
        self,
        answer: str,
        retrieval_results: list[RetrievalResult],
    ) -> list[Citation]:
        pattern = r"\[Source:\s*([^,\]]+),\s*Page\s*(\d+)\]"
        matches = re.findall(pattern, answer, flags=re.IGNORECASE)

        citations: list[Citation] = []
        seen: set[tuple[str, int]] = set()

        for source_file, page_str in matches:
            source_file = source_file.strip()
            page_number = int(page_str)
            key = (source_file, page_number)
            if key in seen:
                continue
            seen.add(key)

            excerpt = self._find_excerpt(source_file, page_number, retrieval_results)
            citations.append(
                Citation(
                    source_file=source_file,
                    page_number=page_number,
                    excerpt=excerpt,
                )
            )

        if not citations and retrieval_results:
            for result in retrieval_results[:3]:
                chunk = result.chunk
                key = (chunk.source_file, chunk.page_number)
                if key in seen:
                    continue
                seen.add(key)
                citations.append(
                    Citation(
                        source_file=chunk.source_file,
                        page_number=chunk.page_number,
                        excerpt=chunk.text[:300],
                    )
                )

        return citations

    def _find_excerpt(
        self,
        source_file: str,
        page_number: int,
        retrieval_results: list[RetrievalResult],
    ) -> str:
        for result in retrieval_results:
            chunk = result.chunk
            if chunk.source_file == source_file and chunk.page_number == page_number:
                return chunk.text[:300]
        return ""
