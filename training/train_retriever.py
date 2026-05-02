import json, torch
from pathlib import Path
from datasets import Dataset
from sentence_transformers import SentenceTransformer, SentenceTransformerTrainer, losses
from sentence_transformers.training_args import SentenceTransformerTrainingArguments
from training.common import load_config, read_jsonl
cfg=load_config(); train=list(read_jsonl(Path(__file__).resolve().parent.joinpath(cfg['train_pairs_path']).resolve()))
model=SentenceTransformer(cfg['model_name'])
ds=Dataset.from_list([{'anchor':cfg['query_prefix']+r['query'],'positive':cfg['passage_prefix']+r['positive_text']} for r in train])
args=SentenceTransformerTrainingArguments(output_dir=cfg['output_dir'],num_train_epochs=cfg['epochs'],per_device_train_batch_size=cfg['train_batch_size'],learning_rate=float(cfg['learning_rate']),warmup_ratio=cfg['warmup_ratio'],seed=42,fp16=torch.cuda.is_available(),report_to=[])
trainer=SentenceTransformerTrainer(model=model,args=args,train_dataset=ds,loss=losses.MultipleNegativesRankingLoss(model))
trainer.train(); out=Path(cfg['output_dir'])/'final'; model.save(str(out)); (Path(cfg['output_dir'])/'training_stats.json').write_text(json.dumps({'train_examples':len(train)}))
print(f'saved model to {out}')
