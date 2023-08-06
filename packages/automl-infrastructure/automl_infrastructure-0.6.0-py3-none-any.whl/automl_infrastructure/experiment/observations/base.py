from abc import ABC, abstractmethod
from automl_infrastructure.experiment.metrics import MetricFactory
from automl_infrastructure.experiment.metrics import Metric
import pandas as pd


class Observation(ABC):
    """
    The Observation class wraps metric and defines aggregation on top of the metric scores list.
    For instance, suppose we have list of accuracy scores, potential aggregations may be mean, std and ect'.
    Note that the metric must be non-aggregated one, that is, the metric should give score for every class.
    """
    def __init__(self, metric):
        """
        Initialize callable metric by a given metric.

        :param metric: the metric we want to aggregate on top.
        :type metric: str, callable or :class:`automl_infrastructure.experiment.metrics.base.Metric`
        """
        if isinstance(metric, str):
            metric_obj = MetricFactory.create(metric)
            self._metric_func = lambda y_true, classifier_prediction: metric_obj.measure(y_true, classifier_prediction)
        elif isinstance(metric, Metric):
            self._metric_func = lambda y_true, classifier_prediction: metric.measure(y_true, classifier_prediction)
        elif callable(metric):
            self._metric_func = metric
        else:
            raise Exception('Unsupported metric type {} for observation.'.format(type(metric)))

    @abstractmethod
    def observe(self, y_true_lst, classifier_prediction_lst, output_class_col='CLASS', output_observation_col='OBSERVATION'):
        """
        The method receives set of true labels list and set of predictions list, and returns the aggregated score for each class.
        The concept of such aggregation is extremely useful in the k-fold cross-validation method, when you
        want to average all folds scores for every class.

        :param y_true_lst: list if true labels sets.
        :type y_true_lst: list of pandas.Series or list

        :param classifier_prediction_lst: list of classes predictions.
        :type classifier_prediction_lst: list of :class:`automl_infrastructure.classifiers.base.ClassifierPrediction`

        :param output_class_col: class column name for the output DataFrame.
        :type output_class_col: str ,optional

        :param output_observation_col: score column name for the output DataFrame.
        :type output_observation_col: str ,optional

        :return: pandas DataFrame with aggregated metric value for each class.
        """
        pass


class SimpleObservation(Observation):
    """
    The class SimpleObservation implements generic observation, leaving the aggregation implementation
    part for the sub-classes.
    """
    def __init__(self, metric):
        super().__init__(metric)

    @abstractmethod
    def agg_func(self, values):
        """
        Gets list of values and return aggregated value on top of them (e.g. mean, standard deviation and ect').

        :param values: list of values to aggregate.
        :type values: list of numbers

        :return: single aggregated value.
        """
        pass

    def observe(self, y_true_lst, classifier_prediction_lst, output_class_col='CLASS', output_observation_col='OBSERVATION'):
        # extract all unique classes names
        unique_classes_names = []
        for j in range(len(classifier_prediction_lst)):
            for i in range(len(classifier_prediction_lst[j].classes_pred)):
                if classifier_prediction_lst[j].classes_pred[i] not in unique_classes_names:
                    unique_classes_names.append(classifier_prediction_lst[j].classes_pred[i])
                if y_true_lst[j][i] not in unique_classes_names:
                    unique_classes_names.append(y_true_lst[j][i])
        unique_classes_names = sorted(unique_classes_names)

        # prepare dictionary of classes and their metric values
        classes_observations_dict = {}
        for class_label in unique_classes_names:
            classes_observations_dict[class_label] = []

        # collect values for each class
        for classifier_prediction, y_true in zip(classifier_prediction_lst, y_true_lst):
            metric_values = self._metric_func(y_true, classifier_prediction)
            for i in range(len(metric_values)):
                classes_observations_dict[unique_classes_names[i]].append(metric_values[i])

        # aggregate values for each class
        for class_label in classes_observations_dict:
            classes_observations_dict[class_label] = self.agg_func(classes_observations_dict[class_label])

        classes_col = []
        observation_col = []
        for key, value in classes_observations_dict.items():
            classes_col.append(key)
            observation_col.append(value)
        return pd.DataFrame.from_dict({output_class_col: classes_col, output_observation_col: observation_col})








