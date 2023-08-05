import numpy as np
import torch
from torch.utils.data import Dataset
from scipy import sparse

from .data_handling import remove_sparsity
from ._utils import label_encoder


class AnnotatedDataset(Dataset):
    def __init__(self,
                 adata,
                 condition_key=None,
                 condition_encoder=None,
                 cell_type_key=None,
                 cell_type_encoder=None,
                 size_factors_key=None,
                 unique_conditions=None,
                 ):
        self.adata = adata
        if sparse.issparse(self.adata.X):
            self.adata = remove_sparsity(self.adata)
        self.data = np.asarray(self.adata.X)

        self.condition_encoder = condition_encoder
        self.condition_key = condition_key
        self.unique_conditions = unique_conditions

        self.cell_type_encoder = cell_type_encoder
        self.cell_type_key = cell_type_key
        self.unique_cell_types = None

        self.size_factors_key = size_factors_key

        if self.condition_key is not None:
            if self.unique_conditions is None:
                self.unique_conditions = adata.obs[condition_key].unique().tolist()
            self.conditions, self.condition_encoder = label_encoder(self.adata,
                                                                    encoder=self.condition_encoder,
                                                                    condition_key=condition_key)
            self.conditions = np.array(self.conditions).reshape(-1, )

        if self.cell_type_key is not None:
            self.unique_cell_types = adata.obs[cell_type_key].unique().tolist()
            self.cell_types, self.cell_type_encoder = label_encoder(self.adata,
                                                                    encoder=self.cell_type_encoder,
                                                                    condition_key=cell_type_key)
            self.cell_types = np.array(self.cell_types).reshape(-1, )

        if self.size_factors_key:
            self.raw_data = np.array(self.adata.raw.X)
            self.size_factors = np.array(self.adata.obs[self.size_factors_key].values).reshape(-1, )

    def __getitem__(self, index):
        outputs = dict()
        outputs["x"] = torch.tensor(self.data[index, :])

        if self.condition_key:
            outputs["c"] = torch.tensor(self.conditions[index])

        if self.cell_type_key:
            outputs["y"] = torch.tensor(self.cell_types[index])

        if self.size_factors_key:
            outputs["raw"] = torch.tensor(self.raw_data[index, :])
            outputs["f"] = torch.tensor(self.size_factors[index])
        return outputs

    def __len__(self):
        return len(self.adata)

    @property
    def condition_label_encoder(self) -> dict:
        return self.condition_encoder

    @condition_label_encoder.setter
    def condition_label_encoder(self, value: dict):
        if value is not None:
            self.condition_encoder = value

    @property
    def cell_type_label_encoder(self) -> dict:
        return self.cell_type_encoder

    @cell_type_label_encoder.setter
    def cell_type_label_encoder(self, value: dict):
        if value is not None:
            self.cell_type_encoder = value

    @property
    def stratifier_weights(self):
        condition_coeff = 1 / len(self.conditions)
        weights_per_condition = list()
        for i in range(len(self.conditions)):
            samples_per_condition = np.count_nonzero(self.conditions == i)
            if samples_per_condition == 0:
                weights_per_condition.append(0)
            else:
                weights_per_condition.append((1 / samples_per_condition) * condition_coeff)
        strat_weights = np.copy(self.conditions)
        for i in range(len(self.conditions)):
            strat_weights = np.where(strat_weights == i, weights_per_condition[i], strat_weights)

        return strat_weights.astype(float)
