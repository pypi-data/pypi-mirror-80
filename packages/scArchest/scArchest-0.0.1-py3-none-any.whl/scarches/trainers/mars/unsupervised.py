import time

import scanpy as sc
import torch
from torch.utils.data import DataLoader

from scarchest.models import MARS
from scarchest.trainers.trvae._utils import make_dataset
from ._utils import print_meta_progress
from .meta import MetaTrainer


class MARSPreTrainer(MetaTrainer):
    def __init__(self, model: MARS, adata: sc.AnnData, task_key: str,
                 **kwargs):
        super().__init__(model, adata, task_key, **kwargs)

    def on_training_begin(self):
        self.train_dataset, self.valid_dataset = make_dataset(self.adata,
                                                              train_frac=self.train_frac,
                                                              use_stratified_split=True,
                                                              condition_key=self.task_key,
                                                              cell_type_key=None,
                                                              size_factor_key=None,
                                                              condition_encoder=self.model.condition_encoder,
                                                              )
        self.train_data_loader = DataLoader(dataset=self.train_dataset,
                                            batch_size=self.batch_size,
                                            num_workers=self.n_workers)

        self.valid_data_loader = DataLoader(dataset=self.valid_dataset,
                                            batch_size=len(self.valid_dataset),
                                            num_workers=1)

        self.optimizer = torch.optim.Adam(params=list(self.model.parameters()), lr=self.learning_rate)

        self.lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer=self.optimizer,
                                                            gamma=self.lr_gamma,
                                                            step_size=self.lr_step_size)

    def train(self,
              n_epochs=400,
              ):
        begin = time.time()

        # Initialize Train/Val Data, Optimizer, Sampler, and Dataloader
        self.on_training_begin()

        for self.epoch in range(n_epochs):
            self.on_epoch_begin()

            loss, recon_loss, kl_loss = self.on_epoch()

            # Validation of Model, Monitoring, Early Stopping
            valid_loss, valid_recon_loss, valid_kl_loss = self.on_epoch_end()

            if self.use_early_stopping:
                if not self.check_early_stop():
                    break

            logs = {
                'loss': [loss],
                'recon_loss': [recon_loss],
                'kl_loss': [kl_loss],
                'val_loss': [valid_loss],
                'val_recon_loss': [valid_recon_loss],
                'val_kl_loss': [valid_kl_loss],
            }

            if self.monitor:
                print_meta_progress(self.epoch, logs, n_epochs)

        if hasattr(self, 'best_state_dict') and self.best_state_dict is not None:
            print("Saving best state of network...")
            print("Best State was in Epoch", self.best_epoch)
            self.model.load_state_dict(self.best_state_dict)

        self.model.eval()

        self.training_time += (time.time() - begin)

        # Empty at the moment
        self.on_training_end()

    def on_epoch(self):
        self.model.train()

        loss = torch.tensor(0.0)
        recon_loss = torch.tensor(0.0)
        kl_loss = torch.tensor(0.0)

        for batch_data in self.train_data_loader:
            x = batch_data['x'].to(self.device)
            c = batch_data['c'].to(self.device)

            _, decoded, batch_loss, batch_recon_loss, batch_kl_loss = self.model(x, c)

            loss += batch_loss * len(batch_data)
            kl_loss += batch_kl_loss * len(batch_data)
            recon_loss += batch_recon_loss * len(batch_data)

            self.optimizer.zero_grad()
            batch_loss.backward()

            if self.clip_value > 0:
                torch.nn.utils.clip_grad_value_(self.model.parameters(), self.clip_value)

            self.optimizer.step()

        loss /= len(self.train_dataset)
        recon_loss /= len(self.train_dataset)
        kl_loss /= len(self.train_dataset)

        return loss, recon_loss, kl_loss

    def on_epoch_end(self, evaluate_on_meta_test=False):
        self.model.eval()

        with torch.no_grad():
            valid_loss, valid_recon_loss, valid_kl_loss = 0.0, 0.0, 0.0
            for valid_data in self.valid_data_loader:
                x = valid_data['x'].to(self.device)
                c = valid_data['c'].to(self.device)

                _, _, batch_loss, batch_recon_loss, batch_kl_loss = self.model(x, c)
                valid_loss += batch_loss * len(valid_data)
                valid_recon_loss += batch_recon_loss * len(valid_data)
                valid_kl_loss += batch_kl_loss * len(valid_data)

            valid_loss /= len(self.valid_dataset)
            valid_kl_loss /= len(self.valid_dataset)
            valid_recon_loss /= len(self.valid_dataset)

        return valid_loss, valid_recon_loss, valid_kl_loss

    def on_epoch_begin(self):
        pass

    def on_iteration_begin(self):
        pass

    def on_iteration_end(self):
        pass

    def on_training_end(self):
        pass

    def check_early_stop(self):
        return True
