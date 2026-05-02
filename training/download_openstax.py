import argparse, shutil, urllib.request
from pathlib import Path
from training.common import load_config
p=argparse.ArgumentParser(); p.add_argument('--urls'); p.add_argument('--copy-from')
a=p.parse_args(); cfg=load_config(); d=Path(__file__).resolve().parent.joinpath(cfg['data_dir']).resolve(); d.mkdir(parents=True,exist_ok=True)
if a.urls:
    for u in Path(a.urls).read_text().splitlines():
        u=u.strip();
        if u: urllib.request.urlretrieve(u, d / Path(u).name)
if a.copy_from:
    for f in Path(a.copy_from).glob('*.pdf'): shutil.copy2(f,d/f.name)
print(f'PDF directory ready: {d}')
