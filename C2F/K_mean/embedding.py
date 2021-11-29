import pandas as pd
from transformers import BertModel, BertTokenizer
import torch
import numpy as np
from tqdm import tqdm
train_df = pd.read_csv('G_Community_c60/train.csv')
test_df = pd.read_csv('G_Community_c60/test.csv')
validate_df = pd.read_csv('G_Community_c60/validate.csv')

#print(len(train_df)+len(test_df)+len(validate_df))
df = pd.concat([train_df, test_df, validate_df], axis=0)
print(df)
BP_df = df[df[:]['category'] == 'Battery and Power']
print(BP_df)

#embedding_model.to('cuda:1')
embedding_model = BertModel.from_pretrained('bert-base-uncased').to('cuda:1')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
embedding_model.eval()
embedding_list = []
with torch.no_grad():
    for index, row in tqdm(BP_df.iterrows(), total=BP_df.shape[0]):
        #print(index)
        #print(row)
    
        #print(row['title']+' [SEP] ' + row['content'])
         
        tokenized_seq = tokenizer.encode_plus(row['title'] + ' [SEP] ' + row['content'], max_length=512, padding="max_length", truncation=True, return_tensors="pt")
        #print(tokenized_seq)
        #print(embedding_model(input_ids=tokenized_seq.input_ids, attention_mask=tokenized_seq.attention_mask).last_hidden_state)
        out = embedding_model(input_ids=tokenized_seq.input_ids.to('cuda:1'), attention_mask=tokenized_seq.attention_mask.to('cuda:1')).pooler_output.cpu()
        out = np.array(out)
        #print(out)
        embedding_list.append(out)
#BP_df['embedding'] = embedding_list
#print(BP_df['embedding'])
#BP_df.to_csv('BP.csv')
embedding_array = np.vstack(embedding_list)
np.save('BP.npy', embedding_array)
