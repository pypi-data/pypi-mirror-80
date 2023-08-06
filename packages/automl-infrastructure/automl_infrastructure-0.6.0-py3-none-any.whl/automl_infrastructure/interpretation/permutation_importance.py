from automl_infrastructure.experiment.metrics.utils import parse_objective
from automl_infrastructure.classifiers import ClassifierPrediction
import pandas as pd
import numpy as np


class PermutationImportance(object):
    def __init__(self, estimator, n_iter=3, scoring='accuracy', random_state=None):
        # initialize scoring function
        self._scoring = parse_objective(scoring)

        self._n_iter = n_iter
        self._rng = np.random.RandomState(seed=random_state)
        self._estimator = estimator

        self._scores_decreases = None

    def fit(self, X, y):
        # calculate base scoring
        base_score = self._calculate_score(X, y)

        self._scores_decreases = {}
        for feature in X:
            self._scores_decreases[feature] = self._get_scores_shuffled(X, y, feature)
            self._scores_decreases[feature] = [base_score - score for score in self._scores_decreases[feature]]

    def show_weights(self):
        if self._scores_decreases is None:
            raise Exception('Can not show weights for unfitted PermutationImportance.')
        # create DataFrame and show it
        rows = []
        for feature in self._scores_decreases:
            rows.append([feature, np.mean(self._scores_decreases[feature]), np.std(self._scores_decreases[feature])])
        df = pd.DataFrame(rows, columns=['Feature', 'Weight', 'Std']).sort_values(by='Weight', ascending=False)\
                .reset_index(drop=True)
        print(df)

    def _calculate_score(self, X, y):
        pred_y = self._estimator.predict(X)
        proba_y = self._estimator.predict(X)
        estimator_prediction = ClassifierPrediction(pred_y, proba_y)
        scoring = self._scoring(y, estimator_prediction)
        return scoring

    def _get_scores_shuffled(self, X, y, feature):
        shuffles_generator = self._iter_shuffled(X, feature)
        return np.array([self._calculate_score(X_shuffled, y) for X_shuffled in shuffles_generator])

    def _iter_shuffled(self, X, feature):
        X_res = X.copy()
        for i in range(self._n_iter):
            X_res[feature] = self._rng.permutation(X[feature].values)
            yield X_res
            X_res[feature] = X[feature]
