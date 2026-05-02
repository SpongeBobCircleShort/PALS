import { SourceMatch } from "@/lib/types";

export function SourcePanel({ sources }: { sources: SourceMatch[] }) {
  return <details className="rounded-lg bg-slate-900 p-4"><summary className="cursor-pointer font-semibold">Sources ({sources.length})</summary><div className="mt-3 space-y-3">{sources.map((s) => <article key={`${s.rank}-${s.chunkIndex}`} className="rounded border border-slate-700 p-3 text-sm"><p className="font-medium">#{s.rank} {s.sourceFile} p.{s.pageNum} chunk {s.chunkIndex} (score {s.score.toFixed(3)})</p><p className="mt-2 text-slate-300">{s.text}</p></article>)}</div></details>;
}
