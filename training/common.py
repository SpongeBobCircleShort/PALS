import json, yaml
from pathlib import Path

def load_config():
    with open(Path(__file__).with_name('config.yaml'), 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def read_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def write_jsonl(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
