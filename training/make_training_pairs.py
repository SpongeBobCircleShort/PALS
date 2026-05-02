import argparse, random, re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from training.common import load_config, read_jsonl, write_jsonl
ap=argparse.ArgumentParser(); ap.add_argument('--use-openai',action='store_true'); args=ap.parse_args()
cfg=load_config(); chunks=list(read_jsonl(Path(__file__).resolve().parent.joinpath(cfg['chunks_path']).resolve()))
texts=[c['text'] for c in chunks]; vec=TfidfVectorizer(stop_words='english', max_features=5000).fit(texts)
fn=vec.get_feature_names_out();
templates=["Explain the physics concept involving {keywords}.","What does this passage say about {keywords}?","How are {k1} and {k2} related in physics?","Why is {k1} important in this topic?","Give a conceptual explanation of {keywords}."]
pairs=[]
for c in chunks:
    toks=[w.lower() for w in re.findall(r'[A-Za-z]{4,}',c['text'])[:80]]
    uniq=list(dict.fromkeys(toks))[:6] or ['physics']
    k1=uniq[0]; k2=uniq[1] if len(uniq)>1 else uniq[0]; ks=', '.join(uniq[:3])
    for t in templates:
        pairs.append({'query':t.format(keywords=ks,k1=k1,k2=k2),'positive_text':c['text']})
random.shuffle(pairs); split=int(len(pairs)*0.9)
write_jsonl(Path(__file__).resolve().parent.joinpath(cfg['train_pairs_path']).resolve(), pairs[:split])
write_jsonl(Path(__file__).resolve().parent.joinpath(cfg['val_pairs_path']).resolve(), pairs[split:])
print(f'generated {len(pairs)} pairs (use-openai={args.use_openai})')
