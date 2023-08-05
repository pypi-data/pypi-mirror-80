import json
import os

import numpy as np
import scanpy as sc
import scarches as sca
from scarches.dataset.trvae.data_handling import remove_sparsity
from scarches.plotting import SCVI_EVAL


use_modified = True
n_epochs = 500
n_epochs_scanvi = 100
early_stopping_kwargs = {
    "early_stopping_metric": "elbo",
    "save_best_state_metric": "elbo",
    "patience": 10,
    "threshold": 0,
    "reduce_lr_on_plateau": True,
    "lr_patience": 8,
    "lr_factor": 0.1,
}
early_stopping_kwargs_scanvi = {
    "early_stopping_metric": "accuracy",
    "save_best_state_metric": "accuracy",
    "on": "full_dataset",
    "patience": 10,
    "threshold": 0.001,
    "reduce_lr_on_plateau": True,
    "lr_patience": 8,
    "lr_factor": 0.1,
}
target_batches = ["Pancreas SS2", "Pancreas CelSeq2"]
batch_key = "study"
cell_type_key = "cell_type"
adata = sc.read("../../../datasets/pancreas_normalized.h5ad")
adata.X = adata.raw.X
adata = remove_sparsity(adata)
fraction_list = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0]

ebm_results = dict()
knn_results = dict()
acc_results = dict()
for fraction in fraction_list:
    ebm_results[str(fraction)] = list()
    knn_results[str(fraction)] = list()
    acc_results[str(fraction)] = list()

for i in range(5):
    for subsample_frac in fraction_list:

        # Create Adata of fraction of every target batch
        final_adata = None
        for target in target_batches:
            adata_sampled = adata[adata.obs[batch_key] == target, :]
            keep_idx = np.loadtxt(f'../../../datasets/pancreas_subsample/pancreas/{target}/{subsample_frac}/{i}.csv',
                                  dtype='int32')
            adata_sampled = adata_sampled[keep_idx, :]

            if final_adata is None:
                final_adata = adata_sampled
            else:
                final_adata = final_adata.concatenate(adata_sampled)

        sca.dataset.setup_anndata(final_adata, batch_key=batch_key, labels_key=cell_type_key)
        final_stats = final_adata.uns["scvi_summary_stats"]
        print(final_adata)
        print(final_stats)

        scvi = sca.models.scVI(
            final_stats["n_genes"],
            n_batch=final_stats["n_batch"],
            n_labels=final_stats["n_labels"],
            n_layers=2,
            modified=use_modified,
        )
        trainer = sca.trainers.scVITrainer(
            scvi,
            final_adata,
            train_size=0.8,
            use_cuda=True,
            frequency=1,
            early_stopping_kwargs=early_stopping_kwargs
        )
        trainer.train(n_epochs=n_epochs)
        scanvi = sca.models.scANVI(
            final_stats["n_genes"],
            n_batch=final_stats["n_batch"],
            n_labels=final_stats["n_labels"],
            n_layers=2,
            classifier_parameters={'dropout_rate': 0.2, 'n_hidden': 10, 'n_layers': 1},
            modified=use_modified
        )
        scanvi.load_state_dict(scvi.state_dict(), strict=False)
        trainer_scanvi = sca.trainers.scANVITrainer(
            scanvi,
            final_adata,
            n_labelled_samples_per_class=5,
            train_size=0.9,
            use_cuda=True,
            frequency=1,
            early_stopping_kwargs=early_stopping_kwargs_scanvi,
        )
        trainer_scanvi.train(n_epochs=n_epochs_scanvi)

        scanvi_eval = SCVI_EVAL(
            scanvi,
            trainer_scanvi,
            final_adata,
            cell_type_key=cell_type_key,
            batch_key=batch_key)
        ebm_results[str(subsample_frac)].append(scanvi_eval.get_ebm())
        knn_results[str(subsample_frac)].append(scanvi_eval.get_knn_purity())
        acc_results[str(subsample_frac)].append(scanvi_eval.get_classification_accuracy())

print("EBM:", ebm_results)
print("KNN:", knn_results)
print("ACC:", acc_results)

overall_results = list()
for fraction in fraction_list:
    subsample_results = list()
    subsample_results.append(sum(ebm_results[str(fraction)]) / len(ebm_results[str(fraction)]))
    subsample_results.append(sum(knn_results[str(fraction)]) / len(knn_results[str(fraction)]))
    subsample_results.append(sum(acc_results[str(fraction)]) / len(acc_results[str(fraction)]))
    overall_results.append(subsample_results)
if use_modified:
    save_path = os.path.expanduser('~/Documents/benchmark_results/modified/only_query/')
else:
    save_path = os.path.expanduser('~/Documents/benchmark_results/base/only_query/')
if not os.path.exists(save_path):
    os.makedirs(save_path)
with open(save_path + "results.txt", 'w') as filehandle:
    json.dump(overall_results, filehandle)
