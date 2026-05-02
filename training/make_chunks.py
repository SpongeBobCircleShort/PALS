import uuid
from pathlib import Path
from training.common import load_config, read_jsonl, write_jsonl
cfg=load_config(); pages=Path(__file__).resolve().parent.parent/'data/pages.jsonl'; out=Path(__file__).resolve().parent.joinpath(cfg['chunks_path']).resolve()
maxw,minw,ov=cfg['max_words'],cfg['min_words'],cfg['overlap_words']; rows=[]
for p in read_jsonl(pages):
    words=p['text'].split(); i=0; idx=0
    while i < len(words):
        part=words[i:i+maxw]
        if len(part)>=minw or i+maxw>=len(words):
            rows.append({'chunk_id':str(uuid.uuid4()),'source_file':p['source_file'],'page_num':p['page_num'],'chunk_index':idx,'text':' '.join(part)})
            idx+=1
        i += max(1, maxw-ov)
write_jsonl(out, rows); print(f'wrote {len(rows)} chunks')
