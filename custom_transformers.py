# file containing custom built transformers to help preprocess data before training
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class NaturalLogValues(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    @staticmethod
    def fit(X):
        return X

    @staticmethod
    def transform(X):
        return np.log(X)