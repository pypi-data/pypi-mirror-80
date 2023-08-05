import numpy as np
from typing import Union
import torch
import scanpy as sc

from scarchest.models import MARS
from scarchest.trainers import MARSTrainer


def mars_operate(network: MARS,
                 new_adata: sc.AnnData,
                 new_tasks: Union[list, str],
                 meta_tasks: list,
                 n_clusters: int,
                 task_key: str,
                 cell_type_key: str,
                 tau: float = 0.2,
                 eta: float = 1.0,
                 freeze: bool = True,
                 remove_dropout: bool = True,
                 ) -> MARS:
    """Transfer Learning function for new data. Uses old trained Network and expands it for new conditions.
       Parameters
       ----------
       network: MARS
            A MARS model object.
       new_tasks: list_str
            List of Strings of new Conditions.
       freeze: Boolean
            If 'True' freezes every part of the network except the first layers of encoder/decoder.
       remove_dropout: Boolean
            If 'True' remove Dropout for Transfer Learning.
       Returns
       -------
       new_network: MARS
            New expanded network with old weights for Transfer Learning.
    """
    conditions = network.conditions
    new_conditions = []

    # Check if new conditions are already known
    for item in new_tasks:
        if item not in conditions:
            new_conditions.append(item)

    n_new_conditions = len(new_conditions)

    # Add new conditions to overall conditions
    for condition in new_conditions:
        conditions.append(condition)

    # Update DR Rate
    new_dr = network.dropout_rate
    if remove_dropout:
        new_dr = 0.0

    new_network = MARS(
        x_dim=network.x_dim,
        architecture=network.architecture,
        z_dim=network.z_dim,
        conditions=conditions,
        alpha=network.alpha,
        activation=network.activation,
        output_activation=network.output_activation,
        use_batchnorm=network.use_batchnorm,
        dropout_rate=new_dr,
    )

    # Expand First Layer weights of encoder/decoder of old network by new conditions
    encoder_input_weights = network.encoder[0].FC_0.weight
    to_be_added_encoder_input_weights = np.random.randn(encoder_input_weights.size()[0], n_new_conditions) * np.sqrt(
        2 / (encoder_input_weights.size()[0] + 1 + encoder_input_weights.size()[1]))
    to_be_added_encoder_input_weights = torch.from_numpy(to_be_added_encoder_input_weights).float().to(network.device)
    new_encoder_input_weights = torch.cat((encoder_input_weights, to_be_added_encoder_input_weights), 1)
    network.encoder[0].FC_0.weight.data = new_encoder_input_weights

    decoder_input_weights = network.decoder[0].FC_0.weight
    to_be_added_decoder_input_weights = np.random.randn(decoder_input_weights.size()[0], n_new_conditions) * np.sqrt(
        2 / (decoder_input_weights.size()[0] + 1 + decoder_input_weights.size()[1]))
    to_be_added_decoder_input_weights = torch.from_numpy(to_be_added_decoder_input_weights).float().to(network.device)
    new_decoder_input_weights = torch.cat((decoder_input_weights, to_be_added_decoder_input_weights), 1)
    network.decoder[0].FC_0.weight.data = new_decoder_input_weights

    # Set the weights of new network to old network weights
    new_network.load_state_dict(network.state_dict())

    # Freeze parts of the network
    if freeze:
        for name, p in new_network.named_parameters():
            if "FC_0" not in name:
                p.requires_grad = False

    new_trainer = MARSTrainer(model=new_network,
                              adata=new_adata,
                              task_key=task_key,
                              meta_test_tasks=meta_tasks,
                              cell_type_key=cell_type_key,
                              n_clusters=n_clusters,
                              tau=tau,
                              eta=eta,
                              )

    return new_network, new_trainer
