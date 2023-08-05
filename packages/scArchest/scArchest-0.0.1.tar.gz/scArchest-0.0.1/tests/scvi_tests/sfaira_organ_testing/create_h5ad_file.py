import os
import sys

env = os.path.expanduser('~/Documents/sfaira_arch/sfaira')
sys.path.insert(0, env)

import sfaira.api as sfaira

datadir = os.path.expanduser('~/Documents/sfaira_arch/sfaira_data')
# Here we choose mouse pancreas:
# The DatasetGroupPancreas contains instances of Dataset which correspond to individual data sets.
ds = sfaira.data.mouse.DatasetGroupPancreas(path=datadir)  # This links all data sets available
print(ds.ids)
ds.datasets['mouse_pancreas_2019_10x_pisco_001_10.1101/661728'].load()
adata = ds.datasets['mouse_pancreas_2019_10x_thompson_004_10.1016/j.cmet.2019.01.021'].adata
print(adata)
ds.datasets['mouse_pancreas_2019_smartseq2_pisco_001_10.1101/661728'].load()
adata = ds.datasets['mouse_pancreas_2019_smartseq2_pisco_001_10.1101/661728'].adata
print(adata.obs['cell_ontology_class'].unique())
print(adata)
ds.datasets['mouse_pancreas_2018_microwell-seq_han_001_10.1016/j.cell.2018.02.001'].load()
adata = ds.datasets['mouse_pancreas_2018_microwell-seq_han_001_10.1016/j.cell.2018.02.001'].adata
print(adata)
ds.datasets['mouse_pancreas_2019_10x_thompson_001_10.1016/j.cmet.2019.01.021'].load()
adata = ds.datasets['mouse_pancreas_2019_10x_thompson_001_10.1016/j.cmet.2019.01.021'].adata
print(adata)
adata = ds.adata
print(adata)
