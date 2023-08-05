import torch
from typing import Iterable
from torch import nn as nn
from torch.distributions import Normal
from scvi.core.modules.utils import one_hot


def reparameterize_gaussian(mu, var):
    return Normal(mu, var.sqrt()).rsample()


def identity(x):
    return x


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


class FCLayers(nn.Module):
    """A helper class to build fully-connected layers for a neural network.

    Parameters
    ----------
    n_in
        The dimensionality of the input
    n_out
        The dimensionality of the output
    n_cat_list
        A list containing, for each category of interest,
        the number of categories. Each category will be
        included using a one-hot encoding.
    n_layers
        The number of fully-connected hidden layers
    n_hidden
        The number of nodes per hidden layer
    dropout_rate
        Dropout rate to apply to each of the hidden layers
    use_batch_norm
        Whether to have `BatchNorm` layers or not
    use_relu
        Whether to have `ReLU` layers or not
    bias
        Whether to learn bias in linear layers or not
    """

    def __init__(
        self,
        n_in: int,
        n_out: int,
        n_cat_list: Iterable[int] = None,
        n_layers: int = 1,
        n_hidden: int = 128,
        dropout_rate: float = 0.1,
        use_batch_norm: bool = True,
        use_relu: bool = True,
        bias: bool = True,
        modified: bool = False,
    ):
        super().__init__()
        layers_dim = [n_in] + (n_layers - 1) * [n_hidden] + [n_out]
        self.modified = modified

        if n_cat_list is not None:
            # n_cat = 1 will be ignored
            self.n_cat_list = [n_cat if n_cat > 1 else 0 for n_cat in n_cat_list]
        else:
            self.n_cat_list = []

        self.fc_layers = nn.Sequential()
        for i, (n_in, n_out) in enumerate(zip(layers_dim[:-1], layers_dim[1:])):
            n_cond = 0
            if self.modified:
                if i == 0:
                    n_cond = sum(self.n_cat_list)
            else:
                n_cond = sum(self.n_cat_list)

            layer = nn.Sequential()
            layer.add_module(name="L", module=CondLayers(n_in, n_out, n_cond, bias))
            if use_batch_norm:
                layer.add_module(name="B", module=nn.BatchNorm1d(n_out, momentum=0.01, eps=0.001))
            if use_relu:
                layer.add_module(name="A", module=nn.ReLU())
            if dropout_rate > 0:
                layer.add_module(name="D", module=nn.Dropout(p=dropout_rate))
            self.fc_layers.add_module(name="Layer{:d}".format(i), module=layer)

    def forward(self, x: torch.Tensor, *cat_list: int, instance_id: int = 0):
        """Forward computation on ``x``.

        Parameters
        ----------
        x
            tensor of values with shape ``(n_in,)``
        cat_list
            list of category membership(s) for this sample
        instance_id
            Use a specific conditional instance normalization (batchnorm)
        x: torch.Tensor

        Returns
        -------
        py:class:`torch.Tensor`
            tensor of shape ``(n_out,)``
        """
        one_hot_cat_list = []  # for generality in this list many indices useless.
        assert len(self.n_cat_list) <= len(
            cat_list
        ), "nb. categorical args provided doesn't match init. params."
        for n_cat, cat in zip(self.n_cat_list, cat_list):
            assert not (
                n_cat and cat is None
            ), "cat not provided while n_cat != 0 in init. params."
            if n_cat > 1:  # n_cat = 1 will be ignored - no additional information
                if cat.size(1) != n_cat:
                    one_hot_cat = one_hot(cat, n_cat)
                else:
                    one_hot_cat = cat  # cat has already been one_hot encoded
                one_hot_cat_list += [one_hot_cat]

        for name, layers in self.fc_layers.named_children():
            for layer in layers:
                if layer is not None:
                    if isinstance(layer, nn.BatchNorm1d):
                        if x.dim() == 3:
                            x = torch.cat(
                                [(layer(slice_x)).unsqueeze(0) for slice_x in x], dim=0
                            )
                        else:
                            x = layer(x)
                    else:
                        if isinstance(layer, CondLayers):
                            if self.modified:
                                if "Layer0" in name:
                                    if x.dim() == 3:
                                        one_hot_cat_list_layer = [
                                            o.unsqueeze(0).expand(
                                                (x.size(0), o.size(0), o.size(1))
                                            )
                                            for o in one_hot_cat_list
                                        ]
                                    else:
                                        one_hot_cat_list_layer = one_hot_cat_list
                                    x = torch.cat((x, *one_hot_cat_list_layer), dim=-1)
                            else:
                                if x.dim() == 3:
                                    one_hot_cat_list_layer = [
                                        o.unsqueeze(0).expand(
                                            (x.size(0), o.size(0), o.size(1))
                                        )
                                        for o in one_hot_cat_list
                                    ]
                                else:
                                    one_hot_cat_list_layer = one_hot_cat_list
                                x = torch.cat((x, *one_hot_cat_list_layer), dim=-1)
                        x = layer(x)
        return x


