from scvi.data import get_from_registry

from scarchest.metrics.metrics import entropy_batch_mixing, knn_purity
from scarchest.models import scVI, scANVI
from scarchest.trainers import scVITrainer, scANVITrainer


import numpy as np
import scanpy as sc
import torch
from typing import Union
import anndata
import matplotlib.pyplot as plt

sc.settings.set_figure_params(dpi=100, frameon=False)
sc.set_figure_params(dpi=100)
torch.set_printoptions(precision=3, sci_mode=False, edgeitems=7)
np.set_printoptions(precision=2, edgeitems=7)


class SCVI_EVAL:
    def __init__(
            self,
            model: Union[scVI, scANVI],
            trainer: Union[scVITrainer, scANVITrainer],
            adata: anndata.AnnData,
            cell_type_key: str,
            batch_key: str,
    ):
        self.model = model
        self.trainer = trainer
        self.adata = adata
        self.modified = model.modified
        self.annotated = type(model) is scANVI
        self.post_adata_2 = None
        self.predictions = None

        if self.trainer.use_cuda:
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')

        self.x_tensor = torch.tensor(self.adata.X, device=self.device)
        self.labels = get_from_registry(self.adata, "labels").astype(np.int8)
        self.label_tensor = torch.tensor(self.labels, device=self.device)
        self.cell_types = self.adata.obs[cell_type_key].tolist()

        self.batch_indices = get_from_registry(self.adata, "batch_indices").astype(np.int8)
        self.batch_tensor = torch.tensor(self.batch_indices, device=self.device)
        self.batch_names = self.adata.obs[batch_key].tolist()

        self.post_adata = self.latent_as_anndata()

    def latent_as_anndata(self):

        if self.modified:
            latents = self.model.get_latents(
                self.x_tensor,
                y=self.label_tensor,
                batch_index=self.batch_tensor
            )
        else:
            latents = self.model.get_latents(
                self.x_tensor,
                y=self.label_tensor,
            )
        if self.annotated:
            latent = latents[0].cpu().detach().numpy()
            latent2 = latents[1].cpu().detach().numpy()
            post_adata_2 = sc.AnnData(latent2)
            post_adata_2.obs['cell_type'] = self.cell_types
            post_adata_2.obs['batch'] = self.batch_names
            self.post_adata_2 = post_adata_2
        else:
            latent = latents[0].cpu().detach().numpy()

        post_adata = sc.AnnData(latent)
        post_adata.obs['cell_type'] = self.cell_types
        post_adata.obs['batch'] = self.batch_names
        return post_adata

    def get_model_arch(self):
        for name, p in self.model.named_parameters():
            print(name, " - ", p.size(0), p.size(-1))

    def plot_latent(self, n_neighbors=8):
        sc.pp.neighbors(self.post_adata, n_neighbors=n_neighbors)
        sc.tl.umap(self.post_adata)
        sc.pl.umap(self.post_adata, color=['cell_type', 'batch'], frameon=False, wspace=0.6)

    def plot_latent_ann(self, n_neighbors=8):
        if self.annotated:
            sc.pp.neighbors(self.post_adata_2, n_neighbors=n_neighbors)
            sc.tl.umap(self.post_adata_2)
            sc.pl.umap(self.post_adata_2, color=['cell_type', 'batch'], frameon=False, wspace=0.6)
        else:
            print("Second latent space not available for scVI models")

    def plot_history(self, n_epochs):
        if self.annotated:
            elbo_full = self.trainer.history["elbo_full_dataset"]
            x_1 = np.linspace(0, len(elbo_full), len(elbo_full))
            fig, axs = plt.subplots(2, 1)
            axs[0].plot(x_1, elbo_full, label="Full")

            accuracy_labelled_set = self.trainer.history["accuracy_labelled_set"]
            accuracy_unlabelled_set = self.trainer.history["accuracy_unlabelled_set"]
            if len(accuracy_labelled_set) != 0:
                x_2 = np.linspace(0, len(accuracy_labelled_set), (len(accuracy_labelled_set)))
                axs[1].plot(x_2, accuracy_labelled_set, label="accuracy labelled")
            if len(accuracy_unlabelled_set) != 0:
                x_3 = np.linspace(0, len(accuracy_unlabelled_set), (len(accuracy_unlabelled_set)))
                axs[1].plot(x_3, accuracy_unlabelled_set, label="accuracy unlabelled")
            axs[0].set_xlabel('Epochs')
            axs[0].set_ylabel('ELBO')
            axs[1].set_xlabel('Epochs')
            axs[1].set_ylabel('Accuracy')
            plt.legend()
            plt.show()
        else:
            elbo_train = self.trainer.history["elbo_train_set"]
            elbo_test = self.trainer.history["elbo_test_set"]
            x = np.linspace(0, len(elbo_train), len(elbo_train))
            plt.plot(x, elbo_train, label="train")
            plt.plot(x, elbo_test, label="test")
            plt.ylim(min(elbo_train) - 50, min(elbo_train) + 1000)
            plt.legend()
            plt.show()

    def get_ebm(self, n_neighbors=50, n_pools=50, n_samples_per_pool=100, verbose=True):
        ebm_score = entropy_batch_mixing(
            adata=self.post_adata,
            label_key='batch',
            n_neighbors=n_neighbors,
            n_pools=n_pools,
            n_samples_per_pool=n_samples_per_pool
        )
        if verbose:
            print("Entropy of Batchmixing-Score:", ebm_score)
        return ebm_score

    def get_knn_purity(self, n_neighbors=50, verbose=True):
        knn_score = knn_purity(
            adata=self.post_adata,
            label_key='cell_type',
            n_neighbors=n_neighbors
        )
        if verbose:
            print("KNN Purity-Score:", knn_score)
        return knn_score

    def get_latent_score(self):
        ebm = self.get_ebm(verbose=False)
        knn = self.get_knn_purity(verbose=False)
        score = ebm + knn
        print("Latent-Space Score (KNN + EBM):", score)
        return score

    def get_classification_accuracy(self):
        if self.annotated:
            if self.modified:
                predictions = self.model.classify(self.x_tensor, batch_index=self.batch_tensor)
            else:
                predictions = self.model.classify(self.x_tensor)
            self.predictions = predictions.cpu().detach().numpy()
            self.predictions = np.argmax(self.predictions, axis=1)
            class_check = np.array(np.expand_dims(self.predictions, axis=1) == self.labels)
            accuracy = np.sum(class_check) / class_check.shape[0]
            print("Classification Accuracy: %0.2f" % accuracy)
            return accuracy
        else:
            print("Classification ratio not available for scVI models")