import { NextResponse } from "next/server";
import { ZodError } from "zod";
import { askRequestSchema } from "@/lib/validation";
import { embedText } from "@/lib/embeddings";
import { querySimilar } from "@/lib/pinecone";
import { buildTutorResponse } from "@/lib/socratic";

export async function POST(req: Request) {
  try {
    const parsed = askRequestSchema.parse(await req.json());
    const embedding = await embedText(parsed.question);
    const matches = await querySimilar(embedding, parsed.topK);
    return NextResponse.json(buildTutorResponse(parsed.question, parsed.showSources ? matches : []));
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json({ error: "Invalid request payload." }, { status: 400 });
    }
    const message = error instanceof Error ? error.message : "Unexpected error";
    const isServerConfig = message.toLowerCase().includes("server misconfiguration") || message.toLowerCase().includes("provider");
    return NextResponse.json({ error: isServerConfig ? "Server configuration or provider error." : "Unable to process request." }, { status: isServerConfig ? 500 : 400 });
  }
}
