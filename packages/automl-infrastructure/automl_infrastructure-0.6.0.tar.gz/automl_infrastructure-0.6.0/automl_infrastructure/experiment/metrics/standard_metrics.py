from automl_infrastructure.experiment.metrics import Metric
from sklearn.metrics import f1_score, precision_score, recall_score, cohen_kappa_score, accuracy_score
from collections import OrderedDict


class Accuracy(Metric):
    """
    The class implements the accuracy metric.
    """
    def __init__(self, is_grouped=False, weighted=True):
        super().__init__(is_grouped, weighted)

    def measure(self, y_true, classifier_prediction):
        if self._is_grouped:
            if self._weighted:
                raise Exception('Accuracy metric may not be weighted: weighted should be False.')
            else:
                return accuracy_score(y_true, classifier_prediction.classes_pred)
        else:
            raise Exception('Accuracy metric must be grouped: is_grouped should be True.')


class F1Score(Metric):
    """
    The class implements the f1-score metric.
    """
    def __init__(self, is_grouped=False, weighted=True):
        super().__init__(is_grouped, weighted)

    def measure(self, y_true, classifier_prediction):
        if self._is_grouped:
            if self._weighted:
                return f1_score(y_true, classifier_prediction.classes_pred, average='weighted')
            else:
                return f1_score(y_true, classifier_prediction.classes_pred, average='micro')
        else:
            return f1_score(y_true, classifier_prediction.classes_pred, average=None)


class Precision(Metric):
    """
    The class implements the precision metric.
    """
    def __init__(self, is_grouped=False, weighted=True):
        super().__init__(is_grouped, weighted)

    def measure(self, y_true, classifier_prediction):
        if self._is_grouped:
            if self._weighted:
                return precision_score(y_true, classifier_prediction.classes_pred, average='weighted')
            else:
                return precision_score(y_true, classifier_prediction.classes_pred, average='micro')
        else:
            return precision_score(y_true, classifier_prediction.classes_pred, average=None)


class Recall(Metric):
    """
    The class implements the recall metric.
    """
    def __init__(self, is_grouped=False, weighted=True):
        super().__init__(is_grouped, weighted)

    def measure(self, y_true, classifier_prediction):
        if self._is_grouped:
            if self._weighted:
                return recall_score(y_true, classifier_prediction.classes_pred, average='weighted')
            else:
                return recall_score(y_true, classifier_prediction.classes_pred, average='micro')
        else:
            return recall_score(y_true, classifier_prediction.classes_pred, average=None)


class CohenKappa(Metric):
    """
    The class implements the cohen's kappa metric.
    Note that the cohen's kappa metric must be grouped.
    """
    def __init__(self, is_grouped=True, weighted=True, linear=True):
        """
        :param is_grouped: weather to aggregate classes score to single value.
        :type is_grouped: bool ,optional

        :param weighted: weather to use weights (according to classes size) during aggregation
        :type weighted: bool ,optional

        :param linear: weather to use linear cohen's kappa or quadratic one.
        :type linear: bool ,optional
        """
        super().__init__(is_grouped, weighted)
        self._linear = linear
        if not is_grouped:
            raise Exception('CohenKappa metric must be grouped: is_grouped should be True.')

    def measure(self, y_true, classifier_prediction):
        if self._weighted:
            if self._linear:
                weights = 'linear'
            else:
                weights = 'quadratic'
            return cohen_kappa_score(y_true, classifier_prediction.classes_pred, weights=weights)
        else:
            return cohen_kappa_score(y_true, classifier_prediction.classes_pred, weights=None)


class Support(Metric):
    """
    The class implements the support metric, that is, for every class how many instances it has.
    """
    def __init__(self, is_grouped=False, weighted=True):
        super().__init__(is_grouped, weighted)

    def measure(self, y_true, classifier_prediction):
        classes_occur_dict = Support._calculate_classes_occurrences(y_true)
        classes_occur = [v for v in classes_occur_dict.values()]
        if self._is_grouped:
            return sum(classes_occur)
        else:
            return classes_occur

    @staticmethod
    def _calculate_classes_occurrences(y_true):
        """
        Calculates for every class, its size.

        :param y_true: the true labels.
        :type y_true: pandas.Series or list

        :return: ordered list of classes sizes, according to the classes lexicography order.
        """
        classes_occur = {}
        for label in y_true:
            if label in classes_occur:
                classes_occur[label] += 1
            else:
                classes_occur[label] = 1
        return OrderedDict(sorted(classes_occur.items()))


class MetricFactory(object):
    """
    Factory of non-grouped metrics - metrics that return score for every class, rather than unified score, by their name.
    """
    standard_metrics = {
        'f1_score': F1Score(is_grouped=False),
        'precision': Precision(is_grouped=False),
        'recall': Recall(is_grouped=False),
        'support': Support(is_grouped=False)
    }

    @staticmethod
    def create(name):
        """
        Returns non-grouped :class:`automl_infrastructure.experiment.metrics.base.Metric` object, by given name.

        :param name: the name of the metric must be selected from the closed pre-defined group
                        ['f1_score', 'precision', 'recall', 'support'].

        :return: non-grouped :class:`automl_infrastructure.experiment.metrics.base.Metric` object, by given name.
        """
        if name not in MetricFactory.standard_metrics:
            raise Exception('Metric named {} is not supported'.format(name))
        return MetricFactory.standard_metrics[name]


class ObjectiveFactory(object):
    """
    Factory of grouped metrics - metrics that return aggregated one score, by their name.
    """
    standard_objectives = {
        'accuracy': Accuracy(is_grouped=True, weighted=False),
        'f1_score': F1Score(is_grouped=True, weighted=False),
        'weighted_f1_score': F1Score(is_grouped=True, weighted=True),
        'precision': Precision(is_grouped=True, weighted=False),
        'weighted_precision': Precision(is_grouped=True, weighted=True),
        'recall': Recall(is_grouped=True, weighted=False),
        'weighted_recall': Recall(is_grouped=True, weighted=True),
        'linear_cohen_kappa': CohenKappa(is_grouped=True, weighted=True, linear=True),
        'quadratic_cohen_kappa': CohenKappa(is_grouped=True, weighted=True, linear=False),
        'cohen_kappa': CohenKappa(is_grouped=True, weighted=False)
    }

    @staticmethod
    def create(name):
        """
        Returns grouped :class:`automl_infrastructure.experiment.metrics.base.Metric` object, by given name.

        :param name: the name of the metric must be selected from the closed pre-defined group
                    ['accuracy', 'weighted_f1_score', 'f1_score', 'weighted_precision', 'precision',
                    'weighted_recall', 'recall', 'linear_cohen_kappa', 'quadratic_cohen_kappa', 'cohen_kappa'].

        :return: grouped :class:`automl_infrastructure.experiment.metrics.base.Metric` object, by given name.
        """
        if name not in ObjectiveFactory.standard_objectives:
            raise Exception('Objective named {} is not supported'.format(name))
        return ObjectiveFactory.standard_objectives[name]


