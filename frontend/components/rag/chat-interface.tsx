"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Send, Loader2, Bot, User, BookOpen } from "lucide-react";

interface Citation {
  source: string;
  page: number;
  excerpt: string;
  score?: number;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<{ total_chunks: number; unique_sources: number } | null>(null);
  const [sources, setSources] = useState<{ source: string; type: string; chunks: number }[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchStats();
    fetchSources();
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/stats`);
      if (res.ok) setStats(await res.json());
    } catch {}
  };

  const fetchSources = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/sources`);
      if (res.ok) setSources(await res.json());
    } catch {}
  };

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const chatHistory = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await fetch(`${API_BASE}/api/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input, chat_history: chatHistory }),
      });

      if (!res.ok) throw new Error("Query failed");

      const data = await res.json();
      const assistantMsg: Message = {
        role: "assistant",
        content: data.answer,
        citations: data.citations || [],
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
      fetchStats();
      fetchSources();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex gap-6 h-full">
      <div className="flex-1 flex flex-col">
        <ScrollArea ref={scrollRef} className="flex-1 pr-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center py-20">
              <BookOpen className="w-16 h-16 text-muted-foreground/30 mb-6" />
              <h3 className="text-2xl font-display text-muted-foreground mb-2">
                Ask anything about your documents
              </h3>
              <p className="text-muted-foreground/60 max-w-md">
                Upload PDFs, CSVs, or add website URLs, then ask questions.
                The AI will answer using only your uploaded content.
              </p>
            </div>
          ) : (
            <div className="space-y-6 py-6">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  {msg.role === "assistant" && (
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0 mt-1">
                      <Bot className="w-4 h-4 text-primary" />
                    </div>
                  )}
                  <div
                    className={`max-w-[75%] rounded-2xl px-5 py-3 ${
                      msg.role === "user"
                        ? "bg-primary text-primary-foreground rounded-br-sm"
                        : "bg-secondary border border-border rounded-bl-sm"
                    }`}
                  >
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-border/50">
                        <p className="text-xs text-muted-foreground mb-2 font-mono">
                          Sources ({msg.citations.length})
                        </p>
                        <div className="space-y-2">
                          {msg.citations.map((cit, j) => (
                            <div
                              key={j}
                              className="text-xs bg-background/50 rounded-lg p-2.5 border border-border/50"
                            >
                              <div className="flex items-center gap-2 mb-1">
                                <span className="font-medium text-foreground/80">
                                  {cit.source}
                                </span>
                                <Badge variant="outline" className="text-[10px] px-1.5 py-0">
                                  p.{cit.page}
                                </Badge>
                                {cit.score !== undefined && (
                                  <span className="text-muted-foreground ml-auto">
                                    {cit.score.toFixed(3)}
                                  </span>
                                )}
                              </div>
                              <p className="text-muted-foreground/70 leading-relaxed">
                                {cit.excerpt}...
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  {msg.role === "user" && (
                    <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0 mt-1">
                      <User className="w-4 h-4 text-primary-foreground" />
                    </div>
                  )}
                </div>
              ))}
              {loading && (
                <div className="flex gap-4">
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0 mt-1">
                    <Loader2 className="w-4 h-4 text-primary animate-spin" />
                  </div>
                  <div className="bg-secondary border border-border rounded-2xl rounded-bl-sm px-5 py-3">
                    <div className="flex gap-1.5">
                      <div className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "0ms" }} />
                      <div className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "150ms" }} />
                      <div className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "300ms" }} />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </ScrollArea>

        <div className="flex gap-3 pt-4 border-t border-border">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={loading ? "Waiting for response..." : "Ask a question about your documents..."}
            disabled={loading}
            className="bg-secondary border-border rounded-xl"
          />
          <Button
            onClick={sendMessage}
            disabled={!input.trim() || loading}
            size="icon"
            className="rounded-xl shrink-0"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </Button>
        </div>
      </div>

      <div className="w-72 shrink-0 hidden lg:block">
        <div className="sticky top-24 space-y-4">
          {stats && (
            <div className="bg-secondary border border-border rounded-xl p-4">
              <p className="text-xs font-mono text-muted-foreground mb-3 uppercase tracking-wider">
                Knowledge Base
              </p>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-background rounded-lg p-3 text-center">
                  <p className="text-2xl font-display text-primary">{stats.total_chunks}</p>
                  <p className="text-[10px] text-muted-foreground font-mono">Chunks</p>
                </div>
                <div className="bg-background rounded-lg p-3 text-center">
                  <p className="text-2xl font-display text-primary">{stats.unique_sources}</p>
                  <p className="text-[10px] text-muted-foreground font-mono">Sources</p>
                </div>
              </div>
            </div>
          )}

          {sources.length > 0 && (
            <div className="bg-secondary border border-border rounded-xl p-4">
              <p className="text-xs font-mono text-muted-foreground mb-3 uppercase tracking-wider">
                Indexed Sources
              </p>
              <div className="space-y-2">
                {sources.map((s, i) => (
                  <div key={i} className="flex items-center gap-2 text-xs">
                    <span className="text-muted-foreground">
                      {s.type === "pdf" ? "📄" : s.type === "csv" ? "📊" : "🌐"}
                    </span>
                    <span className="text-foreground/80 truncate flex-1">{s.source}</span>
                    <span className="text-muted-foreground font-mono">{s.chunks}c</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
