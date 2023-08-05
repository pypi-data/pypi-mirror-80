from typing import Optional

import torch
import torch.nn as nn

from scarchest.models.trvae._utils import one_hot_encoder
from .activations import ACTIVATIONS
from .losses import mse, kl
import numpy as np


def dense_block(i, in_features, out_features, use_batchnorm, dropout_rate, activation):
    model = nn.Sequential()

    model.add_module(name=f"FC_{i}",
                     module=nn.Linear(in_features, out_features, bias=False))
    if use_batchnorm:
        model.add_module(f"BN_{i}", module=nn.BatchNorm1d(out_features, affine=True))

    model.add_module(name=f"ACT_{i}", module=ACTIVATIONS[activation])

    if dropout_rate > 0:
        model.add_module(name=f"DR_{i}", module=nn.Dropout(p=dropout_rate))

    return model


class MARS(nn.Module):
    def __init__(self, x_dim: int,
                 conditions: Optional[list] = [],
                 architecture: list = [128, 32],
                 z_dim: int = 10,
                 alpha=1e-3,
                 activation: str = 'elu',
                 output_activation: str = 'relu',
                 use_batchnorm: bool = False,
                 dropout_rate: float = 0.2):
        super(MARS, self).__init__()

        self.x_dim = x_dim
        self.conditions = conditions if isinstance(conditions, list) else []
        self.n_conditions = len(self.conditions)
        self.condition_encoder = {k: v for k, v in zip(self.conditions, range(self.n_conditions))}
        self.z_dim = z_dim
        self.alpha = alpha
        self.architecture = architecture
        self.use_batchnorm = use_batchnorm
        self.dropout_rate = dropout_rate
        self.activation = activation
        self.output_activation = output_activation

        self.encoder_architecture = [self.x_dim + self.n_conditions] + self.architecture
        self.decoder_architecture = [self.z_dim + self.n_conditions] + list(reversed(self.architecture))

        self.encoder = nn.Sequential(
            *[dense_block(i, in_size, out_size, use_batchnorm, dropout_rate, activation) for i, (in_size, out_size) in
              enumerate(zip(self.encoder_architecture[:-1], self.encoder_architecture[1:]))])

        self.mean = nn.Linear(self.encoder_architecture[-1], self.z_dim)
        self.log_var = nn.Linear(self.encoder_architecture[-1], self.z_dim)

        self.decoder = nn.Sequential(
            *[dense_block(i, in_size, out_size, use_batchnorm, dropout_rate, activation) for i, (in_size, out_size) in
              enumerate(zip(self.decoder_architecture[:-1], self.decoder_architecture[1:]))])

        self.decoder.add_module(name='X_hat',
                                module=dense_block('X_hat', self.decoder_architecture[-1], self.x_dim, use_batchnorm,
                                                   dropout_rate, self.output_activation))

    def sampling(self, mu, log_var):
        """Samples from standard Normal distribution and applies re-parametrization trick.
           It is actually sampling from latent space distributions with N(mu, var), computed by encoder.

           Parameters
           ----------
           mu: torch.Tensor
                Torch Tensor of Means.
           log_var: torch.Tensor
                Torch Tensor of log. variances.

           Returns
           -------
           Torch Tensor of sampled data.
        """

        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return eps.mul(std).add(mu)

    def forward(self, x, c=None):
        if c is not None:
            c = one_hot_encoder(c, n_cls=self.n_conditions)
            xc = torch.cat((x, c), dim=-1)
        else:
            xc = x

        encoded = self.encoder(xc)
        mean_encoded = self.mean(encoded)
        log_var_encoded = self.log_var(encoded)
        encoded = self.sampling(mean_encoded, log_var_encoded)

        if c is not None:
            ec = torch.cat((encoded, c), dim=-1)
        else:
            ec = encoded

        decoded = self.decoder(ec)

        kl_loss = kl(mean_encoded, log_var_encoded)

        recon_loss = mse(decoded, x)  # TODO: support other loss functions
        loss = recon_loss + self.alpha * kl_loss

        return encoded, decoded, loss, recon_loss, kl_loss

    def get_latent(self, x, c=None):
        x = torch.as_tensor(np.array(x).astype(np.float)).type(torch.float32)
        if c is not None:
            c = torch.as_tensor(np.array(c).astype(np.int))
            c = one_hot_encoder(c, n_cls=self.n_conditions)
            xc = torch.cat((x, c), dim=-1)
        else:
            xc = x
        encoded = self.encoder(xc)
        mean_encoded = self.mean(encoded)
        log_var_encoded = self.log_var(encoded)
        encoded = self.sampling(mean_encoded, log_var_encoded)
        return encoded.cpu().data.numpy()

