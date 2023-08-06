from eloquentarduino.ml.data.preprocessing.BaseStep import BaseStep


class NormalizeStep(BaseStep):
    """Apply min/max normalization"""
    def __init__(self, X, y, featurewise=False):
        BaseStep.__init__(self, X, y)
        self.featurewise = featurewise
        self.min = None
        self.max = None

    @property
    def name(self):
        return 'normalize'

    def __str__(self):
        return self.describe(('featurewise', self.featurewise))

    def transform(self):
        axis = 0 if self.featurewise else None
        self.min = self.X.min(axis)
        self.max = self.X.max(axis)
        return self.apply((self.X - self.min) / (self.max - self.min))

    def port(self):
        return self.jinja('Normalize.jinja', {
            'xmin': self.min,
            'inverse_range': 1 / (self.max - self.min),
            'featurewise': self.featurewise
        })