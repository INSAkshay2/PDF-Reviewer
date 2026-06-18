"""Streamlit UI for the Phase 1 PDF RAG assistant."""

import logging
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import get_settings
from src.models import ChatMessage
from src.pipeline.rag_pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="PDF Knowledge Assistant",
    page_icon="📄",
    layout="wide",
)


@st.cache_resource
def get_pipeline() -> RAGPipeline:
    return RAGPipeline()


def init_session_state() -> None:
    defaults = {
        "messages": [],
        "current_doc_id": None,
        "current_source_file": None,
        "ingest_info": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar(settings) -> None:
    st.sidebar.title("Document Upload")
    st.sidebar.markdown("Upload a PDF to index it for question answering.")

    uploaded_file = st.sidebar.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Text-based PDFs work best. Scanned/image PDFs are not supported in Phase 1.",
    )

    if uploaded_file is not None:
        if st.sidebar.button("Process Document", type="primary", use_container_width=True):
            with st.spinner("Processing PDF: extracting, chunking, embedding..."):
                try:
                    pipeline = get_pipeline()
                    saved_path = pipeline.save_uploaded_pdf(
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                    )
                    result = pipeline.ingest_pdf(saved_path)

                    st.session_state.current_doc_id = result.doc_id
                    st.session_state.current_source_file = result.source_file
                    st.session_state.ingest_info = result
                    st.session_state.messages = []
                    st.sidebar.success(
                        f"Indexed **{result.source_file}**: "
                        f"{result.num_pages} pages → {result.num_chunks} chunks"
                    )
                except Exception as exc:
                    logger.exception("Ingestion failed")
                    st.sidebar.error(f"Failed to process PDF: {exc}")

    if st.session_state.ingest_info:
        info = st.session_state.ingest_info
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Active Document**")
        st.sidebar.write(f"File: `{info.source_file}`")
        st.sidebar.write(f"Pages: {info.num_pages}")
        st.sidebar.write(f"Chunks indexed: {info.num_chunks}")
        st.sidebar.caption(f"Index ID: `{info.doc_id}`")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Previously Indexed**")
    pipeline = get_pipeline()
    indexed = pipeline.list_indexed_documents()
    if indexed:
        selected = st.sidebar.selectbox(
            "Load existing index",
            options=["— Select —"] + indexed,
            index=0,
        )
        if selected != "— Select —" and st.sidebar.button("Load Index"):
            store = pipeline.get_store(selected)
            st.session_state.current_doc_id = selected
            st.session_state.current_source_file = selected.split("_")[0]
            st.session_state.ingest_info = None
            st.session_state.messages = []
            st.sidebar.info(f"Loaded index with {store.size} chunks.")
    else:
        st.sidebar.caption("No saved indices yet.")

    if st.session_state.messages:
        if st.sidebar.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()


def render_chat() -> None:
    st.title("Enterprise PDF Knowledge Assistant")
    st.caption("Phase 1: PDF → Chunking → Embeddings → FAISS → Gemini")

    if not get_settings().gemini_api_key:
        st.error(
            "GEMINI_API_KEY is not configured. Copy `.env.example` to `.env` "
            "and add your API key from Google AI Studio."
        )
        return

    if not st.session_state.current_doc_id:
        st.info("Upload and process a PDF in the sidebar to start asking questions.")
        return

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("sources"):
                with st.expander("Sources"):
                    for source in message["sources"]:
                        st.markdown(
                            f"**{source['source_file']} — Page {source['page_number']}** "
                            f"(score: {source['score']:.3f})"
                        )
                        st.caption(source["excerpt"])

    if prompt := st.chat_input("Ask a question about your document..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving context and generating answer..."):
                try:
                    pipeline = get_pipeline()
                    history = [
                        ChatMessage(role=m["role"], content=m["content"])
                        for m in st.session_state.messages[:-1]
                    ]
                    response = pipeline.query(
                        doc_id=st.session_state.current_doc_id,
                        question=prompt,
                        chat_history=history,
                    )

                    st.markdown(response.answer)

                    sources = []
                    for result in response.retrieval_results:
                        sources.append(
                            {
                                "source_file": result.chunk.source_file,
                                "page_number": result.chunk.page_number,
                                "score": result.score,
                                "excerpt": result.chunk.text[:400],
                            }
                        )

                    if sources:
                        with st.expander("Sources"):
                            for source in sources:
                                st.markdown(
                                    f"**{source['source_file']} — Page {source['page_number']}** "
                                    f"(score: {source['score']:.3f})"
                                )
                                st.caption(source["excerpt"])

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response.answer,
                            "sources": sources,
                        }
                    )
                except Exception as exc:
                    logger.exception("Query failed")
                    error_msg = f"Sorry, something went wrong: {exc}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )


def main() -> None:
    init_session_state()
    settings = get_settings()
    render_sidebar(settings)
    render_chat()


if __name__ == "__main__":
    main()
