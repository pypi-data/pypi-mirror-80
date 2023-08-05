import numpy as np


class EarlyStopping(object):
    def __init__(self,
                 mode: str = 'min',
                 early_stopping_metric: str = 'val_loss',
                 save_best_state_metric: str = 'val_loss',
                 benchmark: bool = False,
                 threshold: int = 3,
                 patience: int = 50):
        self.benchmark = benchmark
        self.patience = patience
        self.threshold = threshold
        self.epoch = 0
        self.wait = 0
        self.mode = mode
        self.save_best_state_metric = save_best_state_metric
        self.early_stopping_metric = early_stopping_metric
        self.current_performance = np.inf
        self.best_performance = np.inf
        self.best_performance_state = np.inf
        if self.mode == "max":
            self.best_performance *= -1
            self.current_performance *= -1

        if patience == 0:
            self.is_better = lambda a, b: True
            self.step = lambda a: False

    def step(self, scalar):
        self.epoch += 1
        if self.benchmark or self.epoch < self.patience:
            continue_training = True
        elif self.wait >= self.patience:
            continue_training = False
        else:
            # Shift
            self.current_performance = scalar
            improvement = 0

            # Compute improvement
            if self.mode == "max":
                improvement = self.current_performance - self.best_performance
            elif self.mode == "min":
                improvement = self.best_performance - self.current_performance

            # updating best performance
            if improvement > 0:
                self.best_performance = self.current_performance
            if improvement < self.threshold:
                self.wait += 1
            else:
                self.wait = 0
            continue_training = True

        if not continue_training:
            print("\nStopping early: no improvement of more than " + str(self.threshold) +
                  " nats in " + str(self.patience) + " epochs")
            print("If the early stopping criterion is too strong, "
                  "please instantiate it with different parameters in the train method.")
        return continue_training

    def update_state(self, scalar):
        improved = ((self.mode == "max" and scalar - self.best_performance_state > 0) or
                    (self.mode == "min" and self.best_performance_state - scalar > 0))
        if improved:
            self.best_performance_state = scalar
        return improved
