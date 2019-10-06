# This file holds all the custom classes for sklearn's Pipeline function
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class LogTransformation(BaseEstimator, TransformerMixin):

    def __init__(self, data_to_transform):
        self.data_to_transform = data_to_transform

    def fit(self, X, y=None):
        return self

    @staticmethod
    def transform(y):
        return np.log(y)
