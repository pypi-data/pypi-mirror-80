from abc import abstractmethod

import torch
import torch.nn as nn
from collections import defaultdict
import numpy as np
import time
from torch.utils.data import DataLoader
from torch.utils.data import WeightedRandomSampler

from scarchest.utils.monitor import EarlyStopping
from ._utils import make_dataset, custom_collate, print_progress


class Trainer:
    def __init__(self,
                 model,
                 adata,
                 condition_key: str = None,
                 cell_type_key: str = None,
                 size_factor_key: str = None,
                 is_label_key: str = None,
                 clip_value: float = 0.0,
                 weight_decay: float = 0.04,
                 train_frac: float = 0.9,
                 early_stopping_kwargs: dict = None,
                 batch_size: int = 512,
                 n_samples: int = None,
                 n_workers: int = 0,
                 **kwargs):
        self.adata = adata
        self.condition_key = condition_key
        self.cell_type_key = cell_type_key
        self.size_factor_key = size_factor_key
        self.is_label_key = is_label_key
        self.clip_value = clip_value
        self.weight_decay = weight_decay
        self.train_frac = train_frac
        early_stopping_kwargs = (early_stopping_kwargs if early_stopping_kwargs else dict())
        self.batch_size = batch_size
        self.n_workers = n_workers
        self.seed = kwargs.pop("seed", 2020)
        self.use_stratified_sampling = kwargs.pop("use_stratified_sampling", True)
        self.use_early_stopping = kwargs.pop("use_early_stopping", True)
        self.monitor = kwargs.pop("monitor", True)
        self.use_stratified_split = kwargs.pop("use_stratified_split", False)

        self.early_stopping = EarlyStopping(**early_stopping_kwargs)
        torch.manual_seed(self.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(self.seed)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = model.to(self.device)
        self.model.device = self.device

        self.epoch = -1
        self.iter = 0
        self.best_epoch = None
        self.best_state_dict = None
        self.current_loss = None
        self.previous_loss_was_nan = False
        self.nan_counter = 0
        self.optimizer = None
        self.lr_scheduler = None
        self.training_time = 0

        self.train_data = None
        self.valid_data = None
        self.sampler = None
        self.dataloader_train = None
        self.dataloader_valid = None
        self.n_samples = n_samples
        self.iters_per_epoch = None
        self.val_iters_per_epoch = None

        self.iter_logs = defaultdict(list)
        self.logs = defaultdict(list)

    def on_training_begin(self):
        """
        Initializes Train-/Test Data and Dataloaders with custom_collate and WeightedRandomSampler for Trainloader.
        Returns:

        """
        # Create Train/Valid AnnotatetDataset objects
        self.train_data, self.valid_data = make_dataset(self.adata,
                                                        train_frac=self.train_frac,
                                                        use_stratified_split=self.use_stratified_split,
                                                        condition_key=self.condition_key,
                                                        cell_type_key=self.cell_type_key,
                                                        size_factor_key=self.size_factor_key,
                                                        condition_encoder=self.model.condition_encoder,
                                                        cell_type_encoder=None
                                                        )
        print("Traindata:", len(self.train_data))
        for i in range(len(self.train_data.unique_conditions)):
            print("Condition:", i, "Counts in TrainData:", np.count_nonzero(self.train_data.conditions == i))

        if self.n_samples is None or self.n_samples > len(self.train_data):
            self.n_samples = len(self.train_data)
        self.iters_per_epoch = int(np.ceil(self.n_samples / self.batch_size))

        if self.use_stratified_sampling:
            # Create Sampler and Dataloaders
            stratifier_weights = torch.tensor(self.train_data.stratifier_weights, device=self.device)

            self.sampler = WeightedRandomSampler(stratifier_weights,
                                                 num_samples=self.n_samples,
                                                 replacement=True)
            self.dataloader_train = torch.utils.data.DataLoader(dataset=self.train_data,
                                                                batch_size=self.batch_size,
                                                                sampler=self.sampler,
                                                                collate_fn=custom_collate,
                                                                num_workers=self.n_workers)
        else:
            self.dataloader_train = torch.utils.data.DataLoader(dataset=self.train_data,
                                                                batch_size=self.batch_size,
                                                                shuffle=True,
                                                                collate_fn=custom_collate,
                                                                num_workers=self.n_workers)
        if self.valid_data is not None:
            print("Valid_data", len(self.valid_data))
            for i in range(len(self.valid_data.unique_conditions)):
                print("Condition:", i, "Counts in TrainData:", np.count_nonzero(self.valid_data.conditions == i))

            val_batch_size = self.batch_size
            if self.batch_size > len(self.valid_data):
                val_batch_size = len(self.valid_data)
            self.val_iters_per_epoch = int(np.ceil(len(self.valid_data) / self.batch_size))
            self.dataloader_valid = torch.utils.data.DataLoader(dataset=self.valid_data,
                                                                batch_size=val_batch_size,
                                                                shuffle=True,
                                                                collate_fn=custom_collate,
                                                                num_workers=self.n_workers)

    @abstractmethod
    def on_epoch_begin(self):
        pass

    @abstractmethod
    def loss(self, **kwargs):
        pass

    @abstractmethod
    def on_iteration_begin(self):
        pass

    def on_iteration(self, batch_data):
        # Dont update any weight on first layers except condition weights
        if self.model.freeze:
            for name, module in self.model.named_modules():
                if isinstance(module, nn.BatchNorm1d):
                    if not module.weight.requires_grad:
                        module.affine = False
                        module.track_running_stats = False

        # Calculate Loss depending on Trainer/Model
        self.current_loss = loss = self.loss(**batch_data)
        self.optimizer.zero_grad()
        loss.backward()

        # Gradient Clipping
        if self.clip_value > 0:
            torch.nn.utils.clip_grad_value_(self.model.parameters(), self.clip_value)

        self.optimizer.step()

    @abstractmethod
    def on_iteration_end(self):
        pass

    def on_epoch_end(self):
        # Get Train Epoch Logs
        for key in self.iter_logs:
            if "loss" in key:
                self.logs["epoch_" + key].append(
                    sum(self.iter_logs[key][-self.iters_per_epoch:]) / self.iters_per_epoch)

        # Validate Model
        if self.valid_data is not None:
            self.validate()

        # Monitor Logs
        if self.monitor:
            print_progress(self.epoch, self.logs, self.n_epochs)

    def check_early_stop(self):
        # Calculate Early Stopping and best state
        early_stopping_metric = self.early_stopping.early_stopping_metric
        save_best_state_metric = self.early_stopping.save_best_state_metric
        if save_best_state_metric is not None and self.early_stopping.update_state(
                self.logs[save_best_state_metric][-1]):
            self.best_state_dict = self.model.state_dict()
            self.best_epoch = self.epoch
        continue_training = True
        if early_stopping_metric is not None and not self.early_stopping.step(self.logs[early_stopping_metric][-1]):
            continue_training = False
            return continue_training

        # Update Learning Rate
        self.lr_scheduler.step()
        return continue_training

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

    def train(self,
              n_epochs=400,
              lr=1e-3,
              lr_gamma=1.0,
              lr_step_size=100,
              eps=0.01):
        begin = time.time()
        self.model.train()
        self.n_epochs = n_epochs

        params = filter(lambda p: p.requires_grad, self.model.parameters())

        self.optimizer = torch.optim.Adam(params, lr=lr, eps=eps, weight_decay=self.weight_decay)
        self.lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer=self.optimizer,
                                                            gamma=lr_gamma,
                                                            step_size=lr_step_size)
        # Initialize Train/Val Data, Sampler, Dataloader
        self.on_training_begin()

        for self.epoch in range(n_epochs):
            # Empty at the moment
            self.on_epoch_begin()
            for self.iter, batch_data in enumerate(self.dataloader_train):
                for key1 in batch_data:
                    for key2, batch in batch_data[key1].items():
                        batch_data[key1][key2] = batch.to(self.device)

                # Empty at the moment
                self.on_iteration_begin()

                # Loss Calculation, Gradient Clipping, Freeze first layer, Optimizer Step
                self.on_iteration(batch_data)

                # Empty at the moment
                self.on_iteration_end()

            # Validation of Model, Monitoring, Early Stopping
            self.on_epoch_end()
            if self.use_early_stopping:
                if not self.check_early_stop():
                    break

        if self.best_state_dict is not None:
            print("Saving best state of network...")
            print("Best State was in Epoch", self.best_epoch)
            self.model.load_state_dict(self.best_state_dict)

        self.model.eval()

        self.training_time += (time.time() - begin)

        # Empty at the moment
        self.on_training_end()
