import { Navigation } from "@/components/landing/navigation";
import { ChatInterface } from "@/components/rag/chat-interface";
import { UploadArea } from "@/components/rag/upload-area";
import { Button } from "@/components/ui/button";
import { Trash2, BookOpen, FileText, Globe, Zap } from "lucide-react";

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-x-hidden">
      <Navigation />

      {/* Hero Section */}
      <section className="relative min-h-screen flex flex-col pt-28 pb-12 overflow-hidden bg-black">
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

        <div className="relative z-10 w-full max-w-[1400px] mx-auto px-6 lg:px-12 flex-1 flex flex-col">
          <div className="mb-8">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-white/40">
              <span className="w-8 h-px bg-white/30" />
              Multi-Source RAG Knowledge Base
            </span>
          </div>
          <h1 className="text-[clamp(2rem,5vw,5rem)] font-display leading-[0.92] tracking-tight text-white mb-4">
            <span className="block">Ask your documents.</span>
            <span className="block text-white/40">Get grounded answers.</span>
          </h1>
          <p className="text-lg text-white/50 max-w-xl mb-10 leading-relaxed">
            Upload PDFs, CSVs, or add website URLs. Ask questions and get answers
            with citations from your own content — powered by RAG and Gemini AI.
          </p>

          <div className="grid lg:grid-cols-3 gap-6 flex-1">
            <div className="lg:col-span-1">
              <UploadArea />
            </div>
            <div className="lg:col-span-2 bg-secondary/30 border border-border rounded-2xl p-1">
              <ChatInterface />
            </div>
          </div>
        </div>
      </section>

      {/* How It Works - Keep the tree */}
      <section className="relative py-24 lg:py-32 bg-black text-white overflow-hidden">
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] rounded-full bg-white/[0.02] blur-[100px] pointer-events-none" />
        <div className="relative z-10 max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="relative mb-0 lg:mb-0 grid lg:grid-cols-2 gap-4 lg:gap-12 items-end">
            <div className="overflow-hidden pb-0 lg:pb-32">
              <div>
                <span className="inline-flex items-center gap-3 text-sm font-mono text-white/40 mb-8">
                  <span className="w-12 h-px bg-white/20" />
                  How it works
                </span>
              </div>
              <h2 className="text-6xl md:text-7xl lg:text-[128px] font-display tracking-tight leading-[0.85]">
                <span className="block">Upload.</span>
                <span className="block text-white/30">Ask.</span>
                <span className="block text-white/10">Get answers.</span>
              </h2>
            </div>
            <div className="relative h-[320px] lg:h-[640px] overflow-hidden">
              <img
                src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/tree-uAia6REvB137CQyHFCf0za3O6h2zKO.png"
                alt=""
                aria-hidden="true"
                className="absolute bottom-0 left-0 w-full h-full object-contain object-bottom"
              />
              <div className="absolute inset-0 bg-gradient-to-r from-black via-transparent to-transparent pointer-events-none" />
            </div>
          </div>

          <div className="grid lg:grid-cols-3 gap-4 mt-12">
            {[
              {
                number: "01",
                title: "Upload",
                subtitle: "your content",
                description: "Drag and drop PDFs, CSVs, or enter a website URL. Your documents are processed and indexed into a searchable vector database.",
                icon: UploadIcon,
              },
              {
                number: "02",
                title: "Ask",
                subtitle: "anything",
                description: "Type a question in natural language. The system retrieves the most relevant chunks from your indexed documents.",
                icon: AskIcon,
              },
              {
                number: "03",
                title: "Get answers",
                subtitle: "with citations",
                description: "Gemini AI generates a grounded answer using only your content. Every claim links back to the source document and page.",
                icon: AnswerIcon,
              },
            ].map((step, index) => (
              <div
                key={step.number}
                className="relative text-left p-8 lg:p-12 border border-white/25 bg-black"
              >
                <div className="flex items-center gap-4 mb-8">
                  <span className="text-4xl font-display text-white/20">{step.number}</span>
                  <div className="flex-1 h-px bg-white/10" />
                </div>
                <step.icon />
                <h3 className="text-3xl lg:text-4xl font-display mb-2 mt-4">{step.title}</h3>
                <span className="text-xl text-white/40 font-display block mb-6">{step.subtitle}</span>
                <p className="text-white/60 leading-relaxed">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="relative py-24 lg:py-32 overflow-hidden">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="grid lg:grid-cols-12 gap-8 items-end mb-16 lg:mb-24">
            <div className="lg:col-span-7">
              <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-6">
                <span className="w-12 h-px bg-foreground/30" />
                Features
              </span>
              <h2 className="text-5xl md:text-6xl lg:text-[96px] font-display tracking-tight leading-[0.9]">
                Intelligent
                <br />
                <span className="text-muted-foreground">knowledge retrieval.</span>
              </h2>
            </div>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { icon: FileText, title: "PDF & CSV", desc: "Upload text-based PDFs or CSV files with structured data." },
              { icon: Globe, title: "Web URLs", desc: "Ingest entire websites and ask questions about their content." },
              { icon: Zap, title: "RAG-powered", desc: "Semantic search retrieves the most relevant chunks for your query." },
              { icon: BookOpen, title: "Grounded answers", desc: "Every answer cites sources — no hallucination, full transparency." },
            ].map((feat, i) => (
              <div key={i} className="bg-secondary border border-border rounded-xl p-6">
                <feat.icon className="w-8 h-8 text-primary mb-4" />
                <h3 className="text-lg font-display mb-2">{feat.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{feat.desc}</p>
              </div>
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

function UploadIcon() {
  return (
    <svg className="w-8 h-8 text-[#eca8d6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
    </svg>
  );
}

function AskIcon() {
  return (
    <svg className="w-8 h-8 text-[#a78bfa]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
    </svg>
  );
}

function AnswerIcon() {
  return (
    <svg className="w-8 h-8 text-[#67e8f9]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0118 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3l1.5 1.5 3-3.75" />
    </svg>
  );
}
