from automl_infrastructure.classifiers import Classifier


class Pipeline(Classifier):
    def __init__(self, name, steps):
        super().__init__(name)
        if len(steps) < 1:
            raise Exception("Pipeline must have at least one step.")
        self._last_step = steps[-1]
        if not isinstance(self._last_step, Classifier):
            raise Exception("Pipeline's last step must be {} type.".format(type(Classifier)))
        self._steps = steps
    
    @property
    def last_step(self):
        return self._last_step

    @property
    def steps(self):
        return self._steps
        
    def fit(self, X, y):
        effective_X = X
        for step in self._steps[:-1]:
            step.fit(effective_X, y)
            effective_X = step.transform(effective_X)
        self._steps[-1].fit(effective_X, y)

    def predict(self, X):
        effective_X = self._calculate_effective_X(X)
        return self._steps[-1].predict(effective_X)

    def predict_proba(self, X):
        effective_X = self._calculate_effective_X(X)
        return self._steps[-1].predict_proba(effective_X)

    def _calculate_effective_X(self, X):
        effective_X = X
        for step in self._steps[:-1]:
            effective_X = step.transform(effective_X)
        return effective_X

    def set_params(self, params):
        # update all steps params except for last step
        for step in self._steps[:-1]:
            if step.name in params:
                step.set_params(**params[step.name])

        # update last step params
        if self._steps[-1].name in params:
            self._steps[-1].set_params(params[self._steps[-1].name])

    def get_params(self, deep=True):
        params = {self._steps[-1].name: self._steps[-1].get_params()}
        return params




