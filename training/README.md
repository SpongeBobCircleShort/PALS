# Physics Pals Training Pipeline

This folder contains the local/GPU pipeline for OpenStax physics retrieval fine-tuning.

## Prepare data
Place PDFs in `data/openstax/` manually, or use:
```bash
python training/download_openstax.py --urls urls.txt
```

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r training/requirements.txt
```

## Run step-by-step
```bash
python training/extract_text.py
python training/make_chunks.py
python training/make_training_pairs.py
python training/train_retriever.py
python training/evaluate_retriever.py
python training/index_to_pinecone.py
```

## Index one PDF directly to Pinecone
This uses the same Pinecone metadata fields as the app (`sourceFile`, `pageNum`, `chunkIndex`, `text`). By default it uses OpenAI embeddings, which matches the app defaults in `.env.example`.

```bash
export OPENAI_API_KEY=...
export PINECONE_API_KEY=...
python training/pdf_to_pinecone.py data/openstax/your-file.pdf
```

Optional overrides:
```bash
PINECONE_INDEX_NAME=my-index PINECONE_NAMESPACE=my-pdf \
python training/pdf_to_pinecone.py data/openstax/your-file.pdf \
  --embedding-model text-embedding-3-small
```

To index with a local sentence-transformers model instead:
```bash
python training/pdf_to_pinecone.py data/openstax/your-file.pdf \
  --provider sentence-transformers \
  --embedding-model BAAI/bge-small-en-v1.5
```

## Run full pipeline
```bash
python training/pipeline.py
```

## Notes
- Index dimension must match embedding model dimension; script infers dimension from an actual embedding and creates/validates Pinecone index accordingly.
- Avoid committing PDFs, model artifacts, or API keys.
- OpenStax attribution and licensing caution still applies.
