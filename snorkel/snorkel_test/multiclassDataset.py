from datasets import load_dataset
from torch.utils.data import Dataset
import torch
import pytorch_lightning as pl
from tqdm import tqdm
from transformers import T5Tokenizer
import pandas as pd
import json
class multiclassDataset(Dataset):
    def __init__(self, tokenizer, mode, max_len=512):
        self.max_len = max_len
        self.tokenizer = tokenizer
        self.mode = mode
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
        with open('label_dict.json', 'r') as f:
            self.idx_label_mapping = json.load(f)
        self.idx_label_mapping = {int(idx):label for idx, label in self.idx_label_mapping.items()}
        self.label_idx_mapping = {label:idx for idx, label in self.idx_label_mapping.items()}
        if self.mode == "train":
            with open('new_train.json', 'r') as f:
                self.data = json.load(f)
        elif self.mode == "test":
            with open('dev.json', 'r') as f:
                self.data = json.load(f)
        for d in tqdm(self.data, total=len(self.data)):
            _ = "multi-class classification: "+ d['title'] + '[SEP]' + d['content']
            tokenizer_inputs = self.tokenizer.batch_encode_plus(
                [_], max_length = self.max_len, padding="max_length", truncation=True,
                return_tensors="pt"
                    )
            self.inputs.append(tokenizer_inputs)
            _ = d['label']
            _ = self.idx_label_mapping[_]
            tokenizer_targets = self.tokenizer.batch_encode_plus(
                [_], max_length=10, padding="max_length", truncation=True, return_tensors="pt"
                    )
            self.targets.append(tokenizer_targets)

def get_dataset(tokenizer, mode, args):
    return multiclassDataset(tokenizer=tokenizer, mode=mode, max_len=args.max_seq_length)


