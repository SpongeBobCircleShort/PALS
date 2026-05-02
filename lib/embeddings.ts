import "server-only";
import OpenAI from "openai";
import { config } from "@/lib/config";

const openai = config.openaiApiKey ? new OpenAI({ apiKey: config.openaiApiKey }) : null;

export async function embedText(text: string): Promise<number[]> {
  if (config.embeddingProvider === "custom") {
    if (!config.customEmbeddingEndpoint) {
      throw new Error("Server misconfiguration: missing custom embedding endpoint");
    }
    const response = await fetch(config.customEmbeddingEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(config.customEmbeddingApiKey ? { Authorization: `Bearer ${config.customEmbeddingApiKey}` } : {})
      },
      body: JSON.stringify({ text })
    });
    if (!response.ok) throw new Error("Embedding provider unavailable");
    const payload = (await response.json()) as { embedding?: number[] };
    if (!Array.isArray(payload.embedding) || payload.embedding.length === 0) {
      throw new Error("Embedding provider returned invalid embedding");
    }
    return payload.embedding;
  }

  if (!openai) throw new Error("Server misconfiguration: missing OPENAI_API_KEY");
  const result = await openai.embeddings.create({ model: config.embeddingModel, input: text });
  return result.data[0].embedding;
}
