import os
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from training.common import load_config, read_jsonl

load_dotenv()
cfg = load_config()
root = Path(__file__).resolve().parent.parent
chunks = list(read_jsonl(root / "data/chunks.jsonl"))
model = SentenceTransformer(str((root / "models/physics-pals-bge-small/final").resolve()))
first_vec = model.encode([chunks[0]["text"]], normalize_embeddings=True)[0]
dim = len(first_vec)

if cfg["model_name"].endswith("bge-small-en-v1.5") and dim != 384:
    raise ValueError(f"Expected dim 384 for bge-small, got {dim}")
if cfg["model_name"].endswith("bge-base-en-v1.5") and dim != 768:
    raise ValueError(f"Expected dim 768 for bge-base, got {dim}")

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
idx_name = os.environ.get("PINECONE_INDEX_NAME", cfg["pinecone_index_name"])
existing = {i["name"]: i for i in pc.list_indexes()}
if idx_name not in existing:
    pc.create_index(name=idx_name, dimension=dim, metric=cfg["metric"], spec=ServerlessSpec(cloud=cfg["pinecone_cloud"], region=cfg["pinecone_region"]))
else:
    existing_dim = existing[idx_name]["dimension"]
    if existing_dim != dim:
      raise ValueError(f"Index dimension mismatch. index={existing_dim}, model={dim}")

index = pc.Index(idx_name)
ns = os.environ.get("PINECONE_NAMESPACE", cfg["pinecone_namespace"])
vectors = []
for c in chunks:
    e = model.encode([c["text"]], normalize_embeddings=True)[0].tolist()
    vectors.append({"id": c["chunk_id"], "values": e, "metadata": {"sourceFile": c["source_file"], "pageNum": c["page_num"], "chunkIndex": c["chunk_index"], "text": c["text"]}})
    if len(vectors) >= 50:
        index.upsert(vectors=vectors, namespace=ns)
        vectors = []
if vectors:
    index.upsert(vectors=vectors, namespace=ns)
print(f"upserted {len(chunks)} vectors with dim {dim}")
