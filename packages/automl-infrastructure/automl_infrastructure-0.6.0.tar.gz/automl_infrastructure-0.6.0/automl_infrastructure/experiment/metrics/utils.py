from automl_infrastructure.experiment.metrics import MetricFactory, Metric, ObjectiveFactory


def parse_metric(metric):
    """
    Receive metric and return callable that calculate the metric.

    :param metric: the metric to parse.
    :type metric: str, callable or :class:`automl_infrastructure.experiment.metrics.base.Metric`

    :return: callable (list of Any, list of :class:`automl_infrastructure.classifiers.base.ClassifierPrediction` ->
     number or list of numbers) that calculate the metric.
    """
    if isinstance(metric, str):
        metric_obj = MetricFactory.create(metric)
        metric_func = lambda y_true, classifier_prediction: metric_obj.measure(y_true, classifier_prediction)
    elif isinstance(metric, Metric):
        metric_func = lambda y_true, classifier_prediction: metric.measure(y_true, classifier_prediction)
    elif callable(metric):
        metric_func = metric
    else:
        raise Exception('Unsupported given metric.')
    return metric_func


def parse_objective(objective):
    """
    Receive objective (aggregated metric) and return callable that calculate the metric.

    :param objective: the objective to parse.
    :type objective: str or callable

    :return: callable (list of Any, list of :class:`automl_infrastructure.classifiers.base.ClassifierPrediction` ->
     number) that calculate the metric.
    """
    if callable(objective):
        return objective
    elif isinstance(objective, str):
        objective = ObjectiveFactory.create(objective)
        return lambda y_true, classifier_prediction: objective.measure(y_true, classifier_prediction)
    else:
        raise Exception('Unsupported given objective (scoring).')