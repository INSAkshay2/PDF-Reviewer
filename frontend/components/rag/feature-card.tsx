import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { ReactNode } from "react";

interface FeatureCardProps {
  title: string;
  description: string;
  details: string[];
  icon: ReactNode;
  status?: "implemented" | "planned";
}

export function FeatureCard({
  title,
  description,
  details,
  icon,
  status = "implemented",
}: FeatureCardProps) {
  return (
    <Card className="relative overflow-hidden border-border/60 group hover:border-primary/30 transition-all duration-500">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
            {icon}
          </div>
          {status === "planned" ? (
            <Badge variant="outline" className="text-[10px] font-mono border-amber-500/30 text-amber-400">
              Planned
            </Badge>
          ) : (
            <Badge variant="secondary" className="text-[10px] font-mono text-emerald-400 border-emerald-500/30">
              Implemented
            </Badge>
          )}
        </div>
        <CardTitle className="text-lg font-display mt-3">{title}</CardTitle>
        <CardDescription className="text-sm leading-relaxed">{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="space-y-1.5">
          {details.map((detail, i) => (
            <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
              <span className="text-primary mt-1 shrink-0">▸</span>
              {detail}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
