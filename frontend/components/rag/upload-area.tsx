"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { getApiBaseUrl } from "@/lib/api";
import {
  Upload,
  FileText,
  Globe,
  Loader2,
  CheckCircle,
  XCircle,
} from "lucide-react";

const API_BASE = getApiBaseUrl();

export function UploadArea() {
  const { toast } = useToast();
  const [uploading, setUploading] = useState(false);
  const [ingestingUrl, setIngestingUrl] = useState(false);
  const [url, setUrl] = useState("");

  const handleFileUpload = useCallback(
    async (file: File) => {
      setUploading(true);
      try {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch(`${API_BASE}/api/upload`, {
          method: "POST",
          body: formData,
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || "Upload failed");
        }

        const result = await res.json();
        toast({
          title: "Success",
          description: `${result.source}: ${result.num_chunks} chunks indexed`,
        });
      } catch (e: any) {
        toast({
          title: "Error",
          description: e.message || "Upload failed",
          variant: "destructive",
        });
      } finally {
        setUploading(false);
      }
    },
    [toast],
  );

  const handleUrlIngest = async () => {
    if (!url.trim()) return;
    setIngestingUrl(true);
    try {
      const res = await fetch(`${API_BASE}/api/ingest-url`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Ingest failed");
      }

      const result = await res.json();
      toast({
        title: "Success",
        description: `${url.slice(0, 50)}: ${result.num_chunks} chunks indexed`,
      });
      setUrl("");
    } catch (e: any) {
      toast({
        title: "Error",
        description: e.message || "URL ingest failed",
        variant: "destructive",
      });
    } finally {
      setIngestingUrl(false);
    }
  };

  return (
    <div className="bg-secondary/50 border border-border rounded-2xl p-6">
      <Tabs defaultValue="pdf" className="w-full">
        <TabsList className="grid grid-cols-3 mb-6">
          <TabsTrigger value="pdf" className="gap-2">
            <FileText className="w-4 h-4" />
            PDF
          </TabsTrigger>
          <TabsTrigger value="csv" className="gap-2">
            <FileText className="w-4 h-4" />
            CSV
          </TabsTrigger>
          <TabsTrigger value="url" className="gap-2">
            <Globe className="w-4 h-4" />
            URL
          </TabsTrigger>
        </TabsList>

        <TabsContent value="pdf" className="mt-0">
          <div className="border-2 border-dashed border-border rounded-xl p-8 text-center hover:border-primary/50 transition-colors group">
            <input
              type="file"
              accept=".pdf"
              id="pdf-upload"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFileUpload(file);
              }}
              disabled={uploading}
            />
            <label
              htmlFor="pdf-upload"
              className="cursor-pointer flex flex-col items-center gap-3"
            >
              <Upload className="w-8 h-8 text-muted-foreground group-hover:text-primary transition-colors" />
              <div>
                <p className="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                  {uploading ? "Uploading..." : "Drop a PDF or click to browse"}
                </p>
                <p className="text-xs text-muted-foreground/60 mt-1">
                  Text-based PDF documents only
                </p>
              </div>
            </label>
          </div>
        </TabsContent>

        <TabsContent value="csv" className="mt-0">
          <div className="border-2 border-dashed border-border rounded-xl p-8 text-center hover:border-primary/50 transition-colors group">
            <input
              type="file"
              accept=".csv"
              id="csv-upload"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFileUpload(file);
              }}
              disabled={uploading}
            />
            <label
              htmlFor="csv-upload"
              className="cursor-pointer flex flex-col items-center gap-3"
            >
              <Upload className="w-8 h-8 text-muted-foreground group-hover:text-primary transition-colors" />
              <div>
                <p className="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                  {uploading ? "Uploading..." : "Drop a CSV or click to browse"}
                </p>
                <p className="text-xs text-muted-foreground/60 mt-1">
                  CSV files with text data
                </p>
              </div>
            </label>
          </div>
        </TabsContent>

        <TabsContent value="url" className="mt-0">
          <div className="flex gap-3">
            <Input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              disabled={ingestingUrl}
              className="bg-background border-border rounded-xl"
            />
            <Button
              onClick={handleUrlIngest}
              disabled={!url.trim() || ingestingUrl}
              className="rounded-xl shrink-0 gap-2"
            >
              {ingestingUrl ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Globe className="w-4 h-4" />
              )}
              Ingest
            </Button>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
