import torch
import torch.nn as nn

from ._utils import one_hot_encoder


class CondLayers(nn.Module):
    def __init__(
            self,
            n_in: int,
            n_out: int,
            n_cond: int,
            bias: bool = True,
    ):
        super().__init__()
        self.n_cond = n_cond
        self.expr_L = nn.Linear(n_in, n_out, bias=bias)
        if self.n_cond != 0:
            self.cond_L = nn.Linear(self.n_cond, n_out, bias=False)

    def forward(self, x: torch.Tensor):
        if self.n_cond == 0:
            out = self.expr_L(x)
        else:
            expr, cond = torch.split(x, x.shape[1] - self.n_cond, dim=1)
            out = self.expr_L(expr) + self.cond_L(cond)
        return out


class Encoder(nn.Module):
    """Scnet Encoder class. Constructs the encoder sub-network of scNet. It will transform primary space input to means
       and log. variances of latent space with n_dimensions = z_dimension.

       Parameters
       ----------
       layer_sizes: List
            List of first and hidden layer sizes
       latent_dim: Integer
            Bottleneck layer (z)  size.
       use_bn: Boolean
            If `True` batch normalization will applied to layers.
       use_dr: Boolean
            If `True` dropout will applied to layers.
       dr_rate: Float
            Dropput rate applied to all layers, if `dr_rate`==0 no dropput will be applied.
       num_classes: Integer
            Number of classes (conditions) the data contain. if `None` the model will be a normal VAE instead of
            conditional VAE.

       Returns
       -------
    """
    def __init__(self, layer_sizes, latent_dim,
                 use_bn, use_dr, dr_rate, num_classes=None):
        super().__init__()
        self.n_classes = 0
        if num_classes is not None:
            self.n_classes = num_classes
        self.FC = None
        if len(layer_sizes) > 1:
            print("Encoder Architecture:")
            self.FC = nn.Sequential()
            for i, (in_size, out_size) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
                if i == 0:
                    print("\tInput Layer in, out and cond:", in_size, out_size, self.n_classes)
                    self.FC.add_module(name="L{:d}".format(i), module=CondLayers(in_size,
                                                                                 out_size,
                                                                                 self.n_classes,
                                                                                 bias=False))
                else:
                    print("\tHidden Layer", i, "in/out:", in_size, out_size)
                    self.FC.add_module(name="L{:d}".format(i), module=nn.Linear(in_size, out_size, bias=False))
                if use_bn:
                    self.FC.add_module("B{:d}".format(i), module=nn.BatchNorm1d(out_size, affine=True))
                self.FC.add_module(name="A{:d}".format(i), module=nn.ReLU())
                if use_dr:
                    self.FC.add_module(name="D{:d}".format(i), module=nn.Dropout(p=dr_rate))
        print("\tMean/Var Layer in/out:", layer_sizes[-1], latent_dim)
        self.mean_encoder = nn.Linear(layer_sizes[-1], latent_dim)
        self.log_var_encoder = nn.Linear(layer_sizes[-1], latent_dim)

    def forward(self, x, c=None):
        if c is not None:
            c = one_hot_encoder(c, n_cls=self.n_classes)
            x = torch.cat((x, c), dim=-1)
        if self.FC is not None:
            x = self.FC(x)
        means = self.mean_encoder(x)
        log_vars = self.log_var_encoder(x)
        return means, log_vars