class Encoder(nn.Module):
    """Encodes data of ``n_input`` dimensions into a latent space of ``n_output``
    dimensions using a fully-connected neural network of ``n_hidden`` layers.

    Parameters
    ----------
    n_input
        The dimensionality of the input (data space)
    n_output
        The dimensionality of the output (latent space)
    n_cat_list
        A list containing the number of categories
        for each category of interest. Each category will be
        included using a one-hot encoding
    n_layers
        The number of fully-connected hidden layers
    n_hidden
        The number of nodes per hidden layer
        :dropout_rate: Dropout rate to apply to each of the hidden layers
    distribution
        Distribution of z

    Returns
    -------
    """

    def __init__(
        self,
        n_input: int,
        n_output: int,
        n_cat_list: Iterable[int] = None,
        n_layers: int = 1,
        n_hidden: int = 128,
        dropout_rate: float = 0.1,
        distribution: str = "normal",
        modified: bool = False,
    ):
        super().__init__()
        self.distribution = distribution
        self.encoder = FCLayers(
            n_in=n_input,
            n_out=n_hidden,
            n_cat_list=n_cat_list,
            n_layers=n_layers,
            n_hidden=n_hidden,
            dropout_rate=dropout_rate,
            modified=modified,
        )
        self.mean_encoder = nn.Linear(n_hidden, n_output)
        self.var_encoder = nn.Linear(n_hidden, n_output)

        if distribution == "ln":
            self.z_transformation = nn.Softmax(dim=-1)
        else:
            self.z_transformation = identity

    def forward(self, x: torch.Tensor, *cat_list: int):
        """The forward computation for a single sample.

         #. Encodes the data into latent space using the encoder network
         #. Generates a mean \\( q_m \\) and variance \\( q_v \\)
         #. Samples a new value from an i.i.d. multivariate normal \\( \\sim Ne(q_m, \\mathbf{I}q_v) \\)

        Parameters
        ----------
        x
            tensor with shape (n_input,)
        cat_list
            list of category membership(s) for this sample

        Returns
        -------
        3-tuple of :py:class:`torch.Tensor`
            tensors of shape ``(n_latent,)`` for mean and var, and sample
        """

        # Parameters for latent distribution
        q = self.encoder(x, *cat_list)
        q_m = self.mean_encoder(q)
        q_v = torch.exp(self.var_encoder(q)) + 1e-4
        latent = self.z_transformation(reparameterize_gaussian(q_m, q_v))
        return q_m, q_v, latent


