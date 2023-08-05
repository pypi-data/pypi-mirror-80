from typing import Optional

import torch
import torch.nn as nn

from .modules import Encoder, Decoder
from .losses import mse, mmd, zinb, nb, kl


class trVAE(nn.Module):
    """scNet class. This class contains the implementation of Conditional Variational Auto-encoder.

       Parameters
       ----------
       input_dim: integer
            Number of input features (i.e. gene in case of scRNA-seq).
       conditions: integer
            Number of classes (conditions) the data contain. if `None` the model will be a normal VAE instead of
            conditional VAE.
       encoder_layer_sizes: List
            A list of hidden layer sizes for encoder network.
       latent_dim: integer
            Bottleneck layer (z)  size.
       decoder_layer_sizes: List
            A list of hidden layer sizes for decoder network.
       recon_loss: String
            Definition of Reconstruction-Loss-Method, 'mse', 'nb' or 'zinb'.
       alpha: float
            Alpha coefficient for KL loss.
       use_batch_norm: boolean
            If `True` batch normalization will applied to hidden layers.
       dr_rate: float
            Dropput rate applied to all layers, if `dr_rate`==0 no dropput will be applied.
       use_mmd: boolean
            If `True` then MMD will be applied to first decoder layer.
       beta: float
            beta coefficient for MMD loss.
       eta: float
            Eta coefficient for Reconstruction loss.
       calculate_mmd: String
            Defines the layer which the mmd loss is calculated on, 'y' for first layer of decoder or 'z' for bottleneck
            layer.
    """

    def __init__(self,
                 input_dim: int,
                 conditions: list,
                 encoder_layer_sizes: list = [256, 64],
                 latent_dim: int = 32,
                 decoder_layer_sizes: list = [64, 256],
                 dr_rate: float = 0.05,
                 use_batch_norm: bool = False,
                 calculate_mmd: Optional[str] = 'z',
                 mmd_boundary: Optional[int] = None,
                 recon_loss: Optional[str] = 'zinb',
                 alpha: Optional[float] = 0.0005,
                 beta: Optional[float] = 200,
                 eta: Optional[float] = 5000):
        super().__init__()
        assert isinstance(encoder_layer_sizes, list)
        assert isinstance(latent_dim, int)
        assert isinstance(decoder_layer_sizes, list)
        assert isinstance(conditions, list)
        assert recon_loss in ["mse", "nb", "zinb"], "'recon_loss' must be 'mse', 'nb' or 'zinb'"
        assert calculate_mmd in [None, "y", "z"], "'calculate_mmd' must be None, 'y' or 'z'"

        print("\nINITIALIZING NEW NETWORK..............")
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.n_conditions = len(conditions)
        self.conditions = conditions
        self.condition_encoder = {k: v for k, v in zip(conditions, range(len(conditions)))}
        self.recon_loss = recon_loss

        self.alpha = alpha
        self.beta = beta
        self.eta = eta

        self.dr_rate = dr_rate
        if self.dr_rate > 0:
            self.use_dr = True
        else:
            self.use_dr = False

        self.use_bn = use_batch_norm
        self.calculate_mmd = calculate_mmd
        self.mmd_boundary = mmd_boundary
        self.use_mmd = True if self.calculate_mmd in ['z', 'y'] else False

        self.enc_layer_sizes = encoder_layer_sizes.copy()
        self.dec_layer_sizes = decoder_layer_sizes.copy()
        encoder_layer_sizes.insert(0, self.input_dim)
        decoder_layer_sizes.append(self.input_dim)
        self.encoder = Encoder(encoder_layer_sizes, self.latent_dim,
                               self.use_bn, self.use_dr, self.dr_rate, self.n_conditions)
        self.decoder = Decoder(decoder_layer_sizes, self.latent_dim, self.recon_loss, self.use_bn, self.use_dr,
                               self.dr_rate, self.use_mmd, self.n_conditions)

        self.freeze = False


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

    def generate_with_condition(self, n_samples, c=None):
        z = torch.randn([n_samples, self.latent_dim])
        if c is not None:
            c = torch.ones([n_samples, 1], device=self.device) * c
        output = self.decoder(z, c)
        # If recon Loss is zinb, how to get recon_x?
        return output

    def get_latent(self, x, c=None, mean=False):
        """Map `x` in to the latent space. This function will feed data in encoder  and return  z for each sample in
           data.

           Parameters
           ----------
           x:  numpy nd-array
                Numpy nd-array to be mapped to latent space. `x` has to be in shape [n_obs, input_dim].
           c: `numpy nd-array`
                `numpy nd-array` of original desired labels for each sample.
           mean: boolean

           Returns
           -------
                Returns array containing latent space encoding of 'x'.
        """

        if c is not None:
            c = torch.tensor(c, device=self.device)
        x = torch.tensor(x, device=self.device)
        z_mean, z_log_var = self.encoder(x, c)
        latent = self.sampling(z_mean, z_log_var)
        if mean:
            return z_mean
        return latent.cpu().data.numpy()

    def get_y(self, x, c=None):
        """Map `x` in to the y dimension (First Layer of Decoder). This function will feed data in encoder  and return
           y for each sample in data.

           Parameters
           ----------
           x:  numpy nd-array
                Numpy nd-array to be mapped to latent space. `x` has to be in shape [n_obs, input_dim].
           c: `numpy nd-array`
                `numpy nd-array` of original desired labels for each sample.

           Returns
           -------
           Returns array containing latent space encoding of 'x'
        """

        if c is not None:
            c = torch.tensor(c).to(self.device)
        x = torch.tensor(x).to(self.device)
        z_mean, z_log_var = self.encoder(x, c)
        latent = self.sampling(z_mean, z_log_var)
        output = self.decoder(latent, c)
        return output[-1].cpu().data.numpy()

    def calc_recon_binomial_loss(self, outputs, x_raw, size_factor):
        dec_mean_gamma = outputs["dec_mean_gamma"]
        size_factor_view = size_factor.unsqueeze(1).expand(dec_mean_gamma.size(0), dec_mean_gamma.size(1))
        dec_mean = dec_mean_gamma * size_factor_view
        if outputs["dec_dropout"] is None:
            recon_loss = nb(x_raw, dec_mean, outputs["dec_disp"])
        else:
            recon_loss = zinb(x_raw, dec_mean, outputs["dec_disp"], outputs["dec_dropout"])

        return recon_loss

    def inference(self, x, c=None):
        z1_mean, z1_log_var = self.encoder(x, c)
        z1 = self.sampling(z1_mean, z1_log_var)
        outputs = self.decoder(z1, c)
        recon_x = dec_mean_gamma = dec_dropout = dec_disp = y1 = None
        if self.recon_loss == "mse":
            recon_x, y1 = outputs
        if self.recon_loss == "zinb":
            dec_mean_gamma, dec_dropout, dec_disp, y1 = outputs
        if self.recon_loss == "nb":
            dec_mean_gamma, dec_disp, y1 = outputs
        return dict(
            z1_mean=z1_mean,
            z1_log_var=z1_log_var,
            z1=z1,
            y1=y1,
            recon_x=recon_x,
            dec_mean_gamma=dec_mean_gamma,
            dec_dropout=dec_dropout,
            dec_disp=dec_disp,
        )

    def forward(self, x=None, raw=None, f=None, c=None, y=None):
        outputs = self.inference(x, c)
        if outputs["recon_x"] is not None:
            recon_loss = mse(outputs["recon_x"], x)
        else:
            recon_loss = self.calc_recon_binomial_loss(outputs, raw, f)
        recon_loss *= self.eta

        kl_div = kl(outputs["z1_mean"], outputs["z1_log_var"])
        kl_loss = self.alpha * kl_div
        mmd_loss = 0
        if self.calculate_mmd is not None:
            mmd_calculator = mmd(self.n_conditions, self.beta, self.mmd_boundary)
            if self.calculate_mmd == "z":
                mmd_loss = mmd_calculator(outputs["z1"], c)
            else:
                mmd_loss = mmd_calculator(outputs["y1"], c)
        return recon_loss, kl_loss, mmd_loss
