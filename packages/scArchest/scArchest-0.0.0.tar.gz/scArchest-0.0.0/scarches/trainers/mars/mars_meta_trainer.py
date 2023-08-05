import time

import torch
from sklearn.cluster import KMeans
from torch.utils.data import DataLoader

from scarches.dataset.mars import MetaAnnotatedDataset
from scarches.dataset.trvae import AnnotatedDataset
from scarches.models import MARS
from ._utils import split_meta_train_tasks, euclidean_dist, print_meta_progress
from .meta import MetaTrainer
import scanpy as sc


class MARSTrainer(MetaTrainer):
    def __init__(self, model: MARS, adata: sc.AnnData, task_key: str, cell_type_key: str, n_clusters: int,
                 meta_test_tasks: list,
                 tau: float = 0.2, eta: float = 1.0, **kwargs):
        super().__init__(model, adata, task_key, **kwargs)

        self.cell_type_key = cell_type_key
        self.n_clusters = n_clusters
        self.meta_test_tasks = meta_test_tasks
        self.tau = tau
        self.eta = eta
        self.pre_train_n_epochs = kwargs.pop('pre_train_n_epochs', 100)
        self.pre_train_batch_size = kwargs.pop('pre_train_batch_size', 128)

    def on_training_begin(self):
        self.meta_adata = MetaAnnotatedDataset(adata=self.adata,
                                               task_key=self.task_key,
                                               meta_test_task=self.meta_test_tasks[0],
                                               cell_type_key=self.cell_type_key,
                                               task_encoder=self.model.condition_encoder,
                                               )
        self.meta_train_data_loaders_tr, self.meta_train_data_loaders_ts = split_meta_train_tasks(self.meta_adata,
                                                                                                  self.train_frac,
                                                                                                  stratify=True,
                                                                                                  batch_size=self.batch_size,
                                                                                                  num_workers=self.n_workers)
        self.meta_test_data_loader = pre_train_data_loader = DataLoader(dataset=self.meta_adata.meta_test_task_adata,
                                                                        batch_size=self.pre_train_batch_size,
                                                                        num_workers=self.n_workers)

        self.pre_train_with_meta_test(pre_train_data_loader)

        self.meta_train_landmarks, self.meta_test_landmarks = self.initialize_landmarks()

        self.optimizer = torch.optim.Adam(params=list(self.model.encoder.parameters()), lr=self.learning_rate)
        self.meta_test_landmark_optimizer = torch.optim.Adam(params=[self.meta_test_landmarks], lr=self.learning_rate)

        self.lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer=self.optimizer,
                                                            gamma=self.lr_gamma,
                                                            step_size=self.lr_step_size)

    def pre_train_with_meta_test(self, pre_train_data_loader):
        pre_train_optimizer = torch.optim.Adam(params=list(self.model.parameters()), lr=self.pre_train_learning_rate)

        for _ in range(self.pre_train_n_epochs):
            for _, batch_data in enumerate(pre_train_data_loader):
                x = batch_data['x'].to(self.device)
                c = batch_data['c'].to(self.device)
                _, decoded, loss, recon_loss, kl_loss = self.model(x, c)

                pre_train_optimizer.zero_grad()
                loss.backward()

                if self.clip_value > 0:
                    torch.nn.utils.clip_grad_value_(self.model.parameters(), self.clip_value)

                pre_train_optimizer.step()

    def initialize_landmarks(self):
        def k_means_initalization(dataset: AnnotatedDataset, n_clusters):
            encoded = self.model.get_latent(dataset.data, dataset.conditions)
            k_means = KMeans(n_clusters=n_clusters, random_state=0).fit(encoded)
            return torch.tensor(k_means.cluster_centers_, device=self.device)

        meta_train_landmarks = [
            torch.zeros(size=(len(adataset.unique_cell_types), self.model.z_dim), requires_grad=True,
                        device=self.device) for adataset in self.meta_adata.meta_train_tasks_adata]
        meta_test_landmarks = torch.zeros(size=(self.n_clusters, self.model.z_dim), requires_grad=True,
                                          device=self.device)

        k_means_init_train = [k_means_initalization(adataset, n_clusters=len(adataset.unique_cell_types))
                              for adataset in self.meta_adata.meta_train_tasks_adata]
        k_means_init_test = k_means_initalization(self.meta_adata.meta_test_task_adata,
                                                  n_clusters=self.n_clusters)

        with torch.no_grad():
            [landmark.copy_(k_means_init_train[idx]) for idx, landmark in enumerate(meta_train_landmarks)]
            meta_test_landmarks.copy_(k_means_init_test)

        return meta_train_landmarks, meta_test_landmarks

    def train(self,
              n_epochs=400,
              evaluate_on_meta_test=True,
              ):
        begin = time.time()

        # Initialize Train/Val Data, Optimizer, Sampler, and Dataloader
        self.on_training_begin()

        for self.epoch in range(n_epochs):
            self.on_epoch_begin()

            loss, acc = self.on_epoch()

            # Validation of Model, Monitoring, Early Stopping
            if evaluate_on_meta_test:
                valid_loss, valid_acc, test_accuracy = self.on_epoch_end(evaluate_on_meta_test)
            else:
                valid_loss, valid_acc = self.on_epoch_end(evaluate_on_meta_test)

            if self.use_early_stopping:
                if not self.check_early_stop():
                    break

            logs = {
                'loss': [loss],
                'acc': [acc],
                'val_loss': [valid_loss],
                'val_acc': [valid_acc],
            }

            if evaluate_on_meta_test:
                logs['test_accuracy'] = [test_accuracy]

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

    def on_epoch(self):  # EM step perfomed on each epoch
        self.model.train()
        # Update Landmarks
        for param in self.model.parameters():
            param.requires_grad = False

        self.meta_test_landmarks.requires_grad = False
        self.meta_test_landmark_optimizer.zero_grad()

        for idx, task_data_loader_tr in enumerate(self.meta_train_data_loaders_tr):
            for task_data in task_data_loader_tr:
                X = task_data['x'].to(self.device)
                c = task_data['c'].to(self.device)
                y = task_data['y'].to(self.device)

                encoded, _, _, _, _ = self.model(X, c)
                current_meta_train_landmarks = self.update_meta_train_landmarks(encoded, y,
                                                                                self.meta_train_landmarks[idx],
                                                                                self.tau)

                self.meta_train_landmarks[idx] = current_meta_train_landmarks.data

        self.meta_test_landmarks.requires_grad = True
        for task_data in self.meta_test_data_loader:
            X = task_data['x'].to(self.device)
            c = task_data['c'].to(self.device)
            encoded, _, loss, _, _ = self.model(X, c)
            loss = self.eta * loss + self.test_loss(encoded, self.meta_test_landmarks, self.tau)

            loss.backward()
            self.meta_test_landmark_optimizer.step()

        # Update Encoder
        for param in self.model.parameters():
            param.requires_grad = True

        self.meta_test_landmarks.requires_grad = False
        self.optimizer.zero_grad()

        loss = torch.tensor(0.0)
        acc = torch.tensor(0.0)
        for idx, task_data_loader_tr in enumerate(self.meta_train_data_loaders_tr):
            for batch_data in task_data_loader_tr:
                X = batch_data['x'].to(self.device)
                c = batch_data['c'].to(self.device)
                y = batch_data['y'].to(self.device)

                encoded, _, loss, _, _ = self.model(X, c)
                task_loss, task_acc = self.task_loss(encoded, y, self.meta_train_landmarks[idx])
                loss = self.eta * loss + task_loss
                acc += task_acc

        n_tasks = len(self.meta_train_data_loaders_tr)

        acc /= n_tasks

        for batch_data in self.meta_test_data_loader:
            X = batch_data['x'].to(self.device)
            c = batch_data['c'].to(self.device)
            encoded, _, loss, _, _ = self.model(X, c)
            loss = self.eta * loss + self.test_loss(encoded, self.meta_test_landmarks, self.tau)

        loss = loss / (n_tasks + 1)

        loss.backward()
        self.optimizer.step()

        return loss, acc

    def on_epoch_end(self, evaluate_on_meta_test=False):
        self.model.eval()
        n_tasks = len(self.meta_train_data_loaders_ts)
        with torch.no_grad():
            valid_loss, valid_acc = 0.0, 0.0
            for idx, task_data_loader_tr in enumerate(self.meta_train_data_loaders_ts):
                for task_data in task_data_loader_tr:
                    X = task_data['x'].to(self.device)
                    c = task_data['c'].to(self.device)
                    y = task_data['y'].to(self.device)

                    encoded, _, _, _, _ = self.model(X, c)
                    task_loss, task_acc = self.task_loss(encoded, y, self.meta_train_landmarks[idx])
                    valid_loss += task_loss
                    valid_acc += task_acc.item()

        mean_accuracy = valid_acc / n_tasks
        mean_loss = valid_loss / n_tasks

        if evaluate_on_meta_test:
            test_accuracy = 0.0
            with torch.no_grad():
                for batch_data in self.meta_test_data_loader:
                    X = batch_data['x'].to(self.device)
                    c = batch_data['c'].to(self.device)
                    y = batch_data['y'].to(self.device)
                    encoded, _, _, _, _ = self.model(X, c)
                    test_accuracy += self.evaluate_on_unannotated_dataset(encoded, y) * X.shape[0]

            test_accuracy /= len(self.meta_test_data_loader.dataset)

            return mean_loss, mean_accuracy, test_accuracy
        else:
            return mean_loss, mean_accuracy

    def evaluate_on_unannotated_dataset(self, encoded, y_true):
        distances = euclidean_dist(encoded, self.meta_test_landmarks)
        _, y_pred = torch.max(-distances, dim=1)

        accuracy = y_pred.eq(y_true).float().mean()
        return accuracy

    def task_loss(self, embeddings, labels, landmarks):
        n_samples = embeddings.shape[0]
        unique_labels = torch.unique(labels, sorted=True)
        class_indices = list(map(lambda x: labels.eq(x).nonzero(), unique_labels))

        for idx, value in enumerate(unique_labels):
            labels[labels == value] = idx

        distances = euclidean_dist(embeddings, landmarks)

        loss = torch.stack(
            [distances[indices, landmark_index].sum(0) for landmark_index, indices in
             enumerate(class_indices)]).sum() / n_samples

        _, y_pred = torch.max(-distances, dim=1)

        accuracy = y_pred.eq(labels.squeeze()).float().mean()

        return loss, accuracy

    def test_loss(self, embeddings, landmarks, tau):
        distances = euclidean_dist(embeddings, landmarks)
        min_distances, y_hat = torch.min(distances, dim=1)
        unique_predicted_labels = torch.unique(y_hat, sorted=True)

        loss = torch.stack(
            [min_distances[y_hat == unique_y_hat].mean(0) for unique_y_hat in unique_predicted_labels]).mean()

        if tau > 0:
            landmarks_distances = euclidean_dist(landmarks, landmarks)
            n_landmarks = landmarks.shape[0]
            loss -= torch.sum(landmarks_distances) * tau / (n_landmarks * (n_landmarks - 1))

        return loss

    def update_meta_train_landmarks(self, embeddings, labels, previous_landmarks, tau):
        unique_labels = torch.unique(labels, sorted=True)
        class_indices = list(map(lambda y: labels.eq(y).nonzero(), unique_labels))

        landmarks_mean = torch.stack([embeddings[class_index].mean(0) for class_index in class_indices]).squeeze()

        if previous_landmarks is None or tau == 0:
            return landmarks_mean

        previous_landmarks_sum = previous_landmarks.sum(0)
        n_landmarks = previous_landmarks.shape[0]
        landmarks_distance_partial = (tau / (n_landmarks - 1)) * torch.stack(
            [previous_landmarks_sum - landmark for landmark in previous_landmarks])
        landmarks = (1 / (1 - tau)) * (landmarks_mean - landmarks_distance_partial)

        return landmarks

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
