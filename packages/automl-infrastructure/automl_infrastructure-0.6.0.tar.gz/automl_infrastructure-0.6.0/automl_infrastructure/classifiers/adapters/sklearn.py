from automl_infrastructure.classifiers import BasicClassifier
from sklearn.preprocessing import LabelEncoder


class SklearnClassifierAdapter(BasicClassifier):
    """
    The SklearnClassifierAdapter implements an adapter (wrapper) for sklearn classifiers,
    to match the :class:`automl_infrastructure.classifiers.base.Classifier` contract.
    """
    def __init__(self, name, sklearn_model, features_cols=None, encode_labels=False):
        """
        :param name: name of the classifier (e.g. 'lr1).
        :type name: str

        :param sklearn_model: sklearn classifier to wrap.

        :param features_cols: features list that the classifier should work on, while ignoring other features.
        :type features_cols: list of str ,optional

        :param encode_labels: weather to encode the labels
        :type encode_labels: bool ,optional
        """
        super().__init__(name, features_cols=features_cols)
        self._sklearn_model = sklearn_model
        self._encode_labels = encode_labels
        if encode_labels:
            self._label_encoder = LabelEncoder()

    def _fit(self, x, y, **kwargs):
        """
        Training method on a given dataset with labels.

        :param x: the training dataset.
                Note that the training dataset MUST NOT contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :param y: labels of the training dataset.
        :type y: pandas.Series or list

        :param kwargs: additional params for the inner sklearn classifier.
        """
        if self._encode_labels:
            self._label_encoder.fit(y)
            y = self._label_encoder.transform(y)
        self._sklearn_model.fit(x, y, **kwargs)

    def _predict(self, x):
        """
        The method receive a features dataset , and returns a class prediction for each row.

        :param x: the features dataset.

                Note that the training dataset MUST NOT  contain features of type vector (list or numpy.array).
        :type x: pandas.DataFrame

        :return: list or numpy.array of classes predictions
        """

        prediction_df = self._sklearn_model.predict(x)
        if self._encode_labels:
            prediction_df = self._label_encoder.inverse_transform(prediction_df)
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
        prediction_df = self._sklearn_model.predict_proba(x)
        return prediction_df

    def set_params(self, params):
        self._sklearn_model.set_params(**params)

    def get_params(self, deep=True):
        return self._sklearn_model.get_params(deep=deep)