class DecoderSCVI(nn.Module):
    """Decodes data from latent space of ``n_input`` dimensions ``n_output``
    dimensions using a fully-connected neural network of ``n_hidden`` layers.

    Parameters
    ----------
    n_input
        The dimensionality of the input (latent space)
    n_output
        The dimensionality of the output (data space)
    n_cat_list
        A list containing the number of categories
        for each category of interest. Each category will be
        included using a one-hot encoding
    n_layers
        The number of fully-connected hidden layers
    n_hidden
        The number of nodes per hidden layer
    dropout_rate
        Dropout rate to apply to each of the hidden layers

    Returns
    -------
    """

    def __init__(
        self,
        n_input: int,
        n_output: int,
        n_cat_list: Iterable[int] = None,
        n_layers: int = 1,
        n_hidden: int = 128,
        modified: bool = False,
    ):
        super().__init__()
        self.px_decoder = FCLayers(
            n_in=n_input,
            n_out=n_hidden,
            n_cat_list=n_cat_list,
            n_layers=n_layers,
            n_hidden=n_hidden,
            dropout_rate=0,
            modified=modified,
        )

        # mean gamma
        self.px_scale_decoder = nn.Sequential(
            nn.Linear(n_hidden, n_output), nn.Softmax(dim=-1)
        )

        # dispersion: here we only deal with gene-cell dispersion case
        self.px_r_decoder = nn.Linear(n_hidden, n_output)

        # dropout
        self.px_dropout_decoder = nn.Linear(n_hidden, n_output)

    def forward(
        self, dispersion: str, z: torch.Tensor, library: torch.Tensor, *cat_list: int
    ):
        """The forward computation for a single sample.

         #. Decodes the data from the latent space using the decoder network
         #. Returns parameters for the ZINB distribution of expression
         #. If ``dispersion != 'gene-cell'`` then value for that param will be ``None``

        Parameters
        ----------
        dispersion
            One of the following

            * ``'gene'`` - dispersion parameter of NB is constant per gene across cells
            * ``'gene-batch'`` - dispersion can differ between different batches
            * ``'gene-label'`` - dispersion can differ between different labels
            * ``'gene-cell'`` - dispersion can differ for every gene in every cell
        z :
            tensor with shape ``(n_input,)``
        library
            library size
        cat_list
            list of category membership(s) for this sample

        Returns
        -------
        4-tuple of :py:class:`torch.Tensor`
            parameters for the ZINB distribution of expression
        """
        # The decoder returns values for the parameters of the ZINB distribution

        px = self.px_decoder(z, *cat_list)
        px_scale = self.px_scale_decoder(px)
        px_dropout = self.px_dropout_decoder(px)
        # Clamp to high value: exp(12) ~ 160000 to avoid nans (computational stability)
        px_rate = torch.exp(library) * px_scale  # torch.clamp( , max=12)
        px_r = self.px_r_decoder(px) if dispersion == "gene-cell" else None
        return px_scale, px_r, px_rate, px_dropout


class Decoder(nn.Module):
    """Decodes data from latent space to data space

    ``n_input`` dimensions to ``n_output``
    dimensions using a fully-connected neural network of ``n_hidden`` layers.
    Output is the mean and variance of a multivariate Gaussian

    Parameters
    ----------
    n_input
        The dimensionality of the input (latent space)
    n_output
        The dimensionality of the output (data space)
    n_cat_list
        A list containing the number of categories
        for each category of interest. Each category will be
        included using a one-hot encoding
    n_layers
        The number of fully-connected hidden layers
    n_hidden
        The number of nodes per hidden layer
    dropout_rate
        Dropout rate to apply to each of the hidden layers

    Returns
    -------
    """

    def __init__(
        self,
        n_input: int,
        n_output: int,
        n_cat_list: Iterable[int] = None,
        n_layers: int = 1,
        n_hidden: int = 128,
    ):
        super().__init__()
        self.decoder = FCLayers(
            n_in=n_input,
            n_out=n_hidden,
            n_cat_list=n_cat_list,
            n_layers=n_layers,
            n_hidden=n_hidden,
            dropout_rate=0,
        )

        self.mean_decoder = nn.Linear(n_hidden, n_output)
        self.var_decoder = nn.Linear(n_hidden, n_output)

    def forward(self, x: torch.Tensor, *cat_list: int):
        """The forward computation for a single sample.

         #. Decodes the data from the latent space using the decoder network
         #. Returns tensors for the mean and variance of a multivariate distribution

        Parameters
        ----------
        x
            tensor with shape ``(n_input,)``
        cat_list
            list of category membership(s) for this sample

        Returns
        -------
        2-tuple of :py:class:`torch.Tensor`
            Mean and variance tensors of shape ``(n_output,)``

        """
        # Parameters for latent distribution
        p = self.decoder(x, *cat_list)
        p_m = self.mean_decoder(p)
        p_v = torch.exp(self.var_decoder(p))
        return p_m, p_v


