import { NextResponse } from "next/server";
import { askRequestSchema } from "@/lib/validation";
import { embedText } from "@/lib/embeddings";
import { querySimilar } from "@/lib/pinecone";
import { buildTutorResponse } from "@/lib/socratic";

export async function POST(req: Request) {
  try {
    const json = await req.json();
    const parsed = askRequestSchema.parse(json);
    const embedding = await embedText(parsed.question);
    const matches = await querySimilar(embedding, parsed.topK);
    return NextResponse.json(buildTutorResponse(parsed.question, parsed.showSources ? matches : []));
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
