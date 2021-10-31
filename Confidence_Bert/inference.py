import pandas as pd
import numpy as np
import argparse
import torch
import os

from torch.utils.data import DataLoader
from transformers import BertTokenizer
from utils.datasets import GoogleCommunityDataset
from models.bert_model import PhoneCommentClassifier, PhoneCommentConfidenceClassifier
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix

from tqdm.auto import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"

dataset_options = ['G_Community', 'G_Community_c60']
model_options = ['BERT', 'Confidence_BERT']

parser = argparse.ArgumentParser(description='Text Classification for Phone Comment Data')
parser.add_argument('--train_dataset', default='G_Community', choices=dataset_options)
parser.add_argument('--model', default='BERT', choices=model_options)
parser.add_argument('--inference_data_path', default=None)

args = parser.parse_args()

def test(loader, model_name):
    model.eval()    # Change model to 'eval' mode (BN uses moving mean/var).

    true_label = []
    pred_label = []
    confidence = []

    with torch.no_grad():
        for data in tqdm(loader):
            data = [v.to(device) for k, v in data.items()]

            if model_name == 'BERT':
                pred = model(data)
            elif model_name == 'Confidence_BERT':
                pred, conf = model(data)
            pred = F.softmax(pred, dim=-1)
            pred_value, pred = torch.max(pred.data, 1)
            pred_label.extend(pred.cpu().numpy())

            if model_name == 'Confidence_BERT':
                confidence.extend(conf.cpu().numpy())

            if len(data) > 2: #data has label
                labels_onehot = data[2]
                label_idx = torch.argmax(labels_onehot,dim=1)
                true_label.extend(label_idx.cpu().numpy())

    return true_label, pred_label, confidence


def evaluate(true_label, pred_label):
    acc = accuracy_score(true_label, pred_label)
    f1_macro = f1_score(true_label, pred_label, average='macro')
    precision_matrix = precision_score(true_label, pred_label, average=None)
    recall_matrix = recall_score(true_label, pred_label, average=None)
    confusion = confusion_matrix(true_label, pred_label)

    print("test acurracy: {:.4f}, test macro f1 score: {:.4f}".format(acc, f1_macro))
    print("precision score\n{}".format(precision_matrix))
    print("recall score\n{}".format(recall_matrix))
    print("confusion matrix\n{}".format(confusion))

tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

if not args.inference_data_path:
    data_set = GoogleCommunityDataset('train', "./data/" + args.train_dataset + "/test.csv", tokenizer, 512)
else:
    data_set = GoogleCommunityDataset('test', args.inference_data_path, tokenizer, 512)

data_loader = DataLoader(data_set, batch_size=1, shuffle=False, pin_memory=True)

if args.model == 'BERT':
    model = PhoneCommentClassifier(7).to(device)
elif args.model == 'Confidence_BERT':
    model = PhoneCommentConfidenceClassifier(7).to(device)

filename = '{}_{}'.format(args.model, args.train_dataset)

model.load_state_dict(torch.load('checkpoints/' + filename + '.pt'))

model.eval()
print("Start Inference ...")

true_label, pred_label, confidence = test(data_loader, args.model)
if true_label:
    evaluate(true_label, pred_label)

label_to_text = {
  0: "Battery and Power",
  1: "Camera",
  2: "Connectivity, Network, Bluetooth",
  3: "Contacts, Calls, Voicemail",
  4: "Google Assistant and Voice Actions",
  5: "Homescreen and Launcher",
  6: "Setting up and Personalizing your Device",
}

if args.inference_data_path:
    df = pd.read_csv(args.inference_data_path)
    df['category'] = [label_to_text[k] for k in pred_label]
    if args.model == "Confidence_BERT":
        df['confidence'] = [conf[0] for conf in confidence]
    df.to_csv("./results/"+args.model+"_result_"+os.path.basename(args.inference_data_path),index=None)