class DecoderTOTALVI(nn.Module):
    """
    Decodes data from latent space of ``n_input`` dimensions ``n_output`` dimensions.

    Uses a linear decoder.

    Parameters
    ----------
    n_input
        The dimensionality of the input (latent space)
    n_output_genes
        The dimensionality of the output (gene space)
    n_output_proteins
        The dimensionality of the output (protein space)
    n_cat_list
        A list containing the number of categories
        for each category of interest. Each category will be
        included using a one-hot encoding

    """

    def __init__(
        self,
        n_input: int,
        n_output_genes: int,
        n_output_proteins: int,
        n_cat_list: Iterable[int] = None,
        n_layers: int = 1,
        n_hidden: int = 256,
        dropout_rate: float = 0,
        modified: bool = False
    ):
        super().__init__()
        self.n_output_genes = n_output_genes
        self.n_output_proteins = n_output_proteins

        self.px_decoder = FCLayers(
            n_in=n_input,
            n_out=n_hidden,
            n_cat_list=n_cat_list,
            n_layers=n_layers,
            n_hidden=n_hidden,
            dropout_rate=dropout_rate,
            modified=modified
        )

        # mean gamma
        self.px_scale_decoder = FCLayers(
            n_in=n_hidden + n_input,
            n_out=n_output_genes,
            n_cat_list=n_cat_list,
            n_layers=1,
            use_relu=False,
            use_batch_norm=False,
            dropout_rate=0,
            modified=modified
        )

        # background mean first decoder
        self.py_back_decoder = FCLayers(
            n_in=n_input,
            n_out=n_hidden,
            n_cat_list=n_cat_list,
            n_layers=n_layers,
            n_hidden=n_hidden,
            dropout_rate=dropout_rate,
            modified=modified
        )
        # background mean parameters second decoder
        self.py_back_mean_log_alpha = FCLayers(
            n_in=n_hidden + n_input,
            n_out=n_output_proteins,
            n_cat_list=n_cat_list,
            n_layers=1,
            use_relu=False,
            use_batch_norm=False,
            dropout_rate=0,
            modified=modified
        )
        self.py_back_mean_log_beta = FCLayers(
            n_in=n_hidden + n_input,
            n_out=n_output_proteins,
            n_cat_list=n_cat_list,
            n_layers=1,
            use_relu=False,
            use_batch_norm=False,
            dropout_rate=0,
            modified=modified
        )

        # foreground increment decoder step 1
        self.py_fore_decoder = FCLayers(
            n_in=n_input,
            n_out=n_hidden,
            n_cat_list=n_cat_list,
            n_layers=n_layers,
            n_hidden=n_hidden,
            dropout_rate=dropout_rate,
            modified=modified
        )
        # foreground increment decoder step 2
        self.py_fore_scale_decoder = FCLayers(
            n_in=n_hidden + n_input,
            n_out=n_output_proteins,
            n_cat_list=n_cat_list,
            n_layers=1,
            use_relu=True,
            use_batch_norm=False,
            dropout_rate=0,
            modified=modified
        )

        # dropout (mixture component for proteins, ZI probability for genes)
        self.sigmoid_decoder = FCLayers(
            n_in=n_input,
            n_out=n_hidden,
            n_cat_list=n_cat_list,
            n_layers=n_layers,
            n_hidden=n_hidden,
            dropout_rate=dropout_rate,
            modified=modified
        )
        self.px_dropout_decoder_gene = FCLayers(
            n_in=n_hidden + n_input,
            n_out=n_output_genes,
            n_cat_list=n_cat_list,
            n_layers=1,
            use_relu=False,
            use_batch_norm=False,
            dropout_rate=0,
            modified=modified
        )

        self.py_background_decoder = FCLayers(
            n_in=n_hidden + n_input,
            n_out=n_output_proteins,
            n_cat_list=n_cat_list,
            n_layers=1,
            use_relu=False,
            use_batch_norm=False,
            dropout_rate=0,
            modified=modified
        )

    def forward(self, z: torch.Tensor, library_gene: torch.Tensor, *cat_list: int):
        """
        The forward computation for a single sample.

         #. Decodes the data from the latent space using the decoder network
         #. Returns local parameters for the ZINB distribution for genes
         #. Returns local parameters for the Mixture NB distribution for proteins

         We use the dictionary `px_` to contain the parameters of the ZINB/NB for genes.
         The rate refers to the mean of the NB, dropout refers to Bernoulli mixing parameters.
         `scale` refers to the quanity upon which differential expression is performed. For genes,
         this can be viewed as the mean of the underlying gamma distribution.

         We use the dictionary `py_` to contain the parameters of the Mixture NB distribution for proteins.
         `rate_fore` refers to foreground mean, while `rate_back` refers to background mean. `scale` refers to
         foreground mean adjusted for background probability and scaled to reside in simplex.
         `back_alpha` and `back_beta` are the posterior parameters for `rate_back`.  `fore_scale` is the scaling
         factor that enforces `rate_fore` > `rate_back`.

        Parameters
        ----------
        z
            tensor with shape ``(n_input,)``
        library_gene
            library size
        cat_list
            list of category membership(s) for this sample

        Returns
        -------
        3-tuple (first 2-tuple :py:class:`dict`, last :py:class:`torch.Tensor`)
            parameters for the ZINB distribution of expression

        """
        px_ = {}
        py_ = {}

        px = self.px_decoder(z, *cat_list)
        px_cat_z = torch.cat([px, z], dim=-1)
        px_["scale"] = nn.Softmax(dim=-1)(self.px_scale_decoder(px_cat_z, *cat_list))
        px_["rate"] = library_gene * px_["scale"]

        py_back = self.py_back_decoder(z, *cat_list)
        py_back_cat_z = torch.cat([py_back, z], dim=-1)

        py_["back_alpha"] = self.py_back_mean_log_alpha(py_back_cat_z, *cat_list)
        py_["back_beta"] = torch.exp(
            self.py_back_mean_log_beta(py_back_cat_z, *cat_list)
        )
        log_pro_back_mean = Normal(py_["back_alpha"], py_["back_beta"]).rsample()
        py_["rate_back"] = torch.exp(log_pro_back_mean)

        py_fore = self.py_fore_decoder(z, *cat_list)
        py_fore_cat_z = torch.cat([py_fore, z], dim=-1)
        py_["fore_scale"] = (
            self.py_fore_scale_decoder(py_fore_cat_z, *cat_list) + 1 + 1e-8
        )
        py_["rate_fore"] = py_["rate_back"] * py_["fore_scale"]

        p_mixing = self.sigmoid_decoder(z, *cat_list)
        p_mixing_cat_z = torch.cat([p_mixing, z], dim=-1)
        px_["dropout"] = self.px_dropout_decoder_gene(p_mixing_cat_z, *cat_list)
        py_["mixing"] = self.py_background_decoder(p_mixing_cat_z, *cat_list)

        protein_mixing = 1 / (1 + torch.exp(-py_["mixing"]))
        py_["scale"] = torch.nn.functional.normalize(
            (1 - protein_mixing) * py_["rate_fore"], p=1, dim=-1
        )

        return (px_, py_, log_pro_back_mean)


