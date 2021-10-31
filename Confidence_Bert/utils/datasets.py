from torch.utils.data import Dataset
import pandas as pd
from sklearn.preprocessing import LabelBinarizer
import torch

class GoogleCommunityDataset(Dataset):
    def __init__(self, split, file_path, tokenizer, max_len):
        self.split = split
        self.file_path = file_path
        self.tokenizer = tokenizer
        self.max_len = max_len

        assert type(file_path) == str
        df = pd.read_csv(file_path)
        df = df.dropna()
        x, y = [], []
        for _, doc in df.iterrows():
            context = doc['title'] + " [SEP] " + doc['content']
            x.append(context)
            if self.split == 'train':
              y.append(doc['category'])

        self.text = x

        if self.split == 'train':
          #Category to one-hot vector 
          mlb = LabelBinarizer()
          y_transform = mlb.fit_transform(y)

          self.labels = y_transform
        
    def __len__(self):
        return len(self.text)
    
    def __getitem__(self, item_idx):
        text = self.text[item_idx]
        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            max_length= self.max_len,
            padding = 'max_length',
            return_token_type_ids= False,
            return_attention_mask= True,
            truncation=True,
            return_tensors = 'pt'
          )
        
        input_ids = inputs['input_ids'].flatten()
        attn_mask = inputs['attention_mask'].flatten()
        if self.split == 'train':
          label = torch.tensor(self.labels[item_idx],dtype= torch.long)
                
          return {
            'input_ids': input_ids ,
            'attention_mask': attn_mask,
            'label':label
            }

        elif self.split == 'test':
          return {
            'input_ids': input_ids ,
            'attention_mask': attn_mask,
            }