import json
from sklearn.metrics import confusion_matrix
import numpy as np
with open('8label_snorkel.json', 'r') as f:
    pred_list = json.load(f)
with open('dev.json', 'r') as f:
    gt = json.load(f)
gt_list = []
for d in gt:
    gt_list.append(d['label'])
print(confusion_matrix(np.array(pred_list), np.array(gt_list)))
