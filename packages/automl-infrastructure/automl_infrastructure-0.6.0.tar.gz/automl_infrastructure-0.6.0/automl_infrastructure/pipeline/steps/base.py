

class Step(object):
    def __init__(self, name, transformer):
        self._name = name
        self._transformer = transformer

    @property
    def name(self):
        return self._name

    @property
    def transformer(self):
        return self._transformer

    def fit(self, X, y):
        self._transformer.fit(X, y)

    def transform(self, X):
        return self._transformer.transform(X)

    def set_params(self, **kwargs):
        self._transformer.set_params(**kwargs)

    def get_params(self):
        return self._transformer.get_params()


class GenericStep(object):
    def __init__(self, name, transformer_class, **kwargs):
        self._name = name
        self._update_transformer(transformer_class, **kwargs)

    def fit(self, X, y):
        self._transformer.fit(X, y)

    def transform(self, X):
        return self._transformer.transform(X)

    @property
    def name(self):
        return self._name

    @property
    def transformer(self):
        return self._transformer

    def set_params(self, transformer_class, **kwargs):
        self._update_transformer(transformer_class, **kwargs)

    def _update_transformer(self, class_name, **kwargs):
        self._transformer = class_name(**kwargs)



