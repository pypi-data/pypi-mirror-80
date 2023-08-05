import scanpy as sc
import scarchest as sca
import numpy as np

X = np.random.normal(0.0, 1.0, size=(1000, 500))
tasks = list('ABCD') * 250
labels = list('abcde') * 200

task_key = 'task'
label_key = 'label'
is_label_key = 'check'

np.random.shuffle(tasks)
np.random.shuffle(labels)

adata = sc.AnnData(X=X, obs={task_key: tasks, label_key: labels})

mars = sca.models.MARS(x_dim=adata.shape[1],
                       architecture=[128],
                       z_dim=10,
                       conditions=list('ABCD'),
                       activation='elu',
                       output_activation='linear',
                       use_batchnorm=True,
                       dropout_rate=0.2)

print(mars)

pre_trainer = sca.trainers.MARSPreTrainer(model=mars,
                                          adata=adata,
                                          task_key=task_key,
                                          )

pre_trainer.train(1)

X = np.random.normal(0.0, 1.0, size=(1000, 500))
tasks = list('EFGHI') * 200
labels = list('hijk') * 250

np.random.shuffle(tasks)
np.random.shuffle(labels)

adata = sc.AnnData(X=X, obs={task_key: tasks, label_key: labels})

new_mars, new_trainer = sca.mars_operate(mars,
                                         new_adata=adata,
                                         new_tasks=list('EFGHI'),
                                         meta_tasks=['I'],
                                         task_key=task_key,
                                         cell_type_key=label_key,
                                         n_clusters=4,
                                         tau=0.2,
                                         eta=1.0,
                                         freeze=True,
                                         remove_dropout=False)

print(new_mars)

new_trainer.train(n_epochs=1)
