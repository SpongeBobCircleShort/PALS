import OpenAI from "openai";
import { config } from "@/lib/config";

const openai = config.openaiApiKey ? new OpenAI({ apiKey: config.openaiApiKey }) : null;

export async function embedText(text: string): Promise<number[]> {
  if (config.embeddingProvider === "custom") {
    if (!config.customEmbeddingEndpoint) throw new Error("CUSTOM_EMBEDDING_ENDPOINT is required when EMBEDDING_PROVIDER=custom");
    const response = await fetch(config.customEmbeddingEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(config.customEmbeddingApiKey ? { Authorization: `Bearer ${config.customEmbeddingApiKey}` } : {})
      },
      body: JSON.stringify({ text })
    });
    if (!response.ok) throw new Error(`Custom embedding endpoint failed: ${response.status}`);
    const payload = (await response.json()) as { embedding: number[] };
    if (!Array.isArray(payload.embedding)) throw new Error("Custom embedding response missing embedding array");
    return payload.embedding;
  }

  if (!openai) throw new Error("OPENAI_API_KEY is required for OPENAI embeddings");
  const result = await openai.embeddings.create({ model: config.embeddingModel, input: text });
  return result.data[0].embedding;
}
