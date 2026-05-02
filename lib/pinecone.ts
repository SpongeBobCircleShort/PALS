import { Pinecone } from "@pinecone-database/pinecone";
import { config } from "@/lib/config";
import { SourceMatch } from "@/lib/types";

const pinecone = config.pineconeApiKey ? new Pinecone({ apiKey: config.pineconeApiKey }) : null;

export async function querySimilar(embedding: number[], topK: number): Promise<SourceMatch[]> {
  if (!pinecone) throw new Error("PINECONE_API_KEY is required");
  const index = pinecone.index(config.pineconeIndexName).namespace(config.pineconeNamespace);
  const response = await index.query({ vector: embedding, topK, includeMetadata: true });
  return (response.matches || []).map((m, i) => ({
    rank: i + 1,
    score: m.score ?? 0,
    sourceFile: String(m.metadata?.sourceFile ?? "unknown"),
    pageNum: Number(m.metadata?.pageNum ?? 0),
    chunkIndex: Number(m.metadata?.chunkIndex ?? 0),
    text: String(m.metadata?.text ?? "")
  }));
}
