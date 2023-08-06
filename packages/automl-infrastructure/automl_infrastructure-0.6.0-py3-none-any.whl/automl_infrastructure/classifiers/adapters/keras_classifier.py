from automl_infrastructure.classifiers import BasicClassifier
from sklearn.preprocessing import LabelBinarizer
import numpy as np


class KerasClassifierAdapter(BasicClassifier):
    """
    The KerasClassifierAdapter implements an adapter (wrapper) for keras models,
    to match the :class:`automl_infrastructure.classifiers.base.Classifier` contract.
    """

    def __init__(self, name, keras_classifier, features_cols=None):
        """
        :param name: name of the classifier (e.g. 'lr1).
        :type name: str

        :param keras_classifier: keras classifier to wrap.

        :param features_cols: features list that the classifier should work on, while ignoring other features.
        :type features_cols: list of str ,optional
        """

        super().__init__(name, features_cols=features_cols)
        self._keras_classifier = keras_classifier
        self._label_binarizer = LabelBinarizer()

    def _fit(self, x, y, **kwargs):
        """
        Training method on a given dataset with labels.
        Note that the labels are encoded to binary form.

        :param x: the training dataset.
                Note that the training dataset MUST NOT contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :param y: labels of the training dataset.
        :type y: pandas.Series or list

        :param kwargs: additional params for the inner sklearn classifier.
        """

        self._label_binarizer.fit(y)

        # transform labels to binary form, to match keras models
        y_binarized = self._label_binarizer.transform(y)
        self._keras_classifier.fit(x, y_binarized, **kwargs)

    def _predict(self, x):
        """
        The method receive a features dataset , and returns a class prediction for each row, while
        the predicted labels auto-decoded to its original form.

        :param x: the features dataset.

                Note that the training dataset MUST NOT  contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :return: list or numpy.array of classes predictions
        """

        prediction_df = self._keras_classifier.predict(x)

        # transform vectors predictions to labels
        prediction_df = np.array(list(map(lambda i: self._label_binarizer.classes_[i], prediction_df)))
        return prediction_df

    def _predict_proba(self, x):
        """
        The method receive a features dataset, and returns classes probability prediction for each row.

        :param x: the features dataset.

                Note that the training dataset MUST NOT contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :return: list or numpy.array of classes probability predictions (may be also list or numpy.array).

                Note that the classes probability list order must be natively sorted (e.g. for string, alphabetically).
        """

        prediction_df = self._keras_classifier.predict_proba(x)
        return prediction_df

    def set_params(self, params):
        self._keras_classifier.set_params(**params)

    def get_params(self, deep=True):
        return self._keras_classifier.get_params(deep=deep)

