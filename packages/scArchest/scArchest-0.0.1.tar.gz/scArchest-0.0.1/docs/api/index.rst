API
===

The API reference contains detailed descriptions of the different end-user classes, functions, methods, etc.


.. note::

    This API reference only contains end-user documentation.
    If you are looking to hack away at scArches' internals, you will find more detailed comments in the source code.

Import scArchest as::

    import scarchest as sca

After reading the data (``sca.data.read``), you can normalize your data with our ``sca.data.normalize_hvg`` function.
Then, you can instantiate one of the implemented models from ``sca.models`` module (currently we support ``trVAE``,
``scVI``, ``scANVI``, ``TotalVI``, and ``MARS``) and train it on your dataset.

.. toctree::
    :glob:
    :maxdepth: 2

    *