import numpy as np
from eloquentarduino.ml.data.preprocessing.BaseStep import BaseStep


class FFTStep(BaseStep):
    """Apply FFT"""
    def __init__(self, X, y):
        BaseStep.__init__(self, X, y)
        assert (self.input_dim & (self.input_dim - 1) == 0), 'Number of features MUST be a power of 2 (%d given)' % self.input_dim

    @property
    def name(self):
        return 'fft'

    def __str__(self):
        return self.describe()

    def transform(self):
        # arduinoFFT produces one element less than Numpy (¯\_(ツ)_/¯)
        return self.apply(np.abs(np.fft.rfft(self.X))[:, :-1])

    def port(self):
        return self.jinja('FFT.jinja')