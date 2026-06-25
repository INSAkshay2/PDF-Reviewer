import { Upload, Database, Search, Brain, BookOpen, HardDrive, MessageSquare, Tags, Puzzle, BarChart3 } from "lucide-react";
import type { ReactNode } from "react";

export interface FeatureData {
  title: string;
  description: string;
  details: string[];
  icon: ReactNode;
  status: "implemented" | "planned";
}

export const implementedFeatures: FeatureData[] = [
  {
    title: "Multi-Source Knowledge Ingestion",
    description:
      "Upload PDFs, CSV files, or provide website URLs. Each source type is handled by a dedicated loader that extracts text content while preserving structural metadata.",
    details: [
      "PDF ingestion via PyMuPDF with per-page text extraction",
      "CSV ingestion with structured row-by-row parsing",
      "Website ingestion via HTTP requests with BeautifulSoup HTML parsing",
      "Configurable timeout and error handling per source type",
    ],
    icon: <Upload className="w-5 h-5 text-primary" />,
    status: "implemented",
  },
  {
    title: "Unified Knowledge Base",
    description:
      "All ingested content — regardless of source type — is stored in a single searchable FAISS vector index. A single query can search across PDFs, CSVs, and websites simultaneously.",
    details: [
      "Common document model normalizes all source types into one format",
      "Single FAISS index enables cross-source retrieval in one query",
      "Source type metadata preserved so results indicate origin format",
      "Deduplication and source-level aggregation in stats",
    ],
    icon: <Database className="w-5 h-5 text-primary" />,
    status: "implemented",
  },
  {
    title: "Semantic Search",
    description:
      "Retrieval is based on meaning rather than keyword matching. The BGE embedding model converts text into dense vectors, and FAISS performs fast inner-product similarity search to find the most semantically relevant chunks.",
    details: [
      "BAAI/bge-small-en-v1.5 embeddings with 384-dimensional vectors",
      "Query-side prefix improves retrieval relevance for question-style queries",
      "Configurable top-k (default 5) for controlling context breadth",
      "Similarity scores returned so users can assess relevance confidence",
    ],
    icon: <Search className="w-5 h-5 text-primary" />,
    status: "implemented",
  },
  {
    title: "Gemini-Powered Answers",
    description:
      "Google's Gemini 2.5 Flash model generates answers grounded in the retrieved context. A strict system prompt prevents the model from using external knowledge, ensuring every response is supported by uploaded content.",
    details: [
      "Gemini 2.5 Flash for fast, high-quality generation",
      "System-enforced grounding: model must answer only from context",
      "Refusal mechanism when context lacks sufficient information",
      "Automatic retries with exponential backoff for API resilience",
      "Configurable temperature (default 0.1) for consistent responses",
    ],
    icon: <Brain className="w-5 h-5 text-primary" />,
    status: "implemented",
  },
  {
    title: "Source Citations",
    description:
      "Every answer includes inline source references in the format [Source: filename, Page N]. The citation system automatically parses the generated answer and enriches citations with excerpt previews and relevance scores.",
    details: [
      "Inline citation format: [Source: filename, Page N]",
      "Automated regex-based citation extraction from answer text",
      "Excerpt preview (first 300 chars) shown with each citation",
      "Fallback to top-3 retrieved sources when no inline citations detected",
    ],
    icon: <BookOpen className="w-5 h-5 text-primary" />,
    status: "implemented",
  },
  {
    title: "Persistent Knowledge Storage",
    description:
      "The FAISS index and document metadata are serialized to disk after every write operation. On restart, the system reloads the existing index, preserving all previously uploaded content without requiring re-indexing.",
    details: [
      "Index saved to data/indices/knowledge_base.index (FAISS binary)",
      "Document metadata serialized as pickle alongside index",
      "Automatic load on startup — zero rebuild time",
      "Clear operation resets both index and persisted files",
    ],
    icon: <HardDrive className="w-5 h-5 text-primary" />,
    status: "implemented",
  },
  {
    title: "Chat-Based Interface",
    description:
      "Users interact with the knowledge base through a conversational chat interface. The system maintains session-level chat history so follow-up questions are understood in context.",
    details: [
      "Streaming-capable chat UI with message history",
      "Last 6 messages included as conversational context per query",
      "User and assistant messages clearly distinguished with role icons",
      "Sources panel shows citations inline below each assistant response",
    ],
    icon: <MessageSquare className="w-5 h-5 text-primary" />,
    status: "implemented",
  },
  {
    title: "Metadata-Aware Retrieval",
    description:
      "Retrieved chunks carry their source metadata — filename, source type, page number, and chunk index — through the entire pipeline. This metadata is used during context assembly and citation generation.",
    details: [
      "Each chunk tagged with: source name, type, page, and chunk index",
      "Source type preserved: pdf / csv / website",
      "Page-level granularity for PDF documents",
      "Metadata visible in citation cards and source summary display",
    ],
    icon: <Tags className="w-5 h-5 text-primary" />,
    status: "implemented",
  },
];

export const plannedFeatures: FeatureData[] = [
  {
    title: "Result Re-Ranking",
    description:
      "Add a cross-encoder re-ranker stage after initial retrieval to improve the relevance ordering of chunks before they reach the LLM.",
    details: [
      "Cross-encoder model for finer-grained relevance scoring",
      "Re-rank top-N retrieved chunks before context assembly",
      "Configurable number of candidates to re-rank",
    ],
    icon: <BarChart3 className="w-5 h-5 text-muted-foreground" />,
    status: "planned",
  },
  {
    title: "Hybrid Retrieval",
    description:
      "Combine dense semantic search with sparse keyword (BM25) retrieval to improve recall for exact-match queries like codes, IDs, or proper nouns.",
    details: [
      "BMI25 sparse index alongside FAISS dense index",
      "Weighted fusion of dense and sparse result sets",
      "Configurable hybrid weight parameter",
    ],
    icon: <Puzzle className="w-5 h-5 text-muted-foreground" />,
    status: "planned",
  },
];
