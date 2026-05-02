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
1. Copy `.env.example` to `.env.local`.
2. Fill in environment values.
3. Run:
```bash
npm install
npm run dev
npm run build
```

## API
`POST /api/ask` accepts `{ question, topK, showSources }` and returns Socratic questions, hint support sentences, takeaway, and sources.

## Vercel deployment
1. Push repo to Git provider.
2. Import project in Vercel.
3. Set env vars from `.env.example` in Vercel dashboard.
4. Deploy.

> Deploy only the Next.js app. Do not fine-tune models or run heavy local ML models inside Vercel routes.

## Training pipeline (local/GPU only)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r training/requirements.txt
python training/pipeline.py
```

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
