export const config = {
  openaiApiKey: process.env.OPENAI_API_KEY,
  pineconeApiKey: process.env.PINECONE_API_KEY,
  pineconeIndexName: process.env.PINECONE_INDEX_NAME || "pals-database-bge-small",
  pineconeNamespace: process.env.PINECONE_NAMESPACE || "pals-database",
  embeddingProvider: process.env.EMBEDDING_PROVIDER || "bge-local",
  embeddingModel: process.env.EMBEDDING_MODEL || "Xenova/bge-small-en-v1.5",
  bgeQueryPrefix:
    process.env.BGE_QUERY_PREFIX || "Represent this sentence for searching relevant physics passages: ",
  customEmbeddingEndpoint: process.env.CUSTOM_EMBEDDING_ENDPOINT,
  customEmbeddingApiKey: process.env.CUSTOM_EMBEDDING_API_KEY,
  openaiChatModel: process.env.OPENAI_CHAT_MODEL || "gpt-4.1-mini"
};
