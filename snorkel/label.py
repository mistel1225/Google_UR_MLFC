from snorkel.labeling import labeling_function, PandasLFApplier
from snorkel.labeling.model import LabelModel
import json
import torch
from torch import nn
from bert_labelFunction.multiclassModel import BertFineTuner
from t5_labelFunction.multiclassModel import T5FineTuner
from transformers import (BertTokenizer, T5Tokenizer)
from tqdm import tqdm
import textwrap
import pandas as pd
from io import StringIO
import tomotopy as tp
import gensim
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *

ABSTAIN = -1
BATTERY = 0
CAMERA = 1
NETWORK = 2
CALL = 3
ASSISTANT = 4
HOMESCREEN = 5
SETTING = 6

keywords = {
    0 : ["drain", "swell", "battery"],
    1 : ["lense", "night sight", "astrophotography", "camera"],
    2 : ["wifi", "wi-fi", "sim card", "esim", "4g", "lte", "5g"],
    3 : ["voicemail", "screen call", "calls"],
    4 : ["google assist", "virtual assist", "ok google", "assistant"],
    5 : ["homescreen", "launcher"],
    6 : ["setup", "how to"]
}

#target file
data = pd.read_csv("./../data/raw_data/samsungdata.csv")

nltk.download('wordnet')
stemmer = PorterStemmer()
plda_model = tp.PLDAModel().load("./plda_labelFunction/output/plda_model.model")

#prepare model and tokenizer
bert_model_path = './bert_labelFunction/output/model.ckpt'
bert_model = BertFineTuner.load_from_checkpoint(bert_model_path, map_location='cuda:0')
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

t5_model_path = './t5_labelFunction/output/model.ckpt'
t5_model = T5FineTuner.load_from_checkpoint(t5_model_path, map_location='cuda:0')
t5_tokenizer = T5Tokenizer.from_pretrained('t5-base')

with open('./t5_labelFunction/label_dict.json', 'r') as f:
    label_dict = json.load(f)

softmax = nn.Softmax(dim=1)

@labeling_function()
def vocab_based(d):
    text = d['title'] + ' ' + d['content']
    text = text.lower()
    cnt = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        vocab_list = keywords[i]
        for v in vocab_list:
            if v in text:
                cnt[i] = 1
                break
    if sum(cnt) > 1 or sum(cnt) == 0:
        return ABSTAIN
    else:
        for i in range(7):
            if cnt[i] == 1:
                return i

@labeling_function()
def plda_based(x):
    def lemmatize_stemming(text):
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
    def preprocess(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(lemmatize_stemming(token))
        return result

    doc = preprocess(x.title + ' ' + x.content)
    stopwords = ['googl', 'pixel', 'tri', 'phone', 'work', 'issu', 'help', 'time',
               'devic', 'problem', 'like', 'go', 'want', 'know', 'need', 'thank',
               'happen', 'get', 'come']
    for word in stopwords:
        while word in doc:
            doc.remove(word)

    if doc == []:
        return -1

    doc = plda_model.make_doc(doc)
    result = plda_model.infer(doc=doc)[0]
    return int(max(zip(plda_model.topic_label_dict, result),key=lambda x:x[1])[0])

@labeling_function()
def bert_based(d):
    #prepare input text
    text = '[CLS] '+d['title'] + '[SEP]' + d['content']
    #for batch=1, if batch>1, use batch_encode_plus instead
    tokenizer_inputs = {}
    tokenizer_inputs["source_ids"] = bert_tokenizer.encode_plus(
        text, max_length=300, truncation=True, return_tensors="pt"
            ).input_ids
    pred = bert_model.predict_step(tokenizer_inputs).logits
    pred = torch.argmax(softmax(pred), dim=1)
    return int(pred) if int(pred) != 7 else -1

@labeling_function()
def t5_based(d):
    #prepare input text
    text = 'multi-class classification: '+d['title'] + '[SEP]' + d['content']
    #for batch=1, if batch>1, use batch_encode_plus instead
    tokenizer_inputs = {}
    tokenizer_inputs["source_ids"] = t5_tokenizer.encode_plus(
        text, max_length=300, truncation=True, return_tensors="pt"
            ).input_ids
    pred = t5_model.predict_step(tokenizer_inputs)
    pred = t5_tokenizer.batch_decode(pred, skip_special_tokens=True)
    try:
        return label_dict[pred[0]] if label_dict[pred[0]] !=7 else -1
    except:
        return -1

lfs = [vocab_based, plda_based, bert_based, t5_based]
applier = PandasLFApplier(lfs=lfs)
L_train = applier.apply(df=data)

label_model = LabelModel(cardinality=7)
label_model.fit(L_train=L_train, n_epochs=500,lr_scheduler='linear',log_freq=100, seed=123)
preds_train = label_model.predict(L=L_train)

data['label'] = preds_train
data.to_csv("output.csv",index=None)
