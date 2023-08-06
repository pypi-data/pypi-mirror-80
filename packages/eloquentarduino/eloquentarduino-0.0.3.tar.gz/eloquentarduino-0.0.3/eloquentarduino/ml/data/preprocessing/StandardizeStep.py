from eloquentarduino.ml.data.preprocessing.BaseStep import BaseStep


class StandardizeStep(BaseStep):
    """Apply standardization"""
    def __init__(self, X, y, featurewise=False):
        BaseStep.__init__(self, X, y)
        self.featurewise = featurewise
        self.mean = None
        self.std = None

    @property
    def name(self):
        return 'standardize'

    def __str__(self):
        return self.describe(('featurewise', self.featurewise))

    def transform(self):
        axis = 0 if self.featurewise else None
        self.mean = self.X.mean(axis)
        self.std = self.X.std(axis)
        return self.apply((self.X - self.mean) / self.std)

    def port(self):
        return self.jinja('Standardize.jinja', {
            'xmean': self.mean,
            'inverse_std': 1 / self.std,
            'featurewise': self.featurewise
        })
