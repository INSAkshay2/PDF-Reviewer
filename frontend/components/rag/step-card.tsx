import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { ReactNode } from "react";

interface StepCardProps {
  number: string;
  title: string;
  description: string;
  whyMatters: string;
  technologies: string[];
  icon: ReactNode;
  gradient?: string;
}

export function StepCard({
  number,
  title,
  description,
  whyMatters,
  technologies,
  icon,
  gradient = "from-primary/5 to-transparent",
}: StepCardProps) {
  return (
    <Card className="relative overflow-hidden border-border/60 group hover:border-primary/30 transition-all duration-500">
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-50 group-hover:opacity-80 transition-opacity`} />
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <span className="font-mono text-3xl font-bold text-muted-foreground/30">{number}</span>
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
              {icon}
            </div>
          </div>
        </div>
        <CardTitle className="text-xl font-display mt-2">{title}</CardTitle>
        <CardDescription className="text-sm leading-relaxed mt-1">{description}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-xs font-mono text-muted-foreground uppercase tracking-wider mb-1.5">Why it matters</p>
          <p className="text-sm text-foreground/80 leading-relaxed">{whyMatters}</p>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {technologies.map((tech) => (
            <Badge key={tech} variant="secondary" className="font-mono text-[10px]">
              {tech}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
