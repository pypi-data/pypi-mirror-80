import scanpy as sc
import numpy as np
import scvi as scv
import scarchest as sca
from scarchest.plotting import SCVI_EVAL
from scarchest.dataset.trvae.data_handling import remove_sparsity

use_scarches_version = True
freeze = True
freeze_expression = True

show_plots = True

n_epochs_vae = 200
n_epochs_scanvi = 100
n_epochs_surgery = 100
n_query_labels = 0

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

# ---------------------------------------------------DATA PREPROCESSING-------------------------------------------------

condition_key = 'study'
cell_type_key = 'cell_type'
conditions_dict = dict()
cell_type_dict = dict()

target_conditions = ["Pancreas SS2", "Pancreas CelSeq2"]
adata = sc.read("../../datasets/pancreas_normalized.h5ad",
                backup_url=f"https://zenodo.org/record/3930949/files/pancreas_normalized.h5ad?download=1", sparse=True,
                cache=True)
adata.X = adata.raw.X
adata = remove_sparsity(adata)
celltypes = adata.obs[cell_type_key].unique().tolist()
conditions = adata.obs[condition_key].unique().tolist()

# Save Source Adata
source_adata = adata[~adata.obs[condition_key].isin(target_conditions)].copy()
scv.data.setup_anndata(source_adata, batch_key=condition_key, labels_key=cell_type_key)
source_stats = source_adata.uns["_scvi"]["summary_stats"]
print('SOURCE ADATA...\n', source_adata)
print('SOURCE STATS...\n', source_stats)

# Save Target Adata
target_adata = adata[adata.obs[condition_key].isin(target_conditions)].copy()
scv.data.setup_anndata(target_adata, batch_key=condition_key, labels_key=cell_type_key)
target_stats = target_adata.uns["_scvi"]["summary_stats"]
print('\nTARGET ADATA...\n', target_adata)
print('TARGET STATS...\n', target_stats)

# ----------------------------------------------TRAIN NEW MODEL ON REFERENCE--------------------------------------------
# Train scVI Model on Reference Data
print("\nSCVI MODEL ARCH...")
scvi = sca.models.scVI(
    source_stats["n_genes"],
    n_batch=source_stats["n_batch"],
    n_layers=2,
    modified=use_scarches_version,
)
trainer = sca.trainers.scVITrainer(
    scvi,
    source_adata,
    train_size=0.9,
    use_cuda=True,
    frequency=1,
    silent=False,
    early_stopping_kwargs=early_stopping_kwargs
)
trainer.train(n_epochs_vae)
scvi_eval = SCVI_EVAL(
    scvi,
    trainer,
    source_adata,
    cell_type_key=cell_type_key,
    batch_key=condition_key
)
scvi_eval.get_latent_score()
# vae_eval.get_model_arch()
if show_plots:
    scvi_eval.plot_history(n_epochs_vae)
    scvi_eval.plot_latent()

# Train scANVI Model on Query Data
print('\n', 20 * '###')
print("STARTING WITH SCANVI...")
scanvi = sca.models.scANVI(
    source_stats["n_genes"],
    n_batch=source_stats["n_batch"],
    n_labels=source_stats["n_labels"],
    n_layers=2,
    classifier_parameters={'dropout_rate': 0.2, 'n_hidden': 10, 'n_layers': 1},
    modified=use_scarches_version
)
scanvi.load_state_dict(scvi.state_dict(), strict=False)
trainer_scanvi = sca.trainers.scANVITrainer(
    scanvi,
    source_adata,
    n_labelled_samples_per_class=source_stats["n_cells"],
    train_size=0.9,
    use_cuda=True,
    frequency=1,
    silent=False,
    early_stopping_kwargs=early_stopping_kwargs_scanvi
)
trainer_scanvi.train(n_epochs=n_epochs_scanvi)
scanvi_eval = SCVI_EVAL(
    scanvi,
    trainer_scanvi,
    source_adata,
    cell_type_key=cell_type_key,
    batch_key=condition_key)
scanvi_eval.get_latent_score()
scanvi_eval.get_classification_accuracy()
# scanvi_eval.get_model_arch()
if show_plots:
    scanvi_eval.plot_history(n_epochs_scanvi)
    scanvi_eval.plot_latent()
# -------------------------------------------------------TL PART--------------------------------------------------------

new_scanvi, new_trainer, target_gene_adata = sca.scvi_operate(
    network=scanvi,
    data=target_adata,
    n_epochs=n_epochs_surgery,
    labels_per_class=n_query_labels,
    freeze=freeze,
    freeze_expression=freeze_expression,
)
surgery_eval = SCVI_EVAL(
    new_scanvi,
    new_trainer,
    target_gene_adata,
    cell_type_key=cell_type_key,
    batch_key=condition_key
)
surgery_eval.get_latent_score()
surgery_eval.get_classification_accuracy()
if show_plots:
    surgery_eval.plot_history(n_epochs_surgery)
    surgery_eval.plot_latent()

# -----------------------------------------------------USE FULL DATA----------------------------------------------------
print('\n', 20 * '###')
print("FULL REPRESENTATION...")
scv.data.setup_anndata(adata, batch_key=condition_key, labels_key=cell_type_key)

# Recreate Right Batch Encoding
source_conditions = source_adata.obs[condition_key].unique().tolist()
for condition in source_conditions:
    condition_label = source_adata[source_adata.obs[condition_key] == condition].obs['_scvi_batch'].unique().tolist()[0]
    conditions_dict[condition] = condition_label
target_conditions = target_gene_adata.obs[condition_key].unique().tolist()
for condition in target_conditions:
    condition_label = target_gene_adata[
        target_gene_adata.obs[condition_key] == condition].obs['_scvi_batch'].unique().tolist()[0]
    conditions_dict[condition] = condition_label
adata_conditions = adata.obs[condition_key].copy()
new_conditions = np.zeros_like(adata_conditions)
for idx in range(len(adata_conditions)):
    new_conditions[idx] = conditions_dict[adata_conditions[idx]]
adata.obs['_scvi_batch'] = new_conditions

full_eval = SCVI_EVAL(new_scanvi, new_trainer, adata, cell_type_key=cell_type_key, batch_key=condition_key)
full_eval.get_latent_score()
full_eval.get_classification_accuracy()
if show_plots:
    full_eval.plot_latent()
