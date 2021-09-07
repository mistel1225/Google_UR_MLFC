import json
import logging
import torch
import os
import argparse
import pytorch_lightning as pl
from t5multilabelModel import T5FineTuner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingCallback(pl.Callback):
    def on_validation_end(self, trainer, pl_module):
        logger.info("***** Validation results *****")
        print("val loss={}".format(trainer.callback_metrics["val_loss"]))
        '''
        if pl_module.is_logger():
            metrics = trainer.callback_metrics
            print(metrics)
            for key in sorted(metrics):
                logger.info("{} = {}\n".format(key, str(metrics[key])))
        '''
    def on_test_end(self, trainer, pl_module):
        logger.info("***** Test result ******")
        if pl_module.is_logger():
            metrics = trainer.callback_metrics

            output_test_results_file = os.path.join(pl_module.hparams.output_dir, "test_results.text")

            with open(output_test_results_file, "w") as writer:
                for key in sorted(metrics):
                    if key not in ["log", "progress_bar"]:
                        logger.info("{} = {}\n".format(key, str(metrics[key])))
                        writer.write("{} = {}\n".format(key, str(metrics[key])))


args_dict = dict(
    train_dir = "./train.json",
    val_dir = './val.json',
    output_dir = "./output",
    model_name_or_path='t5-base',
    tokenizer_name_or_path='t5-base',
    max_seq_length=512,
    learning_rate=3e-4,
    weight_decay=0.0,
    adam_epsilon=1e-8,
    warmup_steps=0,
    train_batch_size=4,
    eval_batch_size=4,
    num_train_epochs=5,
    val_every_n_epochs=1,
    limit_train_batches=False,
    gradient_accumulation_steps=32,
    n_gpu=1,
    early_stop_callback=False,
    fp_16=False,
    opt_level='01',
    max_grad_norm=1.0,
    seed=42,
    sanity_val=False
    )

if __name__ == '__main__':
    args = argparse.Namespace(**args_dict)
    checkpoint_callback =  pl.callbacks.ModelCheckpoint(
            dirpath = args.output_dir, filename='model-{val_loss}', monitor="val_loss", mode="min", save_top_k=1
    )
    
    train_params = dict(
    accumulate_grad_batches = args.gradient_accumulation_steps,
    gpus=args.n_gpu,
    max_epochs=args.num_train_epochs,
    num_sanity_val_steps = 2 if args.sanity_val else 0,
    limit_train_batches = 10 if args.limit_train_batches else 1.0,
    precision = 16 if args.fp_16 else 32,
    amp_level=args.opt_level,
    gradient_clip_val=args.max_grad_norm,
    checkpoint_callback=True,
    callbacks=[LoggingCallback(), checkpoint_callback]
    )
    model = T5FineTuner(args_dict)
    trainer = pl.Trainer(**train_params)
    trainer.fit(model)
