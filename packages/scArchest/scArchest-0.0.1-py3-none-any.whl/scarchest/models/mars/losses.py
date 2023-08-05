import torch
import numpy as np
from functools import partial
from torch.autograd import Variable

def kl(mu, logvar):
    """Computes KL loss between tensor of means, log. variances and zero mean, unit variance.

       Parameters
       ----------
       mu: Tensor
            Torch Tensor of means
       logvar: Tensor
            Torch Tensor of log. variances

       Returns
       -------
       KL loss value
    """
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp(), )
    kl_loss = kl_loss / mu.size(0)
    return kl_loss


def mse(recon_x, x):
    """Computes MSE loss between reconstructed data and ground truth data.

       Parameters
       ----------
       recon_x: Tensor
            Torch Tensor of reconstructed data
       x: Tensor
            Torch Tensor of ground truth data

       Returns
       -------
       MSE loss value
    """
    mse_loss = torch.nn.functional.mse_loss(recon_x, x, reduction="mean")
    return mse_loss

