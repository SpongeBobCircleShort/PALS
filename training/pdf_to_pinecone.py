import argparse
import hashlib
import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from training.common import load_config


OPENAI_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
}


def clean_text(text):
    text = text.replace("\u00ad", "").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def iter_pdf_pages(pdf_path):
    reader = PdfReader(str(pdf_path))
    for page_num, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")
        if text:
            yield page_num, text


def chunk_words(text, max_words, overlap_words, min_words):
    words = text.split()
    if not words:
        return

    step = max(1, max_words - overlap_words)
    start = 0
    while start < len(words):
        chunk = words[start : start + max_words]
        if len(chunk) >= min_words or start + max_words >= len(words):
            yield " ".join(chunk)
        start += step


def stable_chunk_id(pdf_path, page_num, chunk_index, text):
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return f"{pdf_path.stem}-p{page_num}-c{chunk_index}-{digest}"


def extract_chunks(pdf_path, max_words, overlap_words, min_words):
    chunks = []
    for page_num, page_text in iter_pdf_pages(pdf_path):
        for chunk_index, text in enumerate(chunk_words(page_text, max_words, overlap_words, min_words)):
            chunks.append(
                {
                    "id": stable_chunk_id(pdf_path, page_num, chunk_index, text),
                    "sourceFile": pdf_path.name,
                    "pageNum": page_num,
                    "chunkIndex": chunk_index,
                    "text": text,
                }
            )
    return chunks


def make_openai_embedder(model_name, batch_size):
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    dimension = OPENAI_DIMENSIONS.get(model_name)

    def embed(texts):
        vectors = []
        for i in range(0, len(texts), batch_size):
            response = client.embeddings.create(model=model_name, input=texts[i : i + batch_size])
            vectors.extend(item.embedding for item in response.data)
        return vectors

    if dimension is None:
        sample = embed(["dimension probe"])[0]
        dimension = len(sample)

    return embed, dimension


def make_sentence_transformers_embedder(model_name, batch_size):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    sample = model.encode(["dimension probe"], normalize_embeddings=True)[0]
    dimension = len(sample)

    def embed(texts):
        return model.encode(texts, batch_size=batch_size, normalize_embeddings=True).tolist()

    return embed, dimension


def list_indexes_by_name(pc):
    indexes = {}
    for item in pc.list_indexes():
        if isinstance(item, dict):
            name = item.get("name")
        else:
            name = getattr(item, "name", None)
        if name:
            indexes[name] = item
    return indexes


def index_dimension(index_description):
    if isinstance(index_description, dict):
        return index_description.get("dimension")
    return getattr(index_description, "dimension", None)


def ensure_index(pc, name, dimension, metric, cloud, region):
    existing = list_indexes_by_name(pc)
    if name not in existing:
        pc.create_index(
            name=name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(cloud=cloud, region=region),
        )
        while not pc.describe_index(name).status["ready"]:
            time.sleep(2)
        return

    existing_dimension = index_dimension(existing[name])
    if existing_dimension is not None and int(existing_dimension) != int(dimension):
        raise ValueError(
            f"Pinecone index '{name}' has dimension {existing_dimension}, "
            f"but this embedding model produces {dimension}. Use a matching index "
            "or set PINECONE_INDEX_NAME to a new index name."
        )


def upsert_chunks(index, namespace, chunks, embed, batch_size):
    total = 0
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vectors = embed([chunk["text"] for chunk in batch])
        records = []
        for chunk, vector in zip(batch, vectors):
            records.append(
                {
                    "id": chunk["id"],
                    "values": vector,
                    "metadata": {
                        "sourceFile": chunk["sourceFile"],
                        "pageNum": chunk["pageNum"],
                        "chunkIndex": chunk["chunkIndex"],
                        "text": chunk["text"],
                    },
                }
            )
        index.upsert(vectors=records, namespace=namespace)
        total += len(records)
        print(f"upserted {total}/{len(chunks)} chunks")


def parse_args():
    cfg = load_config()
    default_provider = os.environ.get("EMBEDDING_PROVIDER", "openai")
    if default_provider not in {"openai", "sentence-transformers"}:
        default_provider = "openai"
    parser = argparse.ArgumentParser(description="Convert a PDF into Pinecone vectors.")
    parser.add_argument("pdf", type=Path, help="Path to the PDF file to index")
    parser.add_argument("--index", default=os.environ.get("PINECONE_INDEX_NAME", cfg["pinecone_index_name"]))
    parser.add_argument("--namespace", default=os.environ.get("PINECONE_NAMESPACE", cfg["pinecone_namespace"]))
    parser.add_argument("--cloud", default=cfg["pinecone_cloud"])
    parser.add_argument("--region", default=cfg["pinecone_region"])
    parser.add_argument("--metric", default=cfg["metric"])
    parser.add_argument("--max-words", type=int, default=cfg["max_words"])
    parser.add_argument("--min-words", type=int, default=cfg["min_words"])
    parser.add_argument("--overlap-words", type=int, default=cfg["overlap_words"])
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument(
        "--provider",
        choices=["openai", "sentence-transformers"],
        default=default_provider,
    )
    parser.add_argument("--embedding-model", default=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"))
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()
    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {pdf_path}")

    chunks = extract_chunks(pdf_path, args.max_words, args.overlap_words, args.min_words)
    if not chunks:
        raise ValueError(f"No extractable text found in {pdf_path}")

    if args.provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is required when --provider openai")
        embed, dimension = make_openai_embedder(args.embedding_model, args.batch_size)
    else:
        embed, dimension = make_sentence_transformers_embedder(args.embedding_model, args.batch_size)

    if not os.environ.get("PINECONE_API_KEY"):
        raise RuntimeError("PINECONE_API_KEY is required")

    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    ensure_index(pc, args.index, dimension, args.metric, args.cloud, args.region)
    index = pc.Index(args.index)
    upsert_chunks(index, args.namespace, chunks, embed, args.batch_size)
    print(f"indexed {len(chunks)} chunks from {pdf_path.name} into {args.index}/{args.namespace}")


if __name__ == "__main__":
    main()
