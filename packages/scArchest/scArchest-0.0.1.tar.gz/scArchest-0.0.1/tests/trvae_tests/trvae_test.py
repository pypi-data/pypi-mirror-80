import scanpy as sc
import torch
import scarchest as sca

sc.settings.set_figure_params(dpi=200, frameon=False)
sc.set_figure_params(dpi=200)
torch.set_printoptions(precision=3, sci_mode=False, edgeitems=7)

condition_key = 'study'
size_factor_key = 'size_factors'
cell_type_key = 'cell_type'

target_conditions = ["Pancreas SS2", "Pancreas CelSeq2"]
adata = sc.read("../../datasets/pancreas_normalized.h5ad",
                backup_url=f"https://zenodo.org/record/3930949/files/pancreas_normalized.h5ad?download=1", sparse=True,
                cache=True)
adata = sca.dataset.trvae.preprocess_data(adata,
                                          filter_min_counts=False,
                                          size_factors=False,
                                          target_sum=None,
                                          log_trans_input=False,
                                          batch_key=None,
                                          n_top_genes=1000,
                                          scale=False)
source_adata = adata[~adata.obs[condition_key].isin(target_conditions)]
target_adata = adata[adata.obs[condition_key].isin(target_conditions)]
source_conditions = source_adata.obs[condition_key].unique().tolist()
network = sca.models.trVAE(source_adata.n_vars,
                           conditions=source_conditions,
                           encoder_layer_sizes=[256, 64],
                           latent_dim=32,
                           decoder_layer_sizes=[64, 256],
                           dr_rate=0.05,
                           use_batch_norm=False,
                           calculate_mmd="z",
                           mmd_boundary=None,
                           recon_loss="zinb",
                           alpha=0.5,
                           beta=200,
                           eta=5000)

trainer = sca.trainers.trVAETrainer(network,
                                    source_adata,
                                    alpha_epoch_anneal=200,
                                    condition_key=condition_key,
                                    size_factor_key=size_factor_key,
                                    weight_decay=0.04,
                                    batch_size=1024,
                                    n_samples=4096)

trainer.train(n_epochs=200,
              lr=0.001,
              eps=1e-6)
'''
condition_labels, _ = sca.dataset.trvae.label_encoder(source_adata,
                                                      encoder=network.condition_label_encoder,
                                                      condition_key=condition_key,
                                                      )

data = network.get_latent(source_adata.X, condition_labels)
adata_latent = sc.AnnData(data)

adata_latent.obs[cell_type_key] = source_adata.obs[cell_type_key].tolist()
adata_latent.obs[condition_key] = source_adata.obs[condition_key].tolist()
sc.pp.neighbors(adata_latent, n_neighbors=8)
sc.tl.umap(adata_latent)
sc.pl.umap(adata_latent, color=[condition_key, cell_type_key], frameon=False, wspace=0.6)
'''
# --------------------------------------------------TRANSFER LEARNING---------------------------------------------------
print(network.condition_encoder)
print(trainer.train_data.condition_label_encoder)
print(network.conditions)
new_network = sca.trvae_operate(network,
                                data_conditions=target_conditions,
                                freeze=True,
                                freeze_expression=True,
                                remove_dropout=False)

new_trainer = sca.trainers.trVAETrainer(new_network,
                                        target_adata,
                                        alpha_epoch_anneal=200,
                                        condition_key=condition_key,
                                        size_factor_key=size_factor_key,
                                        weight_decay=0.04,
                                        batch_size=1024,
                                        n_samples=4096)

new_trainer.train(n_epochs=20,
                  lr=0.001,
                  eps=1e-6)

print(new_network.condition_encoder)
print(new_trainer.train_data.condition_label_encoder)
print(new_network.conditions)
'''
condition_labels, _ = sca.dataset.trvae.label_encoder(target_adata,
                                                      encoder=new_network.condition_label_encoder,
                                                      condition_key=condition_key,
                                                      )

data = new_network.get_latent(target_adata.X, condition_labels)
adata_latent = sc.AnnData(data)

adata_latent.obs[cell_type_key] = target_adata.obs[cell_type_key].tolist()
adata_latent.obs[condition_key] = target_adata.obs[condition_key].tolist()
sc.pp.neighbors(adata_latent, n_neighbors=8)
sc.tl.umap(adata_latent)
sc.pl.umap(adata_latent, color=[condition_key, cell_type_key], frameon=False, wspace=0.6)
'''
# -------------------------------------------------Plotting Whole Data--------------------------------------------------
'''
condition_labels, _ = sca.dataset.trvae.label_encoder(adata,
                                                      encoder=new_network.condition_label_encoder,
                                                      condition_key=condition_key,
                                                      )

data = new_network.get_latent(adata.X, condition_labels)
adata_latent = sc.AnnData(data)

adata_latent.obs[cell_type_key] = adata.obs[cell_type_key].tolist()
adata_latent.obs[condition_key] = adata.obs[condition_key].tolist()
sc.pp.neighbors(adata_latent, n_neighbors=8)
sc.tl.umap(adata_latent)
sc.pl.umap(adata_latent, color=[condition_key, cell_type_key], frameon=False, wspace=0.6)
'''
