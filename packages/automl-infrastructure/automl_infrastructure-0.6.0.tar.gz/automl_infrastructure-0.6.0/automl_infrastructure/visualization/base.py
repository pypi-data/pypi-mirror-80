from abc import ABC, abstractmethod


class Visualization(ABC):
    """
    The class Visualization represents an interface (API) for all kind of visualizations.
    """

    @abstractmethod
    def fit(self, y_true_lst, classifier_prediction_lst):
        """
        Fits the visualization with a given sets of true labels list and classifier predictions list.

        :param y_true_lst: list of true labels list
        :type y_true_lst: list of pandas.Series or list

        :param classifier_prediction_lst: list of classes predictions.
        :type classifier_prediction_lst: list of :class:`automl_infrastructure.classifiers.base.ClassifierPrediction`
        """
        pass

    @abstractmethod
    def show(self):
        """
        Shows the visualization (may be matplotlib diagram or any kind of printing).
        """
        pass

