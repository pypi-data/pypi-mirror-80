import numpy as np
from typing import Union
import torch

from scarchest.models.trvae.trvae import trVAE


def trvae_operate(network: trVAE,
                  data_conditions: Union[list, str],
                  freeze: bool = True,
                  freeze_expression: bool = True,
                  remove_dropout: bool = True,
                  ) -> trVAE:
    """Transfer Learning function for new data. Uses old trained Network and expands it for new conditions.
       Parameters
       ----------
       network: trVAE
            A scNet model object.
       data_conditions: list_str
            List of Strings of new Conditions.
       freeze: Boolean
            If 'True' freezes every part of the network except the first layers of encoder/decoder.
       remove_dropout: Boolean
            If 'True' remove Dropout for Transfer Learning.
       Returns
       -------
       new_network: trVAE
            New expanded network with old weights for Transfer Learning.
    """
    conditions = network.conditions
    new_conditions = []

    # Check if new conditions are already known
    for item in data_conditions:
        if item not in conditions:
            new_conditions.append(item)

    n_new_conditions = len(new_conditions)

    # Add new conditions to overall conditions
    for condition in new_conditions:
        conditions.append(condition)

    # Update DR Rate
    new_dr = network.dr_rate
    if remove_dropout:
        new_dr = 0.0
    new_network = trVAE(
        network.input_dim,
        conditions=conditions,
        encoder_layer_sizes=network.enc_layer_sizes,
        latent_dim=network.latent_dim,
        decoder_layer_sizes=network.dec_layer_sizes,
        recon_loss=network.recon_loss,
        alpha=network.alpha,
        use_batch_norm=network.use_bn,
        dr_rate=new_dr,
        beta=network.beta,
        eta=network.eta,
        calculate_mmd=network.calculate_mmd,
        mmd_boundary=network.mmd_boundary
    )

    # Expand First Layer weights of encoder/decoder of old network by new conditions
    encoder_input_weights = network.encoder.FC.L0.cond_L.weight
    to_be_added_encoder_input_weights = np.random.randn(encoder_input_weights.size()[0], n_new_conditions) * np.sqrt(
        2 / (encoder_input_weights.size()[0] + 1 + encoder_input_weights.size()[1]))
    to_be_added_encoder_input_weights = torch.from_numpy(to_be_added_encoder_input_weights).float().to(network.device)
    new_encoder_input_weights = torch.cat((encoder_input_weights, to_be_added_encoder_input_weights), 1)
    network.encoder.FC.L0.cond_L.weight.data = new_encoder_input_weights

    decoder_input_weights = network.decoder.FirstL.L0.cond_L.weight
    to_be_added_decoder_input_weights = np.random.randn(decoder_input_weights.size()[0], n_new_conditions) * np.sqrt(
        2 / (decoder_input_weights.size()[0] + 1 + decoder_input_weights.size()[1]))
    to_be_added_decoder_input_weights = torch.from_numpy(to_be_added_decoder_input_weights).float().to(network.device)
    new_decoder_input_weights = torch.cat((decoder_input_weights, to_be_added_decoder_input_weights), 1)
    network.decoder.FirstL.L0.cond_L.weight.data = new_decoder_input_weights

    # Set the weights of new network to old network weights
    new_network.load_state_dict(network.state_dict())

    # Freeze parts of the network
    if freeze:
        new_network.freeze = True
        for name, p in new_network.named_parameters():
            p.requires_grad = False
            if freeze_expression:
                if 'cond_L.weight' in name:
                    p.requires_grad = True
            else:
                if "L0" in name or "B0" in name:
                    p.requires_grad = True

    return new_network
