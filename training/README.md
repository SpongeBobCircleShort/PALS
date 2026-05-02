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

## Run full pipeline
```bash
python training/pipeline.py
```

## Notes
- Index dimension must match embedding model dimension; script infers dimension from an actual embedding and creates/validates Pinecone index accordingly.
- Avoid committing PDFs, model artifacts, or API keys.
- OpenStax attribution and licensing caution still applies.