class EncoderTOTALVI(nn.Module):
    """
    Encodes data of ``n_input`` dimensions into a latent space of ``n_output`` dimensions.

    Uses a fully-connected neural network of ``n_hidden`` layers.

    Parameters
    ----------
    n_input
        The dimensionality of the input (data space)
    n_output
        The dimensionality of the output (latent space)
    n_cat_list
        A list containing the number of categories
        for each category of interest. Each category will be
        included using a one-hot encoding
    n_layers
        The number of fully-connected hidden layers
    n_hidden
        The number of nodes per hidden layer
    dropout_rate
        Dropout rate to apply to each of the hidden layers
    distribution
        Distribution of the latent space, one of

        * ``'normal'`` - Normal distribution
        * ``'ln'`` - Logistic normal

    """

    def __init__(
        self,
        n_input: int,
        n_output: int,
        n_cat_list: Iterable[int] = None,
        n_layers: int = 2,
        n_hidden: int = 256,
        dropout_rate: float = 0.1,
        distribution: str = "ln",
        modified: bool = False
    ):
        super().__init__()

        self.encoder = FCLayers(
            n_in=n_input,
            n_out=n_hidden,
            n_cat_list=n_cat_list,
            n_layers=n_layers,
            n_hidden=n_hidden,
            dropout_rate=dropout_rate,
            modified=modified
        )
        self.z_encoder = nn.Sequential(
            nn.Linear(n_hidden, n_hidden),
            nn.BatchNorm1d(n_hidden),
            nn.ReLU(),
            nn.Dropout(p=dropout_rate),
        )
        self.z_mean_encoder = nn.Linear(n_hidden, n_output)
        self.z_var_encoder = nn.Linear(n_hidden, n_output)

        self.l_gene_encoder = nn.Sequential(
            nn.Linear(n_hidden, n_hidden),
            nn.BatchNorm1d(n_hidden),
            nn.ReLU(),
            nn.Dropout(p=dropout_rate),
        )
        self.l_gene_mean_encoder = nn.Linear(n_hidden, 1)
        self.l_gene_var_encoder = nn.Linear(n_hidden, 1)

        self.distribution = distribution

        if distribution == "ln":
            self.z_transformation = nn.Softmax(dim=-1)
        else:
            self.z_transformation = identity

        self.l_transformation = torch.exp

    def reparameterize_transformation(self, mu, var):
        untran_z = Normal(mu, var.sqrt()).rsample()
        z = self.z_transformation(untran_z)
        return z, untran_z

    def forward(self, data: torch.Tensor, *cat_list: int):
        r"""
        The forward computation for a single sample.

         #. Encodes the data into latent space using the encoder network
         #. Generates a mean \\( q_m \\) and variance \\( q_v \\)
         #. Samples a new value from an i.i.d. latent distribution

        The dictionary ``latent`` contains the samples of the latent variables, while ``untran_latent``
        contains the untransformed versions of these latent variables. For example, the library size is log normally distributed,
        so ``untran_latent["l"]`` gives the normal sample that was later exponentiated to become ``latent["l"]``.
        The logistic normal distribution is equivalent to applying softmax to a normal sample.

        Parameters
        ----------
        data
            tensor with shape ``(n_input,)``
        cat_list
            list of category membership(s) for this sample

        Returns
        -------
        6-tuple. First 4 of :py:class:`torch.Tensor`, next 2 are `dict` of :py:class:`torch.Tensor`
            tensors of shape ``(n_latent,)`` for mean and var, and sample

        """
        # Parameters for latent distribution
        q = self.encoder(data, *cat_list)
        qz = self.z_encoder(q)
        qz_m = self.z_mean_encoder(qz)
        qz_v = torch.exp(self.z_var_encoder(qz)) + 1e-4
        z, untran_z = self.reparameterize_transformation(qz_m, qz_v)

        ql_gene = self.l_gene_encoder(q)
        ql_m = self.l_gene_mean_encoder(ql_gene)
        ql_v = torch.exp(self.l_gene_var_encoder(ql_gene)) + 1e-4
        log_library_gene = torch.clamp(reparameterize_gaussian(ql_m, ql_v), max=15)
        library_gene = self.l_transformation(log_library_gene)

        latent = {}
        untran_latent = {}
        latent["z"] = z
        latent["l"] = library_gene
        untran_latent["z"] = untran_z
        untran_latent["l"] = log_library_gene

        return qz_m, qz_v, ql_m, ql_v, latent, untran_latent

