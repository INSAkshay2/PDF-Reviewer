import { Navigation } from "@/components/landing/navigation";
import { FeatureCard } from "@/components/rag/feature-card";
import { implementedFeatures, plannedFeatures } from "@/components/rag/features-content";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { ArrowRight, Lightbulb, FileText, Globe, Zap, BookOpen } from "lucide-react";

const stats = [
  { value: "3", label: "Source types" },
  { value: "10", label: "Pipeline stages" },
  { value: "384", label: "Embedding dimensions" },
  { value: "800", label: "Default chunk size" },
];

export default function FeaturesPage() {
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
              Capabilities
            </span>
          </div>
          <h1 className="text-[clamp(2.5rem,6vw,6rem)] font-display leading-[0.92] tracking-tight text-white mb-6">
            <span className="block">Features</span>
          </h1>
          <p className="text-lg text-white/50 max-w-2xl leading-relaxed mb-10">
            A production-grade RAG knowledge base that ingests PDFs, CSVs, and websites,
            indexes them with FAISS and BGE embeddings, and answers questions using
            Google Gemini — with full source attribution on every response.
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {stats.map((stat) => (
              <div key={stat.label} className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                <p className="text-2xl lg:text-3xl font-display text-white">{stat.value}</p>
                <p className="text-[10px] font-mono text-white/40 uppercase tracking-wider mt-1">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Implemented Features */}
      <section className="py-16 lg:py-20 border-t border-border">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="mb-4">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-4">
              <span className="w-12 h-px bg-foreground/30" />
              Implemented Now
            </span>
          </div>
          <div className="flex items-center gap-3 mb-10">
            <h2 className="text-3xl lg:text-4xl font-display tracking-tight">
              Current Capabilities
            </h2>
            <Badge variant="secondary" className="text-[10px] font-mono text-emerald-400 border-emerald-500/30">
              Production
            </Badge>
          </div>

          <div className="grid md:grid-cols-2 gap-5">
            {implementedFeatures.map((feature) => (
              <FeatureCard key={feature.title} {...feature} />
            ))}
          </div>
        </div>
      </section>

      {/* Extensible Architecture */}
      <section className="py-16 lg:py-20 border-t border-border">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="mb-12">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-4">
              <span className="w-12 h-px bg-foreground/30" />
              Extensibility
            </span>
            <h2 className="text-3xl lg:text-4xl font-display tracking-tight">
              Extensible Architecture
            </h2>
            <p className="text-muted-foreground mt-3 max-w-2xl leading-relaxed">
              The system is built with modular interfaces that make it straightforward to
              add new capabilities without rewriting existing components. This section
              describes the architectural patterns that enable future growth.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            {[
              {
                title: "Pluggable Loaders",
                desc: "Adding a new source type (e.g., Word docs, databases, APIs) requires only implementing a loader function that returns a list of Document objects.",
                icon: FileText,
              },
              {
                title: "Swappable Embeddings",
                desc: "The Embedder class abstracts the embedding model. Swap BGE for OpenAI, Cohere, or any sentence-transformers model by changing one configuration value.",
                icon: Zap,
              },
              {
                title: "Interchangeable LLMs",
                desc: "The LLM client wraps the generation API behind a standard interface. Replace Gemini with GPT, Claude, or a local model by implementing the same method signature.",
                icon: Globe,
              },
              {
                title: "Composable Pipeline",
                desc: "Each pipeline stage (chunker, embedder, retriever, etc.) is an independent class. Stages can be replaced, reordered, or extended without affecting the rest of the system.",
                icon: BookOpen,
              },
            ].map((item) => (
              <Card key={item.title} className="border-border/60 lg:col-span-1 md:col-span-1">
                <CardHeader>
                  <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center mb-2">
                    <item.icon className="w-4 h-4 text-primary" />
                  </div>
                  <CardTitle className="text-base font-display">{item.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Planned / Next */}
      <section className="py-16 lg:py-20 border-t border-border">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="mb-4">
            <span className="inline-flex items-center gap-3 text-sm font-mono text-muted-foreground mb-4">
              <span className="w-12 h-px bg-foreground/30" />
              Roadmap
            </span>
          </div>
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-3xl lg:text-4xl font-display tracking-tight">
              Planned & Upcoming
            </h2>
            <Badge variant="outline" className="text-[10px] font-mono border-amber-500/30 text-amber-400">
              Roadmap
            </Badge>
          </div>
          <p className="text-muted-foreground max-w-2xl leading-relaxed mb-10">
            These features are on the development roadmap. The modular architecture makes
            them natural extensions of the existing pipeline rather than ground-up rewrites.
          </p>

          <div className="grid md:grid-cols-2 gap-5">
            {plannedFeatures.map((feature) => (
              <FeatureCard key={feature.title} {...feature} />
            ))}
          </div>

          <div className="mt-8 bg-secondary/50 border border-dashed border-border rounded-2xl p-6 lg:p-8">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center shrink-0">
                <Lightbulb className="w-5 h-5 text-amber-400" />
              </div>
              <div>
                <h3 className="text-base font-display mb-2">Future Directions</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Beyond the immediate roadmap, the architecture supports adding an analytics
                  dashboard for query monitoring, user workspaces for multi-tenant isolation,
                  source-level filtering for targeted search, evaluation metrics for retrieval
                  quality benchmarking, and graph-based retrieval for entity-relationship queries.
                  Each addition builds on the existing modular pipeline without requiring
                  structural changes.
                </p>
              </div>
            </div>
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
