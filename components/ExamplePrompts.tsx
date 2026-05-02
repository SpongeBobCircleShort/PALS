const prompts = [
  "Why does drag lead to terminal velocity?",
  "How do numerical methods solve differential equations?",
  "What are Fourier modes?",
  "How does Monte Carlo simulation work in physics?",
  "Why do planets stay in orbit?"
];

export function ExamplePrompts({ onSelect }: { onSelect: (prompt: string) => void }) {
  return <div className="flex flex-wrap gap-2">{prompts.map((p) => <button key={p} className="rounded-full bg-slate-800 px-3 py-2 text-sm hover:bg-slate-700" onClick={() => onSelect(p)}>{p}</button>)}</div>;
}
