import { Navigation } from "@/components/landing/navigation";
import { PipelineDiagram } from "@/components/rag/pipeline-diagram";
import { StepCard } from "@/components/rag/step-card";
import { pipelineSteps } from "@/components/rag/how-it-works-content";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Upload,
  FileText,
  GitMerge,
  Layers,
  Database,
  Search,
  Cpu,
  Brain,
  BookOpen,
  Tags,
  Info,
  ArrowRight,
} from "lucide-react";

const systemComponents = [
  { name: "Loaders", description: "Source-specific extractors for PDF (PyMuPDF), CSV (csv module), and websites (BeautifulSoup). Each outputs a list of Document objects.", icon: Upload },
  { name: "Chunker", description: "Recursive text splitter that divides documents at paragraph, sentence, and word boundaries with configurable size (800 chars) and overlap (150 chars).", icon: GitMerge },
  { name: "Embedder", description: "BGE embedding model (bge-small-en-v1.5) via sentence-transformers. Generates 384-dimensional vectors with query-side prefix for retrieval.", icon: Layers },
  { name: "Vector Store", description: "FAISS IndexFlatIP with IDMap wrapper. Supports inner-product similarity search, disk persistence via .index + .pkl files, and clear/rebuild operations.", icon: Database },
  { name: "Retriever", description: "Takes a query, embeds it, searches the FAISS index, and returns top-k Document tuples with similarity scores.", icon: Search },
  { name: "LLM Client", description: "Gemini 2.5 Flash API wrapper with system prompt enforcement, chat history injection, citation parsing, and automatic retry with exponential backoff.", icon: Brain },
  { name: "Citation Layer", description: "Regex-based parser that extracts inline source references from generated text, enriches them with excerpts, and provides fallback source display.", icon: BookOpen },
];

const techBadges = ["Gemini 2.5 Flash", "FAISS", "BGE Embeddings", "Multi-Source RAG", "Next.js", "FastAPI"];

