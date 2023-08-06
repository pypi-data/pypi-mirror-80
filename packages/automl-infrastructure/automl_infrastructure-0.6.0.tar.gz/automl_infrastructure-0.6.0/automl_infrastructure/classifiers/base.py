from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from automl_infrastructure.utils import random_str


class Classifier(ABC):
    """
    The Classifier class defines an interface of a classifier.
    """

    def __init__(self, name, features_cols=None):
        """
        :param name: name of the classifier (e.g. 'lr1).
        :type name: str

        :param features_cols: features list that the classifier should work on, while ignoring other features.
        :type features_cols: list of str ,optional
        """
        self._name = name
        self._features_cols = features_cols

    @property
    def name(self):
        return self._name

    @abstractmethod
    def fit(self, x, y, **kwargs):
        """
        Training method on a given dataset with labels.

        :param x: the training dataset.
                Note that the training dataset may contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :param y: labels of the training dataset.
        :type y: pandas.Series or list

        :param kwargs:
        """
        pass

    @abstractmethod
    def predict(self, x):
        """
        The method receive a features dataset, and returns a class prediction for each row.

        :param x: the features dataset.

                Note that the training dataset may contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :return: list or numpy.array of classes predictions
        """
        pass

    @abstractmethod
    def predict_proba(self, x):
        """
        The method receive a features dataset, and returns classes probability prediction for each row.

        :param x: the features dataset.

                Note that the training dataset may contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :return: list or numpy.array of classes probability predictions (may be also list or numpy.array).

                Note that the classes probability list order must be natively sorted (e.g. for string, alphabetically).
        """
        pass

    @abstractmethod
    def set_params(self, params):
        """
        Sets hyper-params of the classifier.

        :param params: dictionary of parameters value by their name (e.g. {'C' : 1.0}).
        :type params: dict of {str: Any}

        """
        pass

    @abstractmethod
    def get_params(self, deep=True):
        """
        Getter for the classifier hyper-params.

        :param deep: for complex classifiers, weather to return params of inner classifiers.
        :type deep: bool ,optional

        :return: the classifier hyper-params.
        """
        pass


class ClassifierPrediction(object):
    """
    The class defines a coupling between classifier predictions and probabilities.
    The main reason for such object, is for the :class:`automl_infrastructure.experiment.metrics.base.Metric` contract.
    """
    def __init__(self, y_pred, y_proba):
        """
        :param y_pred: class prediction.
        :type y_pred: Any, typically str or int

        :param y_proba: classes probabilities.
        :type y_proba: list or numpy.array
        """
        self._y_pred = y_pred
        self._y_proba = y_proba

    @property
    def classes_pred(self):
        return self._y_pred

    @property
    def classes_proba(self):
        return self._y_proba


class BasicClassifier(Classifier, ABC):

    """
    The BasicClassifier abstract class implements native support for common and wide operations, such that:
    auto-unrolling vector features, narrowing dataframe to specific features ad ect'.
    """
    def __init__(self, name, features_cols=None):
        super().__init__(name, features_cols=features_cols)

        # mapping between unrolled to rolled vector features
        self._vector_features_mapping = {}

    @staticmethod
    def _is_feature_list_type(df, feature):
        """
        :param df: the features dataset.
        :type df: pandas.DataFrame

        :param feature: feature (column) name.
        :type feature: str

        :return: weather a feature inside a dataframe is a vector type.
        """
        # for empty DataFrame or non object column should be False
        if df.shape[0] == 0 or df[feature].dtype != 'object':
            return False

        # for non-empty DataFrame we should check for list or numpy array type
        list_supported_types = [list, np.array, np.ndarray]
        for supported_type in list_supported_types:
            if (df[feature].apply(type) == supported_type).all():
                return True
        return False

    def _unroll_list_feature(self, df, feature):
        """
        Unroll vector feature of a dataset inplace.

        :param df: the dataset to unroll.
        :type df: pandas.DataFrame

        :param feature: the vector feature (column) name.
        :type feature: str
        """
        if feature in self._vector_features_mapping:
            new_column_names = self._vector_features_mapping[feature]
        else:
            # retrieve feature vector length, assuming DataFrame isn't empty
            vector_dim = len(df[feature][0])

            # generate columns
            random_postfix = random_str(5)
            new_column_names = ['{}_{}_{}'.format(feature, random_postfix, i) for i in range(vector_dim)]
            self._vector_features_mapping[feature] = new_column_names

        df[new_column_names] = pd.DataFrame(df[feature].tolist(), index=df.index)
        del df[feature]

    def _get_effective_x(self, x, reset_features_mapping=False):
        """
        Receives features dataset that may contain vector features and returns unrolled dataset with narrowed features.

        :param x:  the dataset to procewss.
        :type x: pandas.DataFrame

        :param reset_features_mapping: weather to recalculate mapping between original vector features, to the unrolled ones.
                Note that usually in the fit process you usually want to recalculate, while in the predict you don't.
        :type reset_features_mapping: bool ,optional

        :return: the new unrolled dataframe
        """
        if self._features_cols is not None:
            # narrow down features
            effective_x = x[self._features_cols]
        else:
            effective_x = x
        effective_x = effective_x.copy()
        if reset_features_mapping:
            self._vector_features_mapping.clear()

        # unroll list type (a.k.a vector type) features to several features
        features_lst = [c for c in effective_x]
        for feature in features_lst:
            if BasicClassifier._is_feature_list_type(effective_x, feature):
                self._unroll_list_feature(effective_x, feature)
        return effective_x

    def fit(self, x, y, **kwargs):
        x = self._get_effective_x(x, reset_features_mapping=True)
        self._fit(x, y, **kwargs)

    def predict(self, x):
        x = self._get_effective_x(x, reset_features_mapping=False)
        return self._predict(x)

    def predict_proba(self, x):
        x = self._get_effective_x(x, reset_features_mapping=False)
        return self._predict_proba(x)

    def _predict(self, x):
        """
        The method receive a features dataset that MUST NOT contain vector features, and returns a class prediction for each row.

        :param x: the features dataset.

                Note that the training dataset may contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :return: list or numpy.array of classes predictions
        """
        pass

    def _predict_proba(self, x):
        """
        The method receive a features dataset, and returns classes probability prediction for each row.

        :param x: the features dataset.

                Note that the training dataset MUST NOT contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :return: list or numpy.array of classes probability predictions (may be also list or numpy.array).

                Note that the classes probability list order must be natively sorted (e.g. for string, alphabetically).
        """
        pass

    def _fit(self, x, y, **kwargs):
        """
        Training method on a given dataset with labels.

        :param x: the training dataset.
                Note that the training dataset MUST NOT contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :param y: labels of the training dataset.
        :type y: pandas.Series or list

        :param kwargs:
        """

        pass

