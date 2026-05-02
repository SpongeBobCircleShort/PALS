"use client";
import { useState } from "react";
import { ExamplePrompts } from "@/components/ExamplePrompts";
import { LoadingState } from "@/components/LoadingState";
import { ErrorMessage } from "@/components/ErrorMessage";
import { TutorResponse } from "@/components/TutorResponse";
import { AskResponse } from "@/lib/types";

export function ChatInterface() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<AskResponse | null>(null);
  const ask = async () => {
    setLoading(true); setError(null);
    try {
      const r = await fetch("/api/ask", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question, topK: 3, showSources: true }) });
      const payload = await r.json();
      if (!r.ok) throw new Error(payload.error || "Request failed");
      setResponse(payload);
    } catch (e) { setError(e instanceof Error ? e.message : "Unknown error"); }
    finally { setLoading(false); }
  };
  return <section className="space-y-4"><textarea value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ask a physics question..." className="min-h-36 w-full rounded-xl bg-slate-900 p-4 text-lg" /><ExamplePrompts onSelect={setQuestion} /><button onClick={ask} disabled={loading || !question.trim()} className="rounded-lg bg-cyan-500 px-6 py-3 font-semibold text-slate-950 disabled:opacity-40">Ask</button>{loading && <LoadingState />}{error && <ErrorMessage message={error} />}{response && <TutorResponse response={response} />}</section>;
}
