from abc import abstractmethod

import torch
from collections import defaultdict

import scanpy as sc
from scarchest.utils.monitor import EarlyStopping


class MetaTrainer:
    def __init__(self,
                 model,
                 adata: sc.AnnData,
                 task_key: str,
                 clip_value: float = 0.0,
                 weight_decay: float = 0.04,
                 train_frac: float = 0.9,
                 freeze_expression_input: bool = False,
                 early_stopping_kwargs: dict = None,
                 batch_size: int = 512,
                 n_workers: int = 0,
                 lr_gamma=1.0,
                 lr_step_size=100,
                 eps=0.01,
                 **kwargs):

        self.adata = adata
        self.task_key = task_key
        self.clip_value = clip_value
        self.weight_decay = weight_decay
        self.train_frac = train_frac
        self.freeze_expression_input = freeze_expression_input
        early_stopping_kwargs = (early_stopping_kwargs if early_stopping_kwargs else dict())
        self.batch_size = batch_size
        self.n_workers = n_workers
        self.lr_gamma = lr_gamma
        self.lr_step_size = lr_step_size
        self.eps = eps
        self.seed = kwargs.pop("seed", 2020)
        self.use_stratified_sampling = kwargs.pop("use_stratified_sampling", True)
        self.use_early_stopping = kwargs.pop("use_early_stopping", True)
        self.monitor = kwargs.pop("monitor", True)
        self.use_stratified_split = kwargs.pop("use_stratified_split", False)
        self.learning_rate = kwargs.pop('lr', 1e-3)
        self.pre_train_learning_rate = kwargs.pop('pre_train_lr', 1e-3)

        self.early_stopping = EarlyStopping(**early_stopping_kwargs)
        torch.manual_seed(self.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(self.seed)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = model.to(self.device)
        self.model.device = self.device

        self.iter_logs = defaultdict(list)
        self.logs = defaultdict(list)
        self.training_time = 0.0

    @abstractmethod
    def on_training_begin(self):
        pass

    @abstractmethod
    def on_epoch_begin(self):
        pass

    @abstractmethod
    def on_iteration_begin(self):
        pass

    @abstractmethod
    def on_epoch(self):
        pass

    @abstractmethod
    def on_iteration_end(self):
        pass

    @abstractmethod
    def on_epoch_end(self):
        pass

    @abstractmethod
    def check_early_stop(self):
        pass
        # Calculate Early Stopping and best state
        # early_stopping_metric = self.early_stopping.early_stopping_metric
        # save_best_state_metric = self.early_stopping.save_best_state_metric
        # if save_best_state_metric is not None and self.early_stopping.update_state(
        #         self.logs[save_best_state_metric][-1]):
        #     self.best_state_dict = self.model.state_dict()
        #     self.best_epoch = self.epoch
        # continue_training = True
        # if early_stopping_metric is not None and not self.early_stopping.step(self.logs[early_stopping_metric][-1]):
        #     continue_training = False
        #     return continue_training
        #
        # # Update Learning Rate
        # self.lr_scheduler.step()
        # return continue_training

    @abstractmethod
    def on_training_end(self):
        pass

    @torch.no_grad()
    def validate(self):
        self.model.eval()
        # Calculate Validation Losses
        for val_iter, batch_data in enumerate(self.dataloader_valid):
            for key1 in batch_data:
                for key2, batch in batch_data[key1].items():
                    batch_data[key1][key2] = batch.to(self.device)

            val_loss = self.loss(**batch_data)

        # Get Validation Logs
        for key in self.iter_logs:
            if "loss" in key:
                self.logs["val_" + key].append(
                    sum(self.iter_logs[key][-self.val_iters_per_epoch:]) / self.val_iters_per_epoch)

        self.model.train()

    @abstractmethod
    def train(self,
              n_epochs=400,
              ):
        pass

    @abstractmethod
    def loss(self, **kwargs):
        pass
