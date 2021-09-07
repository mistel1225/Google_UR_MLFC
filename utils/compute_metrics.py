import json
import numpy as np
from pathlib import Path
from sklearn.metrics import f1_score, accuracy_score
from typing import List, Tuple, Dict
import os
#INPUT: prediction and ground-truth(didn't need to convert it to one-hot format)
# [['label1', 'label2'], ['label1', 'label3', 'label4']]...
#OUTPUT: score for f1_score_micro, f1_score_macro, accuracy_acore


file_path = Path.resolve(Path(os.path.dirname(__file__)))/Path('../data/data_label_replace.json')
file_path = Path.resolve(file_path)

class metrics():
    def __init__(self):
        with open(file_path, 'r') as f:
            label_file = json.load(f)
        idx = 0
        self.label_idx_dict={}
        self.one_hot_truth = []
        self.one_hot_pred = []
        for root, sublabel_list in label_file.items():
            for l in sublabel_list:
                self.label_idx_dict[l] = idx
                idx += 1
        self.label_num = idx+1
    def add_batch(self, pred: List[List[str]], truth: List[List[str]]) -> None:
        for p in pred:
            pred_one_hot_array = np.zeros(self.label_num)
            for l in p:
                try:
                    pred_one_hot_array[self.label_idx_dict[l.lower()]] = 1
                except:
                    print("{} is not in the label list".format(l.lower()))
                    exit(-1)
            self.one_hot_pred.append(pred_one_hot_array.tolist())
        for t in truth:
            truth_one_hot_array = np.zeros(self.label_num)
            for l in t:
                try:
                    truth_one_hot_array[self.label_idx_dict[l.lower()]] = 1
                except:
                    print("{} is not in the label list".format(l.lower()))
                    exit(-1)
            self.one_hot_truth.append(truth_one_hot_array.tolist())
    def compute_score(self) -> Dict:
        f1_micro = f1_score(y_true=self.one_hot_truth, y_pred=self.one_hot_pred, average="micro")
        f1_macro = f1_score(y_true=self.one_hot_truth, y_pred=self.one_hot_pred, average="macro")
        acc = accuracy_score(y_true=self.one_hot_truth, y_pred=self.one_hot_pred)
        print("===============")
        print("f1 micro score: {}".format(f1_micro))
        print("f1 macro score: {}".format(f1_macro))
        print("accuracy score: {}".format(acc))
        return {'f1_micro': f1_micro, 'f1_macro': f1_macro, 'accuracy': acc}
if __name__ == '__main__':
    m = metrics()
