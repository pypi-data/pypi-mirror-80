from automl_infrastructure.experiment.metrics import SimpleMetric
from sklearn.metrics import precision_recall_curve
from sklearn.preprocessing import LabelBinarizer
from collections import OrderedDict
import numpy as np


class ThresholdMinPrecision(SimpleMetric):
    """
    The metric find the threshold of the model, for a given precision, using the precision-recall curve.
    """
    def __init__(self, precision, is_grouped=False, weighted=True):
        """
        :param precision: the given precision to find the threshold on.
        :type precision: any number

        :param is_grouped: weather to aggregate classes score to single value.
        :type is_grouped: bool ,optional

        :param weighted: weather to use weights (according to classes size) during aggregation
        :type weighted: bool ,optional
        """
        super().__init__(is_grouped=is_grouped, weighted=weighted)
        self._precision = precision

    def measure_lst(self, y_true, classifier_prediction):
        # transform classes to binary vectors
        classes = [c for c in y_true] + [c for c in classifier_prediction.classes_pred]
        classes = sorted(list(set(classes)))
        binarizer = LabelBinarizer()
        binarizer.fit(classes)
        y_true_binary = binarizer.transform(y_true)

        # generate metric for every class
        classes_value = OrderedDict()
        if len(classes) == 2:
            y_true_binary = np.column_stack([(1 - y_true_binary)[:, 0], y_true_binary[:, 0]])
        
        for idx, c in enumerate(classes):
            precision_lst, recall_lst, ticks = precision_recall_curve(y_true_binary[:, idx],
                                                                      classifier_prediction.classes_proba[:, idx])
            classes_value[c] = ThresholdMinPrecision._find_threshold_above(ticks, recall_lst, precision_lst, self._precision)
        return classes_value

    @staticmethod
    def _find_threshold_above(ticks, indicators, values, threshold_value):
        """
        Find the first threshold that the precision of the threshold, according to the precision-recall curve
        is above the given precision.

        :param ticks: ticks of the precision-recall graph we want to find the threshold in.
        :type ticks: list of numbers

        :param indicators: the indicator list (e.g. ordered by ticks recall values).
        :type indicators: list of numbers

        :param values: the values we want to examine (e.g. ordered by ticks precision values).
        :type values: list of numbers

        :param threshold_value: minimum required value.
        :type threshold_value: number

        :return: the first indicator value, that its corresponded value in values, above the given threshold.
        """
        value = 0.0
        best_threshold = 1.01
        for i in range(len(ticks)):
            if threshold_value <= values[i] and indicators[i] > value:
                value = indicators[i]
                best_threshold = ticks[i]
        return best_threshold

