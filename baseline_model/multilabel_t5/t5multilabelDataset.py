import json
import os
from torch.utils.data import Dataset
import torch
import pytorch_lightning as pl
from tqdm import tqdm
from transformers import (T5Tokenizer)

class multilabelDataset():
    def __init__(self, tokenizer, data_dir, max_len=512):
        self.max_len = max_len
        self.tokenizer = tokenizer
        self.data_dir = data_dir
        self.inputs = []
        self.targets = []
        self._build()
    def __len__(self):
        return len(self.inputs)
    def __getitem__(self, index):
        source_ids = self.inputs[index]["input_ids"].squeeze()
        target_ids = self.targets[index]["input_ids"].squeeze()

        src_mask = self.inputs[index]["attention_mask"].squeeze()
        target_mask = self.targets[index]["attention_mask"].squeeze()
        return {"source_ids": source_ids, "source_mask": src_mask, "target_ids": target_ids, "target_mask": target_mask}
    def _build(self):
        self._build_examples_from_files(self.data_dir)
    def _build_examples_from_files(self, f):
        with open(f, 'r') as reader:
            data = json.load(reader)
        
        for k, d in tqdm(data.items()):
            _ = "multi classification: "+d['data']['title']+' '+ d['data']['content']
            _ = _.replace('\n', '')
            tokenizer_inputs = self.tokenizer.batch_encode_plus(
                [_], max_length = self.max_len, padding='max_length',
                truncation=True, return_tensors="pt"
            )
            self.inputs.append(tokenizer_inputs)
            _ = d['label']
            _ = ','.join(str(l) for l in _)
            tokenizer_targets = self.tokenizer.batch_encode_plus(
                [_], max_length=32, padding='max_length', truncation=True, return_tensors="pt"
            )
            self.targets.append(tokenizer_targets)
        
def get_dataset(tokenizer, data_dir, args):
    return multilabelDataset(tokenizer=tokenizer, data_dir=data_dir, max_len=args.max_seq_length)

