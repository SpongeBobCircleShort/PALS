import re
from pathlib import Path
from pypdf import PdfReader
from training.common import load_config, write_jsonl
cfg=load_config(); data_dir=Path(__file__).resolve().parent.joinpath(cfg['data_dir']).resolve(); out=Path(__file__).resolve().parent.parent/'data/pages.jsonl'
rows=[]
for pdf in data_dir.glob('*.pdf'):
    r=PdfReader(str(pdf))
    for i,page in enumerate(r.pages, start=1):
        text=(page.extract_text() or '').replace('\u00ad','').replace('\n',' ')
        text=re.sub(r'\s+',' ',text).strip(); text=re.sub(r'^\d+\s*','',text)
        if len(text)>20: rows.append({'source_file':pdf.name,'page_num':i,'text':text})
write_jsonl(out, rows); print(f'wrote {len(rows)} pages to {out}')
