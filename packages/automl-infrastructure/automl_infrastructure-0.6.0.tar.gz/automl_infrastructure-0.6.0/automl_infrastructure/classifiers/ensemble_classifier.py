from automl_infrastructure.classifiers import Classifier
import numpy as np
import pandas as pd
from automl_infrastructure.utils import random_str


class EnsembleClassifier(Classifier):

    """
    The EnsembleClassifier class represents a complex classifier that consists of one or more sub-classifiers.
    The way the complex classifier works is:
        - applying every sub-classifier on the dataset
        - gather from every sub-classifiers the classes probabilities prediction, and apply ensemble model
          on them with extra features (optional)
    """
    def __init__(self, name, input_models, ensemble_model, ensemble_extra_features=None):
        """
        :param name: the name of the classifier.
        :type name: str

        :param input_models: list of sub-classifiers to aggregate their predictions.
        :type input_models: list of :class:`automl_infrastructure.classifiers.base.Classifier`

        :param ensemble_model: the aggregator classifier on top the sub-classifiers and possibly extra features.
        :type ensemble_model: :class:`automl_infrastructure.classifiers.base.Classifier`

        :param ensemble_extra_features: list of extra features that the ensemble model should work on.
        :type ensemble_extra_features: list of str ,optional
        """
        super().__init__(name)
        self._input_models = input_models
        self._ensemble_model = ensemble_model
        self._ensemble_features = ensemble_extra_features

        # used to create dataframe over ensemble features
        self._temporary_ensemble_features = None

    def _prepare_features(self, x, recreate_features_names=False):
        """
        Prepare features for the ensemble model, using the sub-classifier classes probabilities prediction along side
        extra features.

        :param x: the original dataset.
        :type x: pandas.DataFrame

        :param recreate_features_names: weather to regenerate new features cols names
        :type recreate_features_names: bool ,optional
        """
        # make probability prediction for every sub-classifier
        new_features = []
        for input_model in self._input_models:
            new_features.append(input_model.predict_proba(x))
        if self._ensemble_features is not None:
            new_features.append(x[self._ensemble_features])

        features_array = np.concatenate(new_features, axis=1)
        # create random features names if none supplied
        if recreate_features_names:
            new_features_names = ['FEATURE_{}_{}'.format(i, random_str(length=8))
                                  for i in range(features_array.shape[1])]
            self._temporary_ensemble_features = new_features_names
        else:
            if self._temporary_ensemble_features is None:
                raise Exception('You must initialize new features names.')
            new_features_names = self._temporary_ensemble_features

        # transform to pandas DataFrame form
        new_features_df = pd.DataFrame(features_array, columns=new_features_names)
        return new_features_df

    def fit(self, x, y, **kwargs):
        # train input models
        for input_model in self._input_models:
            input_model.fit(x, y, **kwargs)

        # train ensemble model based on input models predictions
        final_x = self._prepare_features(x, recreate_features_names=True)
        self._ensemble_model.fit(final_x, y, **kwargs)

    def predict(self, x):
        final_x = self._prepare_features(x)
        return self._ensemble_model.predict(final_x)

    def predict_proba(self, x):
        final_x = self._prepare_features(x)
        return self._ensemble_model.predict_proba(final_x)

    def set_params(self, params):
        for input_model in self._input_models:
            if input_model.name in params:
                input_model.set_params(params[input_model.name])
        if self._ensemble_model.name in params:
            self._ensemble_model.set_params(params[self._ensemble_model.name])

    def get_params(self, deep=True):
        params = {self._ensemble_model.name: self._ensemble_model.get_params()}
        if deep:
            for input_model in self._input_models:
                params[input_model.name] = input_model.get_params()
        return params
