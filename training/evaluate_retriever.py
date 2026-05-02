import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from training.common import load_config, read_jsonl
cfg=load_config(); val=list(read_jsonl(Path(__file__).resolve().parent.joinpath(cfg['val_pairs_path']).resolve())); model=SentenceTransformer(str(Path(cfg['output_dir'])/'final'))
queries=[cfg['query_prefix']+x['query'] for x in val]; passages=[cfg['passage_prefix']+x['positive_text'] for x in val]
q=model.encode(queries,normalize_embeddings=True); p=model.encode(passages,normalize_embeddings=True)
sim=np.matmul(q,p.T)
r1=r3=r5=mrr=0.0
for i,row in enumerate(sim):
    idx=np.argsort(-row)[:5]
    r1 += float(i in idx[:1]); r3 += float(i in idx[:3]); r5 += float(i in idx[:5]);
    rank=np.where(idx==i)[0]; mrr += 1.0/(rank[0]+1) if len(rank) else 0
n=len(val); print({'Recall@1':r1/n,'Recall@3':r3/n,'Recall@5':r5/n,'MRR@5':mrr/n})
