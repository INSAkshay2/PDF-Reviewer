import { Upload, FileText, GitMerge, Layers, Database, Search, Brain, BookOpen } from "lucide-react";
import type { ReactNode } from "react";

const stages: { label: string; icon: ReactNode }[] = [
  { label: "Ingest", icon: <Upload className="w-4 h-4" /> },
  { label: "Process", icon: <FileText className="w-4 h-4" /> },
  { label: "Chunk", icon: <GitMerge className="w-4 h-4" /> },
  { label: "Embed", icon: <Layers className="w-4 h-4" /> },
  { label: "Index", icon: <Database className="w-4 h-4" /> },
  { label: "Retrieve", icon: <Search className="w-4 h-4" /> },
  { label: "Generate", icon: <Brain className="w-4 h-4" /> },
  { label: "Cite", icon: <BookOpen className="w-4 h-4" /> },
];

export function PipelineDiagram() {
  return (
    <div className="w-full overflow-x-auto pb-4">
      <div className="flex items-center gap-0 min-w-max">
        {stages.map((stage, i) => (
          <div key={stage.label} className="flex items-center">
            <div className="flex flex-col items-center gap-2 px-3">
              <div className="w-12 h-12 rounded-xl bg-secondary border border-border flex items-center justify-center text-primary group-hover:bg-primary/10 transition-colors">
                {stage.icon}
              </div>
              <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider whitespace-nowrap">
                {stage.label}
              </span>
            </div>
            {i < stages.length - 1 && (
              <div className="flex items-center">
                <div className="w-6 h-px bg-border" />
                <div className="w-1.5 h-1.5 rotate-45 border-t border-r border-border -ml-[3px]" />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
