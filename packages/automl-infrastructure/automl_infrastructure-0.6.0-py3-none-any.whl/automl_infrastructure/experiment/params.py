from abc import ABC, abstractmethod


class ParameterSuggester(ABC):
    """
    The class ParameterSuggester represents an interface (API) for parameter suggester in the hyper-params
    optimization process.
    """

    @abstractmethod
    def suggest_continuous_float(self, name, low, high, log):
        """
        Suggests decimal value in the continuous range of [low,high], with the possibility of log scale.

        :param name: name of the hyper-param we want to get suggestion for.
        :type name: str

        :param low: lower bound range for suggestion.
        :type low: number

        :param high: higher bound range for suggestion.
        :type high: number

        :param log: weather to use log scale.
        :type log: bool

        :return the suggested number.
        """
        pass

    @abstractmethod
    def suggest_discrete_float(self, name, low, high, step):
        """
        Suggests decimal value in the discrete range of [low,high] with given step size.

        :param name: name of the hyper-param we want to get suggestion for.
        :type name: str

        :param low: lower bound range for suggestion.
        :type low: number

        :param high: higher bound range for suggestion.
        :type high: number

        :param step: the step size to pick discrete values.

        :return the suggested number (which may be low, low+step, low+2*step and ect').
        """
        pass

    @abstractmethod
    def suggest_int(self, name, low, high):
        """
        Suggests int value in the range of [low,high].

        :param name: name of the hyper-param we want to get suggestion for.
        :type name: str

        :param low: lower bound range for suggestion.
        :type low: int

        :param high: higher bound range for suggestion.
        :type high: int

        :return: the suggested number (which may be low, low+1, low+2 and ect').
        """
        pass

    @abstractmethod
    def suggest_list(self, name, options):
        """
        Suggests one value from a given list of values.

        :param name: name of the hyper-param we want to get suggestion for.
        :type name: str

        :param options: list of options for values.
        :type options: list of Any

        :return: one value from the given list of values
        """
        pass


class OptunaParameterSuggester(ParameterSuggester):
    """
    Wrapper for Optuna, to implement the :class:`automl_infrastructure.experiment.params.ParameterSuggester` interface.
    """

    def __init__(self, trial):
        self._trial = trial

    def suggest_continuous_float(self, name, low, high, log=False):
        if log:
            return self._trial.suggest_loguniform(name, low, high)
        else:
            return self._trial.suggest_uniform(name, low, high)

    def suggest_discrete_float(self, name, low, high, step):
        return self._trial.suggest_discrete_uniform(name, low, high, step)

    def suggest_int(self, name, low, high):
        return self._trial.suggest_int(name, low, high)

    def suggest_list(self, name, options):
        return self._trial.suggest_categorical(name, options)


class Parameter(ABC):
    """
    The Parameter interface defines API for params that can be used in the hyper-params declaration.
    """
    def __init__(self, name):
        """
        Initialize the parameter name.

        :param name: the name of the hyper-param.
        :type name: str
        """
        self._name = name

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    @abstractmethod
    def suggest(self, suggester):
        """
        Suggests value based on suggester.

        :param suggester: value suggester.
        :type suggester: :class:`automl_infrastructure.experiment.params.ParameterSuggester`

        :return: the suggested value by the suggester
        """
        pass

    @abstractmethod
    def copy(self):
        """
        :return: deep copy of the parameter.
        """
        pass


class RangedParameter(Parameter):
    """
    The RangedParameter implements the :class:`automl_infrastructure.experiment.params.ParameterSuggester` interface
    for ranged parameters, discrete or continuous, int or decimals.
    """
    def __init__(self, name, lower, upper, discrete=False, step_rate=None, log=False):
        """
        :param name: name of the hyper-parameter.
        :type name: str

        :param lower: lower bound range for suggestion.
        :type lower: number

        :param upper: higher bound range for suggestion.
        :type upper: number

        :param discrete: weather to suggest discrete value or continuous
        :type discrete: bool ,optional

        :param step_rate: for discrete decimal value, the required step size
        :type step_rate: number ,optional

        :param log: for continuous value, weather to use log scale.
        :type log: bool ,optional
        """
        super().__init__(name)
        self._lower = lower
        self._upper = upper
        self._discrete = discrete
        self._step_rate = step_rate
        self._log = log

    def suggest(self, suggester):
        # check weather we deal with floats or ints
        if isinstance(self._lower, int) and isinstance(self._upper, int):
            return suggester.suggest_int(self.name, self._lower, self._upper)
        else:
            effective_lower = float(self._lower)
            effective_upper = float(self._upper)
            # check weather discrete is needed or continuous one
            if self._discrete:
                return suggester.suggest_discrete_float(self.name, effective_lower, effective_upper, self._step_rate)
            else:
                return suggester.suggest_continuous_float(self.name, effective_lower, effective_upper, log=self._log)

    def copy(self):
        return RangedParameter(self._name, self._lower, self._upper, self._discrete, self._step_rate, self._log)


class ListParameter(Parameter):
    """
    The ListParameter implements the :class:`automl_infrastructure.experiment.params.ParameterSuggester` interface
    for parameters with closed number of options.
    """
    def __init__(self, name, options):
        """
        :param name: name of the hyper-parameter.
        :type name: str

        :param options: list of options values to choose from.
        :type options: list of Any
        """
        super().__init__(name)
        self._options = options

    def suggest(self, suggester):
        return suggester.suggest_list(self.name, self._options)

    def copy(self):
        return ListParameter(self._name, self._options)


