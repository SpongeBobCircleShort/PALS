import { AskResponse } from "@/lib/types";
import { SourcePanel } from "@/components/SourcePanel";

export function TutorResponse({ response }: { response: AskResponse }) {
  return <section className="space-y-4"><div className="rounded-lg bg-slate-900 p-4"><h2 className="font-semibold">Socratic Questions</h2><ul className="mt-2 list-disc space-y-1 pl-5">{response.socraticQuestions.map((q) => <li key={q}>{q}</li>)}</ul></div><div className="rounded-lg bg-slate-900 p-4"><h3 className="font-semibold">Hint from Sources</h3><ul className="mt-2 list-disc pl-5">{response.hint.supportSentences.map((s) => <li key={s}>{s}</li>)}</ul></div><div className="rounded-lg bg-slate-900 p-4"><h3 className="font-semibold">Takeaway</h3><p className="mt-2 text-slate-300">{response.takeaway}</p></div><SourcePanel sources={response.sources} /></section>;
}
