import numpy as np
import random
import argparse
import torch

from torch.utils.data import DataLoader
from transformers import AdamW, BertTokenizer
from utils.datasets import GoogleCommunityDataset
from models.bert_model import PhoneCommentClassifier, PhoneCommentConfidenceClassifier
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, f1_score

from tqdm.auto import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"

dataset_options = ['G_Community', 'G_Community_c60']
model_options = ['BERT', 'Confidence_BERT']

parser = argparse.ArgumentParser(description='Text Classification for Phone Comment Data')
parser.add_argument('--dataset', default='G_Community', choices=dataset_options)
parser.add_argument('--model', default='BERT', choices=model_options)
parser.add_argument('--batch_size', type=int, default=4)
parser.add_argument('--epochs', type=int, default=5)
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--learning_rate', type=float, default=5e-5)
parser.add_argument('--weight_decay', type=float, default=1e-4)
parser.add_argument('--lmbda', type=float, default=0.1)
parser.add_argument('--beta', type=float, default=0.3)

args = parser.parse_args()

# Fix random seed for reproducibility
def same_seeds(seed):
	  torch.manual_seed(seed)
	  if torch.cuda.is_available():
		    torch.cuda.manual_seed(seed)
		    torch.cuda.manual_seed_all(seed)
	  np.random.seed(seed)
	  random.seed(seed)
	  torch.backends.cudnn.benchmark = False
	  torch.backends.cudnn.deterministic = True

def test(loader, model_name):
    model.eval() 

    probability = []
    true_label = []
    pred_label = []
    confidence = []

    with torch.no_grad():
        for data in tqdm(loader):
            data = [v.to(device) for k, v in data.items()]

            labels_onehot = data[2]
            if model_name == 'BERT':
                pred = model(data)
            elif model_name == 'Confidence_BERT':
                pred, conf = model(data)
            pred = F.softmax(pred, dim=-1)

            pred_value, pred = torch.max(pred.data, 1)
            label_idx = torch.argmax(labels_onehot,dim=1)

            probability.extend(pred_value.cpu().numpy())
            true_label.extend(label_idx.cpu().numpy())
            pred_label.extend(pred.cpu().numpy())

    probability = np.array(probability)
    f1_macro = f1_score(true_label, pred_label, average='macro')
    val_acc = accuracy_score(true_label, pred_label)

    if model_name == 'Confidence_BERT':
        confidence = np.array(confidence)
        conf_min = np.min(confidence)
        conf_max = np.max(confidence)
        conf_avg = np.mean(confidence)

    model.train()
    if model_name == 'BERT':
        return val_acc, f1_macro
    elif model_name == 'Confidence_BERT':
        return val_acc, f1_macro, conf_min, conf_max, conf_avg


same_seeds(args.seed)

tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

train_set = GoogleCommunityDataset('train', "./data/" + args.dataset + "/train.csv", tokenizer, 512)
val_set = GoogleCommunityDataset('train', "./data/" + args.dataset + "/validate.csv", tokenizer, 512)

train_loader = DataLoader(train_set, batch_size=4, shuffle=True, pin_memory=True)
train_loader_t = DataLoader(train_set, batch_size=1, shuffle=True, pin_memory=True)
val_loader = DataLoader(val_set, batch_size=1, shuffle=False, pin_memory=True)

if args.model == 'BERT':
    model = PhoneCommentClassifier(7).to(device)
elif args.model == 'Confidence_BERT':
    model = PhoneCommentConfidenceClassifier(7).to(device)

optimizer = AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
prediction_criterion = torch.nn.NLLLoss()
lmbda = args.lmbda

model.train()
print("Start Training ...")

for epoch in range(args.epochs):
    print('epoch', str(epoch))
    correct_count = 0.
    total = 0.
    xentropy_loss_avg = 0.
    best_val_acc = 0.
    if args.model == 'Confidence_BERT':
        confidence_loss_avg = 0.

    progress_bar = tqdm(train_loader)
    for i, data in enumerate(progress_bar):

        data = [v.to(device) for _, v in data.items()]
        labels_onehot = data[2]

        if args.model == 'BERT':
            hidden_state = model(data)
        elif args.model == 'Confidence_BERT':
            hidden_state, confidence = model(data)

        pred_original = torch.nn.functional.softmax(hidden_state, dim=-1)

        eps = 1e-12
        pred_original = torch.clamp(pred_original, 0. + eps, 1. - eps)
        
        if args.model == 'BERT':
            pred_new = torch.log(pred_original)
        elif args.model == 'Confidence_BERT':
            b = torch.bernoulli(torch.Tensor(confidence.size()).uniform_(0, 1)).to(device)
            conf = confidence * b + (1 - b)
            pred_new = pred_original * conf.expand_as(pred_original) + labels_onehot * (1 - conf.expand_as(labels_onehot))
            pred_new = torch.log(pred_new)

        label_idx = torch.argmax(labels_onehot,dim=1)

        if args.model == 'BERT':
            xentropy_loss = prediction_criterion(pred_new, label_idx)
            xentropy_loss.backward()
        elif args.model == 'Confidence_BERT':
            xentropy_loss = prediction_criterion(pred_new, label_idx)
            confidence_loss = torch.mean(-torch.log(confidence))

            total_loss = xentropy_loss + (lmbda * confidence_loss)

            if args.beta > confidence_loss:
                lmbda = lmbda / 1.01
            elif args.beta <= confidence_loss:
                lmbda = lmbda / 0.99

            total_loss.backward()
        
        optimizer.step()
        optimizer.zero_grad()

        xentropy_loss_avg += xentropy_loss
        if args.model == 'Confidence_BERT':
            confidence_loss_avg += confidence_loss

        pred_idx = torch.max(pred_original.data, 1)[1]
        total += labels_onehot.size(0)
        correct_count += (pred_idx == label_idx).sum()
        accuracy = correct_count / total

        if args.model == 'BERT':
            progress_bar.set_postfix(
                loss_x='%.3f' % (xentropy_loss_avg / (i + 1)),
                acc='%.3f' % accuracy)
        elif args.model == 'Confidence_BERT':
            progress_bar.set_postfix(
                loss_x='%.3f' % (xentropy_loss_avg / (i + 1)),
                loss_c='%.3f' % (confidence_loss_avg / (i + 1)),
                lmbdda='%.3f' % lmbda,
                acc='%.3f' % accuracy)

    if args.model == 'BERT':
        train_acc, train_f1_macro = test(train_loader_t, args.model)
        tqdm.write('train_acc: %.3f, train_f1_macro: %.3f' % (train_acc, train_f1_macro))
        val_acc, val_f1_macro = test(val_loader, args.model)
        tqdm.write('val_acc: %.3f, val_f1_macro: %.3f' % (val_acc, val_f1_macro))
    elif args.model == 'Confidence_BERT':
        train_acc, train_f1_macro, conf_min, conf_max, conf_avg = test(train_loader_t, args.model)
        tqdm.write('train_acc: %.3f, train_f1_macro: %.3f, conf_min: %.3f, conf_max: %.3f, conf_avg: %.3f' % (train_acc, train_f1_macro, conf_min, conf_max, conf_avg))
        val_acc, val_f1_macro, conf_min, conf_max, conf_avg = test(val_loader, args.model)
        tqdm.write('val_acc: %.3f, val_f1_macro: %.3f, conf_min: %.3f, conf_max: %.3f, conf_avg: %.3f' % (val_acc, val_f1_macro, conf_min, conf_max, conf_avg))

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        filename = '{}_{}'.format(args.model, args.dataset)
        torch.save(model.state_dict(), 'checkpoints/' + filename + '.pt')