import os
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from training.common import load_config, read_jsonl
load_dotenv(); cfg=load_config(); chunks=list(read_jsonl(Path(__file__).resolve().parent.joinpath(cfg['chunks_path']).resolve()))
model=SentenceTransformer(str(Path(cfg['output_dir'])/'final')); vec=model.encode([chunks[0]['text']],normalize_embeddings=True)[0]; dim=len(vec)
pc=Pinecone(api_key=os.environ['PINECONE_API_KEY']); idx_name=os.environ.get('PINECONE_INDEX_NAME',cfg['pinecone_index_name'])
if idx_name not in [i['name'] for i in pc.list_indexes()]:
    pc.create_index(name=idx_name,dimension=dim,metric=cfg['metric'],spec=ServerlessSpec(cloud=cfg['pinecone_cloud'],region=cfg['pinecone_region']))
index=pc.Index(idx_name); ns=os.environ.get('PINECONE_NAMESPACE',cfg['pinecone_namespace'])
vectors=[]
for c in chunks:
    e=model.encode([c['text']],normalize_embeddings=True)[0].tolist()
    vectors.append({'id':c['chunk_id'],'values':e,'metadata':{'sourceFile':c['source_file'],'pageNum':c['page_num'],'chunkIndex':c['chunk_index'],'text':c['text']}})
    if len(vectors)>=50: index.upsert(vectors=vectors,namespace=ns); vectors=[]
if vectors: index.upsert(vectors=vectors,namespace=ns)
print(f'upserted {len(chunks)} vectors with dim {dim}')
