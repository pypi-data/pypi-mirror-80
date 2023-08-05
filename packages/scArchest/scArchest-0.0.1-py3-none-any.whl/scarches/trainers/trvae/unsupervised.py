from .trainer import Trainer


class trVAETrainer(Trainer):
    def __init__(
            self,
            model,
            adata,
            alpha_iter_anneal: int = None,
            alpha_epoch_anneal: int = None,
            **kwargs
    ):
        super().__init__(model, adata, **kwargs)
        self.alpha_iter_anneal = alpha_iter_anneal
        self.alpha_epoch_anneal = alpha_epoch_anneal

    def loss(self, total_batch=None, labelled_batch=None):
        recon_loss, kl_loss, mmd_loss = self.model(**total_batch)
        kl_loss *= self.calc_alpha_coeff()
        loss = recon_loss + kl_loss + mmd_loss
        self.iter_logs["loss"].append(loss)
        self.iter_logs["recon_loss"].append(recon_loss)
        self.iter_logs["kl_loss"].append(kl_loss)
        self.iter_logs["mmd_loss"].append(mmd_loss)
        return loss

    def calc_alpha_coeff(self):
        """Calculates current alpha coefficient for alpha annealing.

           Parameters
           ----------

           Returns
           -------
           Current annealed alpha value
        """
        if self.alpha_epoch_anneal is not None:
            alpha_coeff = min(self.epoch / self.alpha_epoch_anneal, 1)
        elif self.alpha_iter_anneal is not None:
            alpha_coeff = min(((self.epoch * self.iters_per_epoch + self.iter) / self.alpha_iter_anneal), 1)
        else:
            alpha_coeff = 1
        return alpha_coeff

    def on_epoch_begin(self):
        pass

    def on_iteration_begin(self):
        pass

    def on_iteration_end(self):
        pass

    def on_training_end(self):
        pass
