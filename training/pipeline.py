import subprocess, sys
steps=['extract_text.py','make_chunks.py','make_training_pairs.py','train_retriever.py','evaluate_retriever.py','index_to_pinecone.py']
for s in steps:
    cmd=[sys.executable, __file__.replace('pipeline.py', s)]
    print('running', ' '.join(cmd)); subprocess.run(cmd, check=True)
