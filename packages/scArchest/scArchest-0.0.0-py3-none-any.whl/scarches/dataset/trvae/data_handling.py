import scanpy as sc
from scipy import sparse


def hvg_batch(adata, batch_key=None, target_genes=2000, flavor='cell_ranger', n_bins=20, adataout=False):
    """
    Method to select HVGs based on mean dispersions of genes that are highly
    variable genes in all batches. Using a the top target_genes per batch by
    average normalize dispersion. If target genes still hasn't been reached,
    then HVGs in all but one batches are used to fill up. This is continued
    until HVGs in a single batch are considered.
    """

    adata_hvg = adata if adataout else adata.copy()

    n_batches = len(adata_hvg.obs[batch_key].cat.categories)

    # Calculate double target genes per dataset
    sc.pp.highly_variable_genes(adata_hvg,
                                flavor=flavor,
                                n_top_genes=target_genes,
                                n_bins=n_bins,
                                batch_key=batch_key)

    nbatch1_dispersions = adata_hvg.var['dispersions_norm'][adata_hvg.var.highly_variable_nbatches >
                                                            len(adata_hvg.obs[batch_key].cat.categories) - 1]

    nbatch1_dispersions.sort_values(ascending=False, inplace=True)

    if len(nbatch1_dispersions) > target_genes:
        hvg = nbatch1_dispersions.index[:target_genes]

    else:
        enough = False
        print(f'Using {len(nbatch1_dispersions)} HVGs from full intersect set')
        hvg = nbatch1_dispersions.index[:]
        not_n_batches = 1

        while not enough:
            target_genes_diff = target_genes - len(hvg)

            tmp_dispersions = adata_hvg.var['dispersions_norm'][adata_hvg.var.highly_variable_nbatches ==
                                                                (n_batches - not_n_batches)]

            if len(tmp_dispersions) < target_genes_diff:
                print(f'Using {len(tmp_dispersions)} HVGs from n_batch-{not_n_batches} set')
                hvg = hvg.append(tmp_dispersions.index)
                not_n_batches += 1

            else:
                print(f'Using {target_genes_diff} HVGs from n_batch-{not_n_batches} set')
                tmp_dispersions.sort_values(ascending=False, inplace=True)
                hvg = hvg.append(tmp_dispersions.index[:target_genes_diff])
                enough = True

    print(f'Using {len(hvg)} HVGs')

    if not adataout:
        del adata_hvg
        return hvg.tolist()
    else:
        return adata_hvg[:, hvg].copy()


def remove_sparsity(adata):
    """
        If ``adata.X`` is a sparse matrix, this will convert it in to normal matrix.
        Parameters
        ----------
        adata: :class:`~anndata.AnnData`
            Annotated data matrix.
        Returns
        -------
        adata: :class:`~anndata.AnnData`
            Annotated dataset.
    """
    if sparse.issparse(adata.X):
        new_adata = sc.AnnData(X=adata.X.A, obs=adata.obs.copy(deep=True), var=adata.var.copy(deep=True))
        return new_adata

    return adata


def preprocess_data(adata,
                    filter_min_counts=True,
                    size_factors=True,
                    target_sum=None,
                    log_trans_input=True,
                    batch_key=None,
                    n_top_genes=1000,
                    scale=False):
    """Preprocesses the `adata`.
       Parameters
       ----------
       adata: `~anndata.AnnData`
            Annotated data matrix.
       filter_min_counts: boolean
            If 'True' filter out Genes and Cells under min_count.
       size_factors: boolean
            If 'True' add Size Factors for ZINB/NB loss to 'adata'.
       target_sum:
       log_trans_input: boolean
            If 'True' logarithmize the data matrix.
       batch_key:
       n_top_genes: int
            Only keeps n highest variable genes in 'adata'
       scale: boolean
            If 'True' scale data to unit variance and zero mean.
       Returns
       -------
       adata: `~anndata.AnnData`
            Preprocessed annotated data matrix.
    """

    if filter_min_counts:
        sc.pp.filter_genes(adata, min_counts=1)
        sc.pp.filter_cells(adata, min_counts=1)

    adata_count = adata.copy()
    obs = adata.obs_keys()

    if size_factors and 'size_factors' not in obs:
        sc.pp.normalize_total(adata,
                              target_sum=target_sum,
                              exclude_highly_expressed=False,
                              key_added='size_factors')

    if log_trans_input:
        sc.pp.log1p(adata)
        if 0 < n_top_genes < adata.shape[1]:
            if batch_key:
                genes = hvg_batch(adata.copy(), batch_key=batch_key, adataout=False, target_genes=n_top_genes)
            else:
                sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes)
                genes = adata.var['highly_variable']
            adata = adata[:, genes]
            adata_count = adata_count[:, genes]

    if scale:
        sc.pp.scale(adata)

    if sparse.issparse(adata_count.X):
        adata_count.X = adata_count.X.A
    if sparse.issparse(adata.X):
        adata.X = adata.X.A

    if adata.raw is None:
        adata.raw = adata_count.copy()

    return adata
