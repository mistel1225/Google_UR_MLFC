import json
import torch
from multiclassModel import T5FineTuner
from transformers import (T5Tokenizer)
from tqdm import tqdm
import textwrap
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
from tqdm import tqdm
#plt.figure(dpi=100, figsize=(150, 50))
#target file
with open('./dev.json', 'r') as f:
    data = json.load(f)
with open('./label_dict.json', 'r') as f:
    label_dict = json.load(f)
label_dict = {label:idx for idx, label in label_dict.items()}
#print(label_dict)
#prepare model and tokenizer
model_path = './output/model_nosnorkel.ckpt'
model = T5FineTuner.load_from_checkpoint(model_path, map_location='cuda:0')
tokenizer = T5Tokenizer.from_pretrained('t5-base')
pred_list = []
gt_list = []

for d in tqdm(data):
    #prepare input text
    text = 'multi-class classification: '+d['title'] + '[SEP]' + d['content']
    #for batch=1, if batch>1, use batch_encode_plus instead
    tokenizer_inputs = {}
    tokenizer_inputs["source_ids"] = tokenizer.encode_plus(
        text, max_length=300, truncation=True, return_tensors="pt"
            ).input_ids
    pred = model.predict_step(tokenizer_inputs)
    pred = tokenizer.batch_decode(pred, skip_special_tokens=True)
    pred_list.append(int(label_dict[pred[0]]))
    gt_list.append(d['label'])

with open('out.json', 'w') as f:
    json.dump(pred_list, f, indent=2)
'''
ticks = label_dict.keys()
ax = sns.heatmap(matrix, annot=True, fmt="d", cmap="YlGnBu", xticklabels=ticks, yticklabels=ticks)
plt.yticks(rotation=0)
plt.ylabel("True")
plt.xticks(rotation=270)
plt.xlabel("predict")
plt.show()
plt.savefig("out")'''
