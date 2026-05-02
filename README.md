# Physics Pals

Physics Pals is a Socratic physics tutor web app built with Next.js for Vercel plus a separate local/GPU retriever fine-tuning pipeline.

## Architecture
- **Vercel app only:** Next.js UI + lightweight API routes.
- **Retrieval:** Pinecone stores textbook chunk vectors and metadata.
- **Embeddings for query-time:**
  - `EMBEDDING_PROVIDER=openai` (default, easiest)
  - `EMBEDDING_PROVIDER=custom` (hosted fine-tuned endpoint)
- **Training/indexing:** run locally, Colab, Kaggle, RunPod, Modal, etc. Never on Vercel.

## Setup (Web)
```bash
npm install
npm run dev
npm run build
```

Copy `.env.example` to `.env.local` and set keys.

## API
`POST /api/ask` returns Socratic questions, hint support sentences, takeaway, and sources.

## Vercel Deployment
Deploy only this Next.js app. Add environment variables in the Vercel dashboard. Do **not** train or run large local ML models in Vercel routes.

## Custom embedding model hosting options
1. Keep using OpenAI embeddings in production.
2. Host the fine-tuned sentence-transformers model on Hugging Face Inference Endpoints, Modal, RunPod, Replicate, or a small FastAPI service.
3. Set:
   - `EMBEDDING_PROVIDER=custom`
   - `CUSTOM_EMBEDDING_ENDPOINT=...`
   - `CUSTOM_EMBEDDING_API_KEY=...`

**Consistency rule:** if chunks are indexed with the custom model, queries must use the same model. Mixing OpenAI query embeddings with custom-indexed chunks causes vector-space mismatch.

## OpenStax licensing and attribution caution
OpenStax content requires proper attribution. OpenStax pages may restrict using their textbook content for training large language models or generative AI offerings without permission. This project is designed for a small retrieval/embedding model powering educational RAG over attributed passages, not for training a generative LLM to reproduce OpenStax content.
