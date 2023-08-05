import torch
import numpy as np
from functools import partial
from torch.autograd import Variable

from ._utils import partition


def _nan2inf(x):
    return torch.where(torch.isnan(x), torch.zeros_like(x) + np.inf, x)


def _nan2zero(x):
    return torch.where(torch.isnan(x), torch.zeros_like(x), x)


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


def nb(x, mu, theta, eps=1e-8, mean=True):
    """Computes negative binomial loss.

       Parameters
       ----------
       x: Tensor
            Torch Tensor of ground truth data.
       mu: Tensor
            Torch Tensor of means of the negative binomial (has to be positive support).
       theta: Tensor
            Torch Tensor of inverse dispersion parameter (has to be positive support).
       eps: Float
            numerical stability constant.
       mean: boolean
            If 'True' NB loss value gets returned, if 'False' NB loss Tensor gets returned with same shape as 'x'
            (needed for ZINB loss calculation).

       Returns
       -------
       If 'mean' is 'True' NB loss value gets returned, otherwise Torch tensor of losses gets returned.
    """

    if theta.ndimension() == 1:
        theta = theta.view(1, theta.size(0))  # In this case, we reshape theta for broadcasting
    t1 = torch.lgamma(theta + eps) + torch.lgamma(x + 1.0) - torch.lgamma(x + theta + eps)
    t2 = (theta + x) * torch.log(1.0 + (mu / (theta + eps))) + (x * (torch.log(theta + eps) - torch.log(mu + eps)))
    final = t1 + t2
    final = _nan2inf(final)
    if mean:
        final = torch.mean(final)
    return final


def zinb(x, mu, theta, pi, eps=1e-8, ridge_lambda=0.0, mean=True):
    """Computes zero inflated negative binomial loss.

       Parameters
       ----------
       x: Tensor
            Torch Tensor of ground truth data.
       mu: Tensor
            Torch Tensor of means of the negative binomial (has to be positive support).
       theta: Tensor
            Torch Tensor of inverses dispersion parameter (has to be positive support).
       pi: Tensor
            Torch Tensor of logits of the dropout parameter (real support)
       eps: Float
            numerical stability constant.
       ridge_lambda: Float
            Ridge Coefficient.
       mean: boolean
            If 'True' NB loss value gets returned, if 'False' NB loss Tensor gets returned with same shape as 'x'
            (needed for ZINB loss calculation).

       Returns
       -------
       If 'mean' is 'True' ZINB loss value gets returned, otherwise Torch tensor of losses gets returned.
    """

    nb_case = nb(x, mu, theta, mean=False) - torch.log(1.0 - pi + eps)

    if theta.ndimension() == 1:
        theta = theta.view(1, theta.size(0))  # In this case, we reshape theta for broadcasting

    zero_nb = torch.pow(theta / (theta + mu + eps), theta)
    zero_case = -torch.log(pi + ((1.0 - pi) * zero_nb) + eps)
    result = torch.where((x < 1e-8), zero_case, nb_case)
    ridge = ridge_lambda * torch.square(pi)
    result += ridge
    if mean:
        result = torch.mean(result)

    result = _nan2inf(result)

    return result


def pairwise_distance(x, y):

    if not len(x.shape) == len(y.shape) == 2:
        raise ValueError('Both inputs should be matrices.')

    if x.shape[1] != y.shape[1]:
        raise ValueError('The number of features should be the same.')

    x = x.view(x.shape[0], x.shape[1], 1)
    y = torch.transpose(y, 0, 1)
    output = torch.sum((x - y) ** 2, 1)
    output = torch.transpose(output, 0, 1)

    return output


def gaussian_kernel_matrix(x, y, sigmas):
    """Computes multiscale-RBF kernel between x and y.

       Parameters
       ----------
       x: Tensor
            Tensor with shape [batch_size, z_dim].
       y: Tensor
            Tensor with shape [batch_size, z_dim].
       sigmas: Tensor

       Returns
       -------
       Returns the computed multiscale-RBF kernel between x and y.
    """

    sigmas = sigmas.view(sigmas.shape[0], 1)
    beta = 1. / (2. * sigmas)
    dist = pairwise_distance(x, y).contiguous()
    dist_ = dist.view(1, -1)
    s = torch.matmul(beta, dist_)

    return torch.sum(torch.exp(-s), 0).view_as(dist)


def maximum_mean_discrepancy(x, y, kernel=gaussian_kernel_matrix):
    """Computes Maximum Mean Discrepancy(MMD) between x and y.

       Parameters
       ----------
       x: Tensor
            Tensor with shape [batch_size, z_dim]
       y: Tensor
            Tensor with shape [batch_size, z_dim]
       kernel: gaussian_kernel_matrix

       Returns
       -------
       Returns the computed MMD between x and y.
    """

    cost = torch.mean(kernel(x, x))
    cost += torch.mean(kernel(y, y))
    cost -= 2 * torch.mean(kernel(x, y))

    return cost


def mmd_loss_calc(source_features, target_features):
    """Initializes Maximum Mean Discrepancy(MMD) between source_features and target_features.

       Parameters
       ----------
       source_features: Tensor
            Tensor with shape [batch_size, z_dim]
       target_features: Tensor
            Tensor with shape [batch_size, z_dim]

       Returns
       -------
       Returns the computed MMD between x and y.
    """

    sigmas = [
        1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 5, 10, 15, 20, 25, 30, 35, 100,
        1e3, 1e4, 1e5, 1e6
    ]
    if torch.cuda.is_available():
        gaussian_kernel = partial(
            gaussian_kernel_matrix, sigmas=Variable(torch.cuda.FloatTensor(sigmas))
        )
    else:
        gaussian_kernel = partial(
            gaussian_kernel_matrix, sigmas=Variable(torch.FloatTensor(sigmas))
        )
    loss_value = maximum_mean_discrepancy(source_features, target_features, kernel=gaussian_kernel)

    return loss_value


def mmd(n_conditions, beta, boundary):
    """Initializes Maximum Mean Discrepancy(MMD) between every different condition.

       Parameters
       ----------
       n_conditions: integer
            Number of classes (conditions) the data contain.
       beta: float
            beta coefficient for MMD loss.
       boundary: integer
            If not 'None', mmd loss is only calculated on #new conditions.
       y: Tensor
            Torch Tensor of computed latent data.
       c: Tensor
            Torch Tensor of labels

       Returns
       -------
       Returns MMD loss.
    """
    def mmd_loss(y, c):
        # partition separates y into num_cls subsets w.r.t. their labels c
        conditions_mmd = partition(y, c, n_conditions)
        loss = 0.0
        if boundary is not None:
            for i in range(boundary):
                for j in range(boundary, n_conditions):
                    if conditions_mmd[i].size(0) < 2 or conditions_mmd[j].size(0) < 2:
                        continue
                    loss += mmd_loss_calc(conditions_mmd[i], conditions_mmd[j])
        else:
            for i in range(len(conditions_mmd)):
                if conditions_mmd[i].size(0) < 1:
                    continue
                for j in range(i):
                    if conditions_mmd[j].size(0) < 1 or i == j:
                        continue
                    loss += mmd_loss_calc(conditions_mmd[i], conditions_mmd[j])
        return beta * loss

    return mmd_loss
