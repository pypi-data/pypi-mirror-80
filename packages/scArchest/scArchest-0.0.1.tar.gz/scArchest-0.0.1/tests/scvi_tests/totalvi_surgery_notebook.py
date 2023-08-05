import scanpy as sc
import numpy as np
import scvi as scv
import scarchest as sca
from scarchest.plotting import SCVI_EVAL
from scarchest.dataset.trvae.data_handling import remove_sparsity

adata = scv.data.pbmcs_10x_cite_seq(run_setup_anndata=False)
# batch 0 corresponds to dataset_10k, batch 1 corresponds to dataset_5k
batch = adata.obs.batch.values.ravel()
held_out_proteins = adata.obsm["protein_expression"][batch == 1].copy()
adata.obsm["protein_expression"].loc[batch == 1] = np.zeros_like(adata.obsm["protein_expression"][batch == 1])
sc.pp.highly_variable_genes(
    adata,
    batch_key="batch",
    flavor="seurat_v3",
    n_top_genes=4000,
    subset=True
)
scv.data.setup_anndata(adata, batch_key="batch", protein_expression_obsm_key="protein_expression")
vae = sca.models.scvi.totalVI(
    adata,
    latent_distribution="normal",
    n_layers_decoder=2
)