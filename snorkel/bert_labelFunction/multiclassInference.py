import json
import torch
from torch import nn
from multiclassModel import BertFineTuner
from transformers import (BertTokenizer)
from tqdm import tqdm
import textwrap


#target file
with open('./dev.json', 'r') as f:
    data = json.load(f)
#prepare model and tokenizer
model_path = './output/model.ckpt'
model = BertFineTuner.load_from_checkpoint(model_path, map_location='cuda:0')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#load label dict
with open('./label_dict.json', 'r') as f:
    label_dict = json.load(f)

softmax = nn.Softmax(dim=1)

for d in data:
    #prepare input text
    text = '[CLS] '+d['title'] + '[SEP]' + d['content']
    #for batch=1, if batch>1, use batch_encode_plus instead
    tokenizer_inputs = {}
    tokenizer_inputs["source_ids"] = tokenizer.encode_plus(
        text, max_length=300, truncation=True, return_tensors="pt"
            ).input_ids
    pred = model.predict_step(tokenizer_inputs).logits
    pred = torch.argmax(softmax(pred), dim=1)
    print(pred)
    pred = label_dict[str(int(pred))]
    text = textwrap.fill(text, width=80)
    print("===========Text=============")
    print(text)
    print("===========Pred=============")
    print(pred)
