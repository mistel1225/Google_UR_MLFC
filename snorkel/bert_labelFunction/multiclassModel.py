import torch
import pytorch_lightning as pl
from torch.utils.data import Dataset, DataLoader
from . import multiclassDataset
#from multiclassDataset import get_dataset
import torch
from torch import nn
from transformers import (
    AdamW,
    BertForSequenceClassification,
    BertTokenizer,
    BertConfig,
    get_linear_schedule_with_warmup
        )
from sklearn.metrics import f1_score, accuracy_score


class BertFineTuner(pl.LightningModule):
    def __init__(self, hparams):
        super().__init__()
        self.hparams.update(hparams)
        self.save_hyperparameters()
        config = BertConfig()
        config.num_labels = hparams['num_labels']
        self.model = BertForSequenceClassification.from_pretrained(self.hparams.model_name_or_path, config=config)
        self.tokenizer = BertTokenizer.from_pretrained(self.hparams.tokenizer_name_or_path)
    def forward(self, batch):
        return self.model(batch["source_ids"])
    def predict_step(self, batch, *args, **kwargs):
        return self(batch)
    def _step(self, batch):
        labels = batch["target_ids"]
        output = self.model(
            input_ids = batch["source_ids"],
            attention_mask = batch["source_mask"],
            labels = labels,
        )
        loss = output.loss
        return loss
    def training_step(self, batch, batch_idx):
        loss = self._step(batch)
        self.log('train_loss', loss, prog_bar=False, logger=True)
        return loss
    def validation_step(self, batch, batch_idx):
        loss = self._step(batch)
        self.log('val_loss', loss, prog_bar=False, logger=True)
        output = self(batch)
        return {'pred': output, 'gt': batch['target_ids']}
    def validation_epoch_end(self, val_step_outputs):
        gt_list = []
        pred_list = []
        softmax = nn.Softmax(dim=1)
        for out in val_step_outputs:
            pred = out['pred']['logits']
            gt = out['gt']
            pred = torch.argmax(softmax(pred), dim=1)
            for l1, l2 in zip(pred, gt):
                pred_list.append(l1.cpu())
                gt_list.append(l2.cpu())
        acc = accuracy_score(gt_list, pred_list)
        f1_macro = f1_score(gt_list, pred_list, average='macro')
        f1_micro = f1_score(gt_list, pred_list, average='micro')
        self.log('val_acc', acc, prog_bar=False, logger=True)
        self.log('val_f1_micro', f1_micro, prog_bar=False, logger=True)
        self.log('val_f1_macro', f1_macro, prog_bar=False, logger=True)
    def configure_optimizers(self):
        model = self.model
        no_decay = ["bias", "LayerNorm.weight"]
        optimizer_ground_parameters = [
                {
                    "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
                    "weight": self.hparams.weight_decay,
                    },
                {
                    "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
                    "weight_decay": 0.0,
                    },
                ]
        optimizer = AdamW(optimizer_ground_parameters, lr=self.hparams.learning_rate, eps=self.hparams.adam_epsilon)
        self.opt = optimizer
        t_total = (
                ((self.hparams.num_train_size)//(self.hparams.train_batch_size) // (self.hparams.gradient_accumulation_steps))
                * float(self.hparams.num_train_epochs)
                )
        scheduler = get_linear_schedule_with_warmup(self.opt, num_warmup_steps=self.hparams.warmup_steps, num_training_steps=t_total)
        self.lr_scheduler = scheduler
        return [optimizer], [scheduler]
    def train_dataloader(self):
        train_dataset = multiclassDataset.get_dataset(tokenizer=self.tokenizer, mode='train', args=self.hparams)
        return DataLoader(train_dataset, batch_size=self.hparams.train_batch_size, drop_last=False, shuffle=True, num_workers=8)
    def val_dataloader(self):
        val_dataset = multiclassDataset.get_dataset(tokenizer=self.tokenizer, mode='test', args=self.hparams)
        self.val_dataset = val_dataset
        return DataLoader(val_dataset, batch_size=self.hparams.eval_batch_size, num_workers=8)
