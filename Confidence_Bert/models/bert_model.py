import torch
from transformers import AdamW, BertTokenizer, BertModel

class PhoneCommentConfidenceClassifier(torch.nn.Module):

  def __init__(self, n_classes=7):
    super(PhoneCommentConfidenceClassifier, self).__init__()

    self.bert = BertModel.from_pretrained("bert-base-cased")
    self.classifier = torch.nn.Linear(self.bert.config.hidden_size, n_classes)
    self.confidence = torch.nn.Linear(self.bert.config.hidden_size, 1)
    self.relu = torch.nn.ReLU()
    self.softmax = torch.nn.Softmax(dim=1)
    self.sigmoid = torch.nn.Sigmoid()
    self.dropout = torch.nn.Dropout(p=0.5)
    self.n_classes = n_classes

    torch.nn.init.xavier_uniform_(self.classifier.weight)
    torch.nn.init.xavier_uniform_(self.confidence.weight)

  def forward(self, x):
    input_ids, attn_mask = x[0], x[1]
    bert_output = self.bert(input_ids=input_ids,attention_mask=attn_mask)
    hidden_state_dropout = self.dropout(bert_output.last_hidden_state[:,0,:].view(-1, 768))
    output = self.classifier(hidden_state_dropout)
    c = self.sigmoid(self.confidence(hidden_state_dropout))

    return output, c


class PhoneCommentClassifier(torch.nn.Module):

  def __init__(self, n_classes=7):
    super(PhoneCommentClassifier, self).__init__()

    self.bert = BertModel.from_pretrained("bert-base-cased")
    self.classifier = torch.nn.Linear(self.bert.config.hidden_size, n_classes)
    self.relu = torch.nn.ReLU()
    self.softmax = torch.nn.Softmax(dim=1)
    self.dropout = torch.nn.Dropout(p=0.5)
    self.n_classes = n_classes

    torch.nn.init.xavier_uniform_(self.classifier.weight)

  def forward(self, x):
    input_ids, attn_mask = x[0], x[1]
    bert_output = self.bert(input_ids=input_ids,attention_mask=attn_mask)
    hidden_state_dropout = self.dropout(bert_output.last_hidden_state[:,0,:].view(-1, 768))
    output = self.classifier(hidden_state_dropout)

    return output