import json
import logging
import torch
import os
import argparse
import pytorch_lightning as pl
from pytorch_lightning import loggers as pl_loggers
from multiclassModel import BertFineTuner
import pandas as pd


num_train_size = 15000
args_dict = dict(
    output_dir = './output',
    model_name_or_path='bert-base-uncased',
    tokenizer_name_or_path='bert-base-uncased',
    max_seq_length=300,
    learning_rate=3e-4,
    weight_decay=0.0,
    adam_epsilon=1e-8,
    warmup_steps=0,
    train_batch_size=16,
    eval_batch_size=4,
    num_train_epochs=2,
    val_check_interval=0.25,
    limit_train_batches=False,
    gradient_accumulation_steps=32,
    n_gpu=1,
    early_stop_callback=False,
    fp_16=False,
    opt_level='01',
    max_grad_norm=1.0,
    seed=42,
    sanity_val=True,
    num_train_size = num_train_size,
    num_labels = 8
        )
if __name__ == '__main__':
    args = argparse.Namespace(**args_dict)
    checkpoint_callback = pl.callbacks.ModelCheckpoint(
        dirpath = args.output_dir, filename='model-{val_loss}', monitor="val_loss", mode="min", save_top_k=1
    )
    tb_logger = pl_loggers.TensorBoardLogger(name="finetune", save_dir="logs/", default_hp_metric=False)
    train_params = dict(
    accumulate_grad_batches = args.gradient_accumulation_steps,
    gpus=args.n_gpu,
    max_epochs = args.num_train_epochs,
    num_sanity_val_steps = 2 if args.sanity_val else 0,
    limit_train_batches = 10 if args.limit_train_batches else 1.0,
    precision = 16 if args.fp_16 else 32,
    amp_level = args.opt_level,
    gradient_clip_val = args.max_grad_norm,
    checkpoint_callback=True,
    callbacks=[checkpoint_callback, pl.callbacks.EarlyStopping(monitor="val_loss")],
    logger = tb_logger,
    log_every_n_steps=5,
    flush_logs_every_n_steps=10,
    val_check_interval = args.val_check_interval,
    )

    model = BertFineTuner(args_dict)
    trainer = pl.Trainer(**train_params)
    trainer.fit(model)
