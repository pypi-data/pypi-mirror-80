from abc import ABC, abstractmethod
from collections import OrderedDict
import numpy as np


class Metric(ABC):
    """
    The class Metric defines an interface for metrics.
    Formally speaking, metric may:
    - aggregate classes scores to a single score (e.g. average precision of all classes).
    - if aggregation was required, weather to weight classes according to their
        size (e.g. weighted average precision of all classes).
    """
    def __init__(self, is_grouped=False, weighted=True):
        """
        :param is_grouped: weather to aggregate classes score to single value.
        :type is_grouped: bool ,optional

        :param weighted: weather to use weights (according to classes size) during aggregation
        :type weighted: bool ,optional
        """
        self._is_grouped = is_grouped
        self._weighted = weighted

    @abstractmethod
    def measure(self, y_true, classifier_prediction):
        """
        The method receives true labels and prediction (class prediction along all classes probabilities)
        and returns score for each class if aggregation wasn't asked by the user, and one score otherwise.

        :param y_true: true labels
        :type y_true: pandas.Series or list

        :param classifier_prediction: class prediction with classes probabilities list
        :type classifier_prediction: list of :class:`automl_infrastructure.classifiers.base.ClassifierPrediction`

        :return: if aggregation wasn't asked by the user, list of classes scores ordered by
         classes nature sorting (e.g. alphabetically for classes of type string)
         and one score otherwise (weighted if was asked by the user).
        """
        pass


class SimpleMetric(Metric, ABC):
    """
    The abstract class SimpleMetric partly implements the :class:`automl_infrastructure.experiment.metrics.base.Metric` interface.
    Its main goal is implementing the classes order and weights aggregation for future sub-classes (concrete metrics).
    """

    def __init__(self, is_grouped=False, weighted=True):
        super().__init__(is_grouped=is_grouped, weighted=weighted)

    def measure(self, y_true, classifier_prediction):
        classes_measure = self.measure_lst(y_true, classifier_prediction)
        classes_measure = [v[1] for v in classes_measure.items()]
        if self._is_grouped:
            if self._weighted:
                # calculate the total number of distinct classes
                classes_num = len(set(y_true + classifier_prediction.classes_pred))

                # calculate size of every class, while keeping classes natural order
                classes_size = SimpleMetric._calculate_classes_occurrences(y_true, classifier_prediction.classes_pred)
                weighted_sum = 0.0
                for i in range(len(classes_measure)):
                    if classes_num[i] > 0:
                        weighted_sum += classes_measure[i] / classes_size[i]
                weighted_sum = weighted_sum / classes_num
                return weighted_sum
            else:
                return np.mean(classes_measure)
        else:
            return classes_measure

    @abstractmethod
    def measure_lst(self, y_true, classifier_prediction):
        """
        Same as measure method, but returns a dictionary of classes and their scores.

        :param y_true: true labels
        :type y_true: pandas.Series or list

        :param classifier_prediction: class prediction with classes probabilities list
        :type classifier_prediction: :class:`automl_infrastructure.classifiers.base.ClassifierPrediction`

        :return: a dictionary of classes and their scores
        """
        pass

    @staticmethod
    def _calculate_classes_occurrences(y_true, y_pred):
        """
        Calculate the size of each class and return a sorted list of sizes according to classes order.

        :param y_true: true labels.
        :type y_true: pandas.Series or list

        :param y_pred: classes predictions.
        :type y_pred: list or numpy.array

        :return: a sorted list of sizes according to classes order.
        """
        classes_occur = {}
        joint_classes = y_true+y_pred
        for label in joint_classes:
            if label in classes_occur:
                classes_occur[label] += 1
            else:
                classes_occur[label] = 1
        return [v[1] for v in OrderedDict(sorted(classes_occur.items()))]
