import numpy as np
from typing import Union
import torch
import torch.nn as nn
import anndata

from scvi.data import get_from_registry

from scarchest.models import scVI, scANVI
from scarchest.trainers import scVITrainer, scANVITrainer, UnlabelledScanviTrainer


def weight_update_check(old_network, op_network):
    for op_name, op_p in op_network.named_parameters():
        for name, p in old_network.named_parameters():
            if op_name == name:
                comparison = torch.eq(p, op_p)
                if False in comparison:
                    print("UPDATED WEIGHTS", op_name)
    for name, module in op_network.named_modules():
        if isinstance(module, nn.BatchNorm1d):
            if module.affine == False and module.track_running_stats == False:
                print("FROZEN BATCHNORM:", name)


def scvi_operate(
        network: Union[scVI, scANVI],
        data: anndata.AnnData,
        labels_per_class: int = 0,
        n_epochs: int = 50,
        freeze: bool = True,
        freeze_expression: bool = True,
        remove_dropout: bool = False,
) -> [Union[scVI, scANVI], Union[scVITrainer, scANVITrainer], anndata.AnnData]:
    """Transfer Learning function for new data. Uses old trained Network and expands it for new conditions.
       Parameters
       ----------
       network: VAE_M, SCANVI_M
            A Scvi/Scanvi model object.
       data: GeneExpressionDataset
            GeneExpressionDataset object.
       labels_per_class: Integer
            Number of labelled Samples used for Retraining
       n_epochs: Integer
            Number of epochs for training the network on query data.
       freeze: Boolean
            If 'True' freezes every part of the network except the first layers of encoder/decoder.
       freeze_expression: Boolean
            If 'True' freeze every weight in first layers except the condition weights.
       remove_dropout: Boolean
            If 'True' remove Dropout for Transfer Learning.

       Returns
       -------
       op_network: VAE_M, SCANVI_M
            Newly network that got trained on query data.
       op_trainer: UnsupervisedTrainer, SemiSupervisedTrainer
            Trainer for the newly network.
       data: GeneExpressionDataset
            GeneExpressionDataset object with updated batch labels.
    """

    early_stopping_kwargs = {
        "early_stopping_metric": "elbo",
        "save_best_state_metric": "elbo",
        "patience": 15,
        "threshold": 0,
        "reduce_lr_on_plateau": True,
        "lr_patience": 8,
        "lr_factor": 0.1,
    }
    early_stopping_kwargs_scanvi = {
        "early_stopping_metric": "accuracy",
        "save_best_state_metric": "accuracy",
        "on": "full_dataset",
        "patience": 15,
        "threshold": 0.001,
        "reduce_lr_on_plateau": True,
        "lr_patience": 8,
        "lr_factor": 0.1,
    }

    # Update DR Rate
    new_dr = network.dropout_rate
    if remove_dropout:
        new_dr = 0.0

    n_new_conditions = data.uns["_scvi"]["summary_stats"]["n_batch"]
    adata = data.copy()
    adata.obs['_scvi_batch'] = get_from_registry(adata, "batch_indices").astype(np.int8) + network.n_batch
    n_conditions = network.n_batch + n_new_conditions
    if type(network) is scVI:
        print("Create new VAE....")
        op_network = scVI(
            n_input=network.n_input,
            n_batch=n_conditions,
            n_hidden=network.n_hidden,
            n_latent=network.n_latent,
            n_layers=network.n_layers,
            dropout_rate=new_dr,
            dispersion=network.dispersion,
            log_variational=network.log_variational,
            gene_likelihood=network.gene_likelihood,
            latent_distribution=network.latent_distribution,
            modified=network.modified,
        )
    elif type(network) is scANVI:
        print("Create new SCANVI....")
        op_network = scANVI(
            n_input=network.n_input,
            n_batch=n_conditions,
            n_labels=network.n_labels,
            n_hidden=network.n_hidden,
            n_latent=network.n_latent,
            n_layers=network.n_layers,
            dropout_rate=new_dr,
            dispersion=network.dispersion,
            log_variational=network.log_variational,
            gene_likelihood=network.gene_likelihood,
            y_prior=network.y_prior,
            labels_groups=network.labels_groups,
            use_labels_groups=network.use_labels_groups,
            classifier_parameters=network.cls_parameters,
            modified=network.modified,
        )
    else:
        print("Please use a compatible model for this operate function")
        exit()

    op_network.new_conditions = n_new_conditions
    if network.modified:
        # Expand first Layer weights of z encoder of old network by new conditions
        encoder_input_weights = network.z_encoder.encoder.fc_layers.Layer0.L.cond_L.weight
        to_be_added_encoder_input_weights = np.random.randn(encoder_input_weights.size()[0], n_new_conditions) * \
                                            np.sqrt(2 / (encoder_input_weights.size()[0] + 1 +
                                                         encoder_input_weights.size()[1]))
        to_be_added_encoder_input_weights = torch.tensor(
            to_be_added_encoder_input_weights,
            device=encoder_input_weights.get_device()).float()
        network.z_encoder.encoder.fc_layers.Layer0.L.cond_L.weight.data = torch.cat(
            (network.z_encoder.encoder.fc_layers.Layer0.L.cond_L.weight, to_be_added_encoder_input_weights), 1)

        # Expand first Layer weights of decoder of old network by new conditions
        decoder_input_weights = network.decoder.px_decoder.fc_layers.Layer0.L.cond_L.weight
        to_be_added_decoder_input_weights = np.random.randn(decoder_input_weights.size()[0], n_new_conditions) * \
                                            np.sqrt(2 / (decoder_input_weights.size()[0] + 1 +
                                                         decoder_input_weights.size()[1]))
        to_be_added_decoder_input_weights = torch.tensor(
            to_be_added_decoder_input_weights,
            device=decoder_input_weights.get_device()).float()
        network.decoder.px_decoder.fc_layers.Layer0.L.cond_L.weight.data = torch.cat(
            (network.decoder.px_decoder.fc_layers.Layer0.L.cond_L.weight, to_be_added_decoder_input_weights), 1)
    else:
        for layer in network.decoder.px_decoder.fc_layers:
            decoder_input_weights = layer.L.cond_L.weight
            to_be_added_decoder_input_weights = np.random.randn(decoder_input_weights.size()[0], n_new_conditions) * \
                                                np.sqrt(2 / (decoder_input_weights.size()[0] + 1 +
                                                             decoder_input_weights.size()[1]))
            to_be_added_decoder_input_weights = torch.tensor(
                to_be_added_decoder_input_weights,
                device=decoder_input_weights.get_device()).float()
            layer.L.cond_L.weight.data = torch.cat(
                (layer.L.cond_L.weight, to_be_added_decoder_input_weights), 1)

    # Set the weights of new network to old network weights
    op_network.load_state_dict(network.state_dict())

    # Freeze parts of the network
    if freeze:
        op_network.freeze = True
        for name, p in op_network.named_parameters():
            p.requires_grad = False

            if freeze_expression:
                if network.modified:
                    if 'cond_L.weight' in name and ('z_encoder' in name or 'px_decoder' in name):
                        p.requires_grad = True
                    if 'l_encoder' in name:
                        p.requires_grad = True
                else:
                    if 'cond_L.weight' in name and ('z_encoder' in name or 'px_decoder' in name):
                        p.requires_grad = True
                    if 'z_encoder' in name and 'Layer0' in name:
                        p.requires_grad = True
                    if 'l_encoder' in name:
                        p.requires_grad = True
            else:
                if network.modified:
                    if ('z_encoder' in name or 'px_decoder' in name) and 'Layer0' in name:
                        p.requires_grad = True
                    if 'l_encoder' in name:
                        p.requires_grad = True
                else:
                    if 'z_encoder' in name and 'Layer0' in name:
                        p.requires_grad = True
                    if 'px_decoder' in name:
                        p.requires_grad = True

    # Retrain Networks
    if type(network) is scVI:
        op_trainer = scVITrainer(
            op_network,
            adata,
            train_size=0.9,
            use_cuda=True,
            frequency=1,
            early_stopping_kwargs=early_stopping_kwargs
        )
        op_trainer.train(n_epochs=n_epochs, lr=1e-3)
    if type(network) is scANVI:
        if labels_per_class == 0:
            op_trainer = UnlabelledScanviTrainer(
                op_network,
                adata,
                n_labelled_samples_per_class=labels_per_class,
                train_size=0.9,
                use_cuda=True,
                frequency=1,
                early_stopping_kwargs=early_stopping_kwargs_scanvi
            )
        else:
            op_trainer = scANVITrainer(
                op_network,
                adata,
                n_labelled_samples_per_class=labels_per_class,
                classification_ratio=50,
                train_size=0.9,
                use_cuda=True,
                frequency=1,
                early_stopping_kwargs=early_stopping_kwargs_scanvi
            )

        op_trainer.train(n_epochs=n_epochs, lr=1e-3)

    weight_update_check(network, op_network)

    return op_network, op_trainer, adata