export default function HowItWorksPage() {
  return (
    <main className="relative min-h-screen overflow-x-hidden">
      <Navigation />

      {/* Hero */}
      <section className="relative pt-36 pb-20 lg:pb-28 overflow-hidden bg-black">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent" />
          <div className="absolute inset-0 opacity-20">
            {[...Array(8)].map((_, i) => (
              <div key={`h-${i}`} className="absolute h-px bg-white/10" style={{ top: `${12.5 * (i + 1)}%`, left: 0, right: 0 }} />
            ))}
            {[...Array(12)].map((_, i) => (
              <div key={`v-${i}`} className="absolute w-px bg-white/10" style={{ left: `${8.33 * (i + 1)}%`, top: 0, bottom: 0 }} />
            ))}
          </div>
        </div>

        <div className="relative z-10 w-full max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="mb-6">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-white/40">
              <span className="w-8 h-px bg-white/30" />
              Architecture
            </span>
          </div>
          <h1 className="text-[clamp(2.5rem,6vw,6rem)] font-display leading-[0.92] tracking-tight text-white mb-6">
            <span className="block">How It Works</span>
          </h1>
          <p className="text-lg text-white/50 max-w-2xl leading-relaxed mb-8">
            A retrieval-augmented generation pipeline that ingests documents from multiple sources,
            indexes them for semantic search, and generates grounded answers using Google Gemini.
            Every response is supported by citations back to the source material.
          </p>
          <div className="flex flex-wrap gap-2">
            {techBadges.map((tech) => (
              <Badge key={tech} variant="secondary" className="font-mono text-[11px] bg-white/5 text-white/70 border-white/10">
                {tech}
              </Badge>
            ))}
          </div>
        </div>
      </section>

      {/* Pipeline Overview */}
      <section className="py-16 lg:py-20 border-t border-border">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="mb-10">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-4">
              <span className="w-12 h-px bg-foreground/30" />
              End-to-End Flow
            </span>
            <h2 className="text-3xl lg:text-4xl font-display tracking-tight">
              System Pipeline Overview
            </h2>
          </div>
          <div className="bg-secondary border border-border rounded-2xl p-6 lg:p-10">
            <PipelineDiagram />
            <p className="text-sm text-muted-foreground mt-6 leading-relaxed">
              From raw documents to cited answers — eight stages that transform uploaded files into
              verified responses. Each stage is a modular component in the pipeline.
            </p>
          </div>
        </div>
      </section>

      {/* Detailed Step Cards */}
      <section className="py-16 lg:py-20 border-t border-border">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="mb-12">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-4">
              <span className="w-12 h-px bg-foreground/30" />
              Deep Dive
            </span>
            <h2 className="text-3xl lg:text-4xl font-display tracking-tight">
              Pipeline Steps in Detail
            </h2>
            <p className="text-muted-foreground mt-3 max-w-2xl leading-relaxed">
              Each step in the pipeline has a specific responsibility. Together they form a
              production-grade RAG system that is modular, testable, and extensible.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-5">
            {pipelineSteps.map((step) => (
              <StepCard key={step.number} {...step} />
            ))}
          </div>
        </div>
      </section>

      {/* Example Query Journey */}
      <section className="py-16 lg:py-20 border-t border-border">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="mb-12">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-4">
              <span className="w-12 h-px bg-foreground/30" />
              Walkthrough
            </span>
            <h2 className="text-3xl lg:text-4xl font-display tracking-tight">
              Example Query Journey
            </h2>
          </div>

          <div className="bg-secondary border border-border rounded-2xl overflow-hidden">
            <div className="grid lg:grid-cols-5">
              <div className="lg:col-span-2 p-6 lg:p-8 bg-background/50 border-b lg:border-b-0 lg:border-r border-border">
                <div className="space-y-6">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center">
                        <Upload className="w-3 h-3 text-primary" />
                      </div>
                      <span className="text-sm font-mono text-muted-foreground">Step 1</span>
                    </div>
                    <p className="text-sm font-medium">User uploads <span className="font-mono text-primary">Annual_Report.pdf</span></p>
                    <p className="text-xs text-muted-foreground mt-1">PDF is parsed, chunked, embedded, and indexed into FAISS.</p>
                  </div>

                  <div className="flex items-center gap-2">
                    <div className="w-px h-6 bg-border ml-3" />
                  </div>

                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center">
                        <MessageSquare className="w-3 h-3 text-primary" />
                      </div>
                      <span className="text-sm font-mono text-muted-foreground">Step 2</span>
                    </div>
                    <p className="text-sm font-medium">User asks: <span className="italic text-muted-foreground">&ldquo;What was the Q4 revenue growth?&rdquo;</span></p>
                    <p className="text-xs text-muted-foreground mt-1">Query is embedded and matched against the FAISS index.</p>
                  </div>

                  <div className="flex items-center gap-2">
                    <div className="w-px h-6 bg-border ml-3" />
                  </div>

                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center">
                        <Search className="w-3 h-3 text-primary" />
                      </div>
                      <span className="text-sm font-mono text-muted-foreground">Step 3</span>
                    </div>
                    <p className="text-sm font-medium">Retriever finds top 5 relevant chunks</p>
                    <p className="text-xs text-muted-foreground mt-1">Chunks from the Financial Results section score highest (0.89–0.92).</p>
                  </div>

                  <div className="flex items-center gap-2">
                    <div className="w-px h-6 bg-border ml-3" />
                  </div>

                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center">
                        <Brain className="w-3 h-3 text-primary" />
                      </div>
                      <span className="text-sm font-mono text-muted-foreground">Step 4</span>
                    </div>
                    <p className="text-sm font-medium">Gemini generates answer with citations</p>
                    <p className="text-xs text-muted-foreground mt-1">Answer cites [Source: Annual_Report.pdf, Page 12] inline.</p>
                  </div>
                </div>
              </div>

              <div className="lg:col-span-3 p-6 lg:p-8">
                <div className="space-y-4">
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                      <span className="text-xs font-bold text-primary-foreground">U</span>
                    </div>
                    <div className="bg-primary/10 text-sm rounded-2xl rounded-bl-sm px-4 py-2.5 max-w-[80%]">
                      What was the Q4 revenue growth?
                    </div>
                  </div>

                  <div className="flex items-start gap-2">
                    <div className="w-8 h-8 rounded-full bg-secondary border border-border flex items-center justify-center shrink-0 mt-1">
                      <Brain className="w-4 h-4 text-primary" />
                    </div>
                    <div className="bg-secondary border border-border text-sm rounded-2xl rounded-bl-sm px-4 py-3 max-w-[85%] space-y-2">
                      <p>
                        Based on the financial statements in your uploaded document, the company achieved a
                        Q4 revenue growth of <strong>12.4%</strong> year-over-year, reaching $2.8 billion in
                        quarterly revenue. [Source: Annual_Report.pdf, Page 12]
                      </p>
                      <Separator className="my-2" />
                      <div className="text-xs text-muted-foreground">
                        <p className="font-medium text-foreground/80 mb-1">Source</p>
                        <p><span className="text-primary">Annual_Report.pdf</span> — Page 12, score: 0.892</p>
                        <p className="mt-1 text-muted-foreground/70 leading-relaxed">
                          &ldquo;Q4 revenue grew 12.4% year-over-year to $2.8 billion, driven by strong performance
                          in the enterprise segment with particular strength in cloud services...&rdquo;
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why RAG Section */}
      <section className="py-16 lg:py-20 border-t border-border">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="grid lg:grid-cols-2 gap-12 items-start">
            <div>
              <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-4">
                <span className="w-12 h-px bg-foreground/30" />
                Why RAG?
              </span>
              <h2 className="text-3xl lg:text-4xl font-display tracking-tight mb-6">
                Why RAG Instead of Plain Chat?
              </h2>
              <div className="space-y-4">
                <p className="text-muted-foreground leading-relaxed">
                  A standard LLM chat relies entirely on the model&apos;s pre-trained knowledge, which is
                  static, potentially outdated, and can produce confident-sounding but incorrect answers.
                </p>
                <p className="text-muted-foreground leading-relaxed">
                  RAG grounds every response in your actual documents. The model cannot invent facts —
                  it must extract information from the retrieved context or state that it doesn&apos;t
                  have the information.
                </p>
                <p className="text-muted-foreground leading-relaxed">
                  This approach solves three critical problems: <strong>hallucination</strong> (answers
                  are tied to sources), <strong>freshness</strong> (you control the knowledge base, not
                  the model&apos;s training cutoff), and <strong>verifiability</strong> (every claim
                  links back to a source you can inspect).
                </p>
              </div>
            </div>

            <div className="bg-secondary border border-border rounded-2xl p-6 lg:p-8">
              <h3 className="text-sm font-mono text-muted-foreground uppercase tracking-wider mb-4">Key Benefits</h3>
              <div className="space-y-4">
                {[
                  { label: "No hallucination", desc: "Answers are forced to use only retrieved context. Refusal mechanism prevents fabrication." },
                  { label: "Multi-source unification", desc: "PDFs, CSVs, and web content become one searchable knowledge base." },
                  { label: "Verifiable citations", desc: "Every answer includes source references. Users can inspect the exact source material." },
                  { label: "Always up-to-date", desc: "Upload new documents at any time. The knowledge base evolves with your content." },
                  { label: "Model-agnostic design", desc: "The retrieval pipeline works independently of the LLM. Swap models without rebuilding your index." },
                ].map((benefit) => (
                  <div key={benefit.label} className="flex gap-3">
                    <div className="w-5 h-5 rounded-full bg-emerald-500/10 flex items-center justify-center shrink-0 mt-0.5">
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium">{benefit.label}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">{benefit.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* System Components */}
      <section className="py-16 lg:py-20 border-t border-border">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="mb-12">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-4">
              <span className="w-12 h-px bg-foreground/30" />
              Architecture
            </span>
            <h2 className="text-3xl lg:text-4xl font-display tracking-tight">
              System Components
            </h2>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {systemComponents.map((comp) => (
              <Card key={comp.name} className="border-border/60">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
                      <comp.icon className="w-4 h-4 text-primary" />
                    </div>
                    <CardTitle className="text-base font-display">{comp.name}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground leading-relaxed">{comp.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12 flex items-center justify-between">
          <span className="text-sm text-muted-foreground font-mono">
            PDF Reviewer — Multi-Source RAG Knowledge Base
          </span>
          <span className="text-sm text-muted-foreground/60 font-mono">
            Powered by Gemini AI
          </span>
        </div>
      </footer>
    </main>
  );
}

function MessageSquare(props: React.ComponentProps<typeof Upload>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className={props.className}>
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  );
}
