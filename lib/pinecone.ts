import "server-only";
import { Pinecone } from "@pinecone-database/pinecone";
import { config } from "@/lib/config";
import { SourceMatch } from "@/lib/types";

const pinecone = config.pineconeApiKey ? new Pinecone({ apiKey: config.pineconeApiKey }) : null;

export async function querySimilar(embedding: number[], topK: number): Promise<SourceMatch[]> {
  if (!pinecone) throw new Error("Server misconfiguration: missing PINECONE_API_KEY");
  const index = pinecone.index(config.pineconeIndexName).namespace(config.pineconeNamespace);
  const response = await index.query({ vector: embedding, topK, includeMetadata: true });
  return (response.matches ?? []).map((m, i) => ({
    rank: i + 1,
    score: typeof m.score === "number" ? m.score : 0,
    sourceFile: typeof m.metadata?.sourceFile === "string" ? m.metadata.sourceFile : "unknown",
    pageNum: Number.isFinite(Number(m.metadata?.pageNum)) ? Number(m.metadata?.pageNum) : 0,
    chunkIndex: Number.isFinite(Number(m.metadata?.chunkIndex)) ? Number(m.metadata?.chunkIndex) : 0,
    text: typeof m.metadata?.text === "string" ? m.metadata.text : ""
  }));
}
