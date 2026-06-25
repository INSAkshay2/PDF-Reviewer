import { Database, FileText, GitMerge, Layers, Search, Cpu, Brain, BookOpen, Upload, Tags } from "lucide-react";
import type { ReactNode } from "react";

export interface StepData {
  number: string;
  title: string;
  description: string;
  whyMatters: string;
  technologies: string[];
  icon: ReactNode;
  gradient: string;
}

export const pipelineSteps: StepData[] = [
  {
    number: "01",
    title: "Data Ingestion",
    description:
      "The system accepts documents from three source types: PDF files, CSV files, and website URLs. Each source type has a dedicated loader that handles its specific format.",
    whyMatters:
      "Multi-source ingestion means you can build a knowledge base from diverse inputs — technical PDFs, structured spreadsheets, and live web content — all in one place.",
    technologies: ["PyMuPDF", "BeautifulSoup", "CSV"],
    icon: <Upload className="w-5 h-5 text-primary" />,
    gradient: "from-blue-500/5 to-transparent",
  },
  {
    number: "02",
    title: "Parsing & Normalization",
    description:
      "Raw source content is extracted and normalized into a unified internal Document model. A text cleaner strips excessive whitespace, normalizes unicode, and removes artifacts before further processing.",
    whyMatters:
      "Without normalization, PDFs, CSVs, and web pages would each require different handling downstream. A common document format means the rest of the pipeline is source-agnostic.",
    technologies: ["Text Cleaner", "Document Model", "Pydantic"],
    icon: <FileText className="w-5 h-5 text-primary" />,
    gradient: "from-emerald-500/5 to-transparent",
  },
  {
    number: "03",
    title: "Chunking",
    description:
      "Large documents are split into smaller, overlapping chunks using a recursive separator strategy. The chunker tries to break at paragraph boundaries (double newline), then sentence boundaries (period + space), then word boundaries (space), with a configurable chunk size of 800 characters and 150-character overlap.",
    whyMatters:
      "Retrieval works best on focused text segments. Chunking ensures long documents don't bury relevant details, while overlap prevents information loss at boundaries.",
    technologies: ["Recursive Splitter", "Configurable Size", "Overlap"],
    icon: <GitMerge className="w-5 h-5 text-primary" />,
    gradient: "from-violet-500/5 to-transparent",
  },
  {
    number: "04",
    title: "Metadata Tagging",
    description:
      "Each chunk is tagged with its source filename, source type (pdf / csv / website), page number (for PDFs), and chunk index. This metadata follows every chunk through the pipeline and is used during citation generation.",
    whyMatters:
      "Metadata turns raw chunks into traceable evidence. When the system cites a source, it can point to the exact file, page, and chunk, making answers verifiable.",
    technologies: ["Source Tracking", "Page Numbers", "Chunk Index"],
    icon: <Tags className="w-5 h-5 text-primary" />,
    gradient: "from-amber-500/5 to-transparent",
  },
  {
    number: "05",
    title: "Embedding Generation",
    description:
      "Each text chunk is converted into a vector embedding using the BAAI/bge-small-en-v1.5 model from sentence-transformers. The embedder applies a query prefix ('Represent this sentence for searching relevant passages: ') to differentiate document embeddings from query embeddings during search.",
    whyMatters:
      "Embeddings capture semantic meaning, enabling the system to find relevant content even when the query uses different words than the source document.",
    technologies: ["BGE Embeddings", "Sentence Transformers", "Query Prefix"],
    icon: <Layers className="w-5 h-5 text-primary" />,
    gradient: "from-cyan-500/5 to-transparent",
  },
  {
    number: "06",
    title: "FAISS Indexing",
    description:
      "The embeddings are added to a FAISS IndexFlatIP index with IDMap for efficient inner-product similarity search. The index and associated document metadata are serialized to disk after every write operation, ensuring persistence across restarts.",
    whyMatters:
      "FAISS enables sub-millisecond retrieval over thousands of chunks on CPU. Disk persistence means the knowledge base survives server restarts without re-indexing.",
    technologies: ["FAISS", "IndexFlatIP", "Disk Persistence"],
    icon: <Database className="w-5 h-5 text-primary" />,
    gradient: "from-rose-500/5 to-transparent",
  },
  {
    number: "07",
    title: "Query Processing",
    description:
      "When a user submits a question, the system embeds the query using the same BGE model (with the retrieval prefix), then performs a similarity search against the FAISS index. The top-k most semantically similar chunks are retrieved along with their similarity scores.",
    whyMatters:
      "Semantic retrieval finds conceptually related content, not just keyword matches. A question about 'Q4 revenue growth' will find chunks discussing financial results even if the exact phrase isn't used.",
    technologies: ["Semantic Search", "Top-k Retrieval", "Score Ranking"],
    icon: <Search className="w-5 h-5 text-primary" />,
    gradient: "from-orange-500/5 to-transparent",
  },
  {
    number: "08",
    title: "Context Assembly",
    description:
      "The retrieved chunks are formatted into a structured prompt that includes source metadata (file name, page number, score) alongside the chunk text. If the conversation has history, the last 6 messages are included to maintain conversational context.",
    whyMatters:
      "Proper context assembly ensures the LLM receives relevant information in a structured format, with clear attribution so it can cite sources correctly in its response.",
    technologies: ["Prompt Assembly", "Chat History", "Source Tags"],
    icon: <Cpu className="w-5 h-5 text-primary" />,
    gradient: "from-pink-500/5 to-transparent",
  },
  {
    number: "09",
    title: "Gemini Answer Generation",
    description:
      "The assembled prompt is sent to Google's Gemini 2.5 Flash model with a system instruction that requires the model to answer only from the provided context. If the context lacks sufficient information, the model responds with 'I cannot find this in the uploaded documents.' The API call includes automatic retries with exponential backoff.",
    whyMatters:
      "Grounding the LLM in retrieved context prevents hallucination. The model cannot inject external knowledge — every answer must be supported by an uploaded document. This is the core of RAG reliability.",
    technologies: ["Gemini API", "Grounded Generation", "Retry Logic"],
    icon: <Brain className="w-5 h-5 text-primary" />,
    gradient: "from-purple-500/5 to-transparent",
  },
  {
    number: "10",
    title: "Source Citations",
    description:
      "After generation, the system parses the answer text for inline source references using the format '[Source: filename, Page N]'. Each citation is enriched with the excerpt text and similarity score. If no inline citations are detected, the top 3 retrieved documents are shown as fallback sources.",
    whyMatters:
      "Citations make answers verifiable. Instead of trusting a black-box LLM, users can inspect the exact source material behind each claim, building trust in the system's responses.",
    technologies: ["Regex Parsing", "Citation Extraction", "Fallback Logic"],
    icon: <BookOpen className="w-5 h-5 text-primary" />,
    gradient: "from-indigo-500/5 to-transparent",
  },
];

export const pipelineOverview = [
  { label: "Ingest", icon: "Upload" },
  { label: "Process", icon: "FileText" },
  { label: "Chunk", icon: "GitMerge" },
  { label: "Embed", icon: "Layers" },
  { label: "Index", icon: "Database" },
  { label: "Retrieve", icon: "Search" },
  { label: "Generate", icon: "Brain" },
  { label: "Cite", icon: "BookOpen" },
];
