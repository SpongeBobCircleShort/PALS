import { NextResponse } from "next/server";
import { ZodError } from "zod";
import { askRequestSchema } from "@/lib/validation";
import { embedText } from "@/lib/embeddings";
import { querySimilar } from "@/lib/pinecone";
import { buildTutorResponse } from "@/lib/socratic";
import { SourceMatch } from "@/lib/types";

export async function POST(req: Request) {
  try {
    const parsed = askRequestSchema.parse(await req.json());

    const embedding = await embedText(parsed.question);

    let matches: SourceMatch[] = [];
    try {
      matches = await querySimilar(embedding, parsed.topK);
    } catch (error) {
      console.error("Pinecone retrieval failed; returning Socratic response without sources.", error);
    }

    return NextResponse.json(buildTutorResponse(parsed.question, parsed.showSources ? matches : []));
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json({ error: "Invalid request payload." }, { status: 400 });
    }

    const message = error instanceof Error ? error.message : "Unexpected error";

    if (message.includes("missing custom embedding endpoint")) {
      return NextResponse.json(
        {
          error:
            "Embedding is set to custom, but CUSTOM_EMBEDDING_ENDPOINT is not configured. Set EMBEDDING_PROVIDER=openai or provide a hosted custom endpoint."
        },
        { status: 500 }
      );
    }

    if (message.includes("missing OPENAI_API_KEY")) {
      return NextResponse.json(
        { error: "OPENAI_API_KEY is missing on the server. Add it in Vercel Project Environment Variables." },
        { status: 500 }
      );
    }

    return NextResponse.json({ error: "Unable to process request." }, { status: 500 });
  }
}
