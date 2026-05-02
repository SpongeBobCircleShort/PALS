export const config = {
  openaiApiKey: process.env.OPENAI_API_KEY,
  pineconeApiKey: process.env.PINECONE_API_KEY,
  pineconeIndexName: process.env.PINECONE_INDEX_NAME || "physics-pals",
  pineconeNamespace: process.env.PINECONE_NAMESPACE || "openstax-physics",
  embeddingProvider: process.env.EMBEDDING_PROVIDER || "openai",
  embeddingModel: process.env.EMBEDDING_MODEL || "text-embedding-3-small",
  customEmbeddingEndpoint: process.env.CUSTOM_EMBEDDING_ENDPOINT,
  customEmbeddingApiKey: process.env.CUSTOM_EMBEDDING_API_KEY,
  openaiChatModel: process.env.OPENAI_CHAT_MODEL || "gpt-4.1-mini"
};