class Decoder(nn.Module):
    """Scnet Decoder class. Constructs the decoder sub-network of scNet. It will transform constructed latent space to
       the previous space of data with n_dimensions = x_dimension.

       Parameters
       ----------
       layer_sizes: List
            List of hidden and last layer sizes
       latent_dim: Integer
            Bottleneck layer (z)  size.
       recon_loss: String
            Definition of Reconstruction-Loss-Method, 'mse', 'nb' or 'zinb'.
       use_bn: Boolean
            If `True` batch normalization will applied to layers.
       use_dr: Boolean
            If `True` dropout will applied to layers.
       dr_rate: Float
            Dropput rate applied to all layers, if `dr_rate`==0 no dropput will be applied.
       use_mmd: boolean
            If `True` then MMD will be applied to first decoder layer.
       num_classes: Integer
            Number of classes (conditions) the data contain. if `None` the model will be a normal VAE instead of
            conditional VAE.
       output_active: String
            Defines the Activation for the last layer of decoder if 'recon_loss' is 'mse'.

       Returns
       -------
    """
    def __init__(self, layer_sizes, latent_dim, recon_loss, use_bn, use_dr, dr_rate, use_mmd=False, num_classes=None):
        super().__init__()
        self.use_mmd = use_mmd
        self.use_bn = use_bn
        self.use_dr = use_dr
        self.recon_loss = recon_loss
        self.n_classes = 0
        if num_classes is not None:
            self.n_classes = num_classes
        layer_sizes = [latent_dim] + layer_sizes
        print("Decoder Architecture:")
        # Create first Decoder layer
        self.FirstL = nn.Sequential()
        print("\tFirst Layer in/out: ", layer_sizes[0], layer_sizes[1])
        self.FirstL.add_module(name="L0", module=CondLayers(layer_sizes[0], layer_sizes[1], self.n_classes, bias=False))
        if self.use_bn:
            self.FirstL.add_module("B0", module=nn.BatchNorm1d(layer_sizes[1], affine=True))
        self.FirstL.add_module(name="A0", module=nn.ReLU())
        if self.use_dr:
            self.FirstL.add_module(name="D0", module=nn.Dropout(p=dr_rate))

        # Create all Decoder hidden layers
        if len(layer_sizes) > 2:
            self.HiddenL = nn.Sequential()
            for i, (in_size, out_size) in enumerate(zip(layer_sizes[1:-1], layer_sizes[2:])):
                if i+3 < len(layer_sizes):
                    print("\tHidden Layer", i+1, "in/out:", in_size, out_size)
                    self.HiddenL.add_module(name="L{:d}".format(i+1), module=nn.Linear(in_size, out_size, bias=False))
                    if self.use_bn:
                        self.HiddenL.add_module("B{:d}".format(i+1), module=nn.BatchNorm1d(out_size, affine=True))
                    self.HiddenL.add_module(name="A{:d}".format(i+1), module=nn.ReLU())
                    if self.use_dr:
                        self.HiddenL.add_module(name="D{:d}".format(i+1), module=nn.Dropout(p=dr_rate))
        else:
            self.HiddenL = None

        # Create Output Layers
        print("\tOutput Layer in/out: ", layer_sizes[-2], layer_sizes[-1], "\n")
        if self.recon_loss == "mse":
            self.OutputLayer = nn.Sequential()
            self.OutputLayer.add_module(name="outputL", module=nn.Linear(layer_sizes[-2], layer_sizes[-1]))
            self.OutputLayer.add_module(name="outputA", module=nn.ReLU())
        if self.recon_loss == "zinb":
            # mean gamma
            self.mean_decoder = nn.Linear(layer_sizes[-2], layer_sizes[-1])
            # dispersion: here we only deal with gene-cell dispersion case
            self.disp_decoder = nn.Sequential(nn.Linear(layer_sizes[-2], layer_sizes[-1]), nn.Softplus())
            # dropout
            self.dropout_decoder = nn.Sequential(nn.Linear(layer_sizes[-2], layer_sizes[-1]), nn.Sigmoid())
        if self.recon_loss == "nb":
            # mean gamma
            self.mean_decoder = nn.Linear(layer_sizes[-2], layer_sizes[-1])
            # dispersion: here we only deal with gene-cell dispersion case
            self.disp_decoder = nn.Sequential(nn.Linear(layer_sizes[-2], layer_sizes[-1]), nn.Softplus())

    def forward(self, z, c=None):
        # Add Condition Labels to Decoder Input
        if c is not None:
            c = one_hot_encoder(c, n_cls=self.n_classes)
            z_cat = torch.cat((z, c), dim=-1)
            dec_latent = self.FirstL(z_cat)
        else:
            dec_latent = self.FirstL(z)

        # Compute Hidden Output
        if self.HiddenL is not None:
            x = self.HiddenL(dec_latent)
        else:
            x = dec_latent

        # Compute Decoder Output
        if self.recon_loss == "mse":
            output = self.OutputLayer(x)
            return output, dec_latent
        if self.recon_loss == "zinb":
            # Parameters for ZINB and NB
            dec_mean_gamma = self.mean_decoder(x)
            dec_mean_gamma = torch.clamp(torch.exp(dec_mean_gamma), min=1e-4, max=1e4)
            dec_disp = self.disp_decoder(x)
            dec_disp = torch.clamp(dec_disp, min=1e-6, max=1e6)
            dec_dropout = self.dropout_decoder(x)
            return dec_mean_gamma, dec_dropout, dec_disp, dec_latent
        if self.recon_loss == "nb":
            # Parameters for ZINB and NB
            dec_mean_gamma = self.mean_decoder(x)
            dec_mean_gamma = torch.clamp(torch.exp(dec_mean_gamma), min=1e-4, max=1e4)
            dec_disp = self.disp_decoder(x)
            dec_disp = torch.clamp(dec_disp, min=1e-6, max=1e6)
            return dec_mean_gamma, dec_disp, dec_latent
