import json
import torch
from multiclassModel import T5FineTuner
from transformers import (T5Tokenizer)
from tqdm import tqdm
import textwrap


#target file
with open('./dev.json', 'r') as f:
    data = json.load(f)
#prepare model and tokenizer
model_path = './output/model1.ckpt'
model = T5FineTuner.load_from_checkpoint(model_path, map_location='cuda:0')
tokenizer = T5Tokenizer.from_pretrained('t5-base')

for d in data:
    #prepare input text
    text = 'multi-class classification: '+d['title'] + '[SEP]' + d['content']
    #for batch=1, if batch>1, use batch_encode_plus instead
    tokenizer_inputs = {}
    tokenizer_inputs["source_ids"] = tokenizer.encode_plus(
        text, max_length=300, truncation=True, return_tensors="pt"
            ).input_ids
    pred = model.predict_step(tokenizer_inputs)
    pred = tokenizer.batch_decode(pred, skip_special_tokens=True)
    text = textwrap.fill(text, width=80)
    print("===========Text=============")
    print(text)
    print("===========Pred=============")
    print(pred)
