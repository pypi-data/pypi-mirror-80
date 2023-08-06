import copy
import operator
from functools import reduce
from time import strftime, gmtime
import dill
import numpy as np
import optuna
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import shuffle
from automl_infrastructure.classifiers import ClassifierPrediction
from automl_infrastructure.experiment.metrics.standard_metrics import ObjectiveFactory
from automl_infrastructure.experiment.params import OptunaParameterSuggester
from automl_infrastructure.utils import random_str


class Experiment(object):
    """The Experiment class represents cross-validation training and testing process on a given set of models
       with hyper-parameters optimization support (optional) built in, and predefined/custom metrics for observation.

       In the end of the process, you may watch a report that among other things includes:
            - the best model together with its parameters.
            - metrics (observations) summary on the divided training and validation sets.
            - visualizations (e.g. confusion matrix) summary on the divided training and validation sets.
        """

    def __init__(self, name, x, y, models, hyper_parameters={}, observations={}, visualizations={},
                 objective='accuracy', objective_name=None, maximize=True,
                 n_folds=3, n_repetitions=5, additional_training_data_x=None, additional_training_data_y=None):
        """
        :param name: the name of the experiment.
        :type name: str

        :param x: dataframe that represents the features (every column is a feature).
                Note that the column type may be also a vector (list or numpy array).
        :type x: pandas.DataFrame.

        :param y: labels.
        :type y: pandas.Series or list

        :param models: list of classifiers to be examined.
        :type models: list of :class:`automl_infrastructure.classifiers.base.Classifier`

        :param hyper_parameters: dictionary that contains for each model its, list of parameters to optimize.

                Note that for complex models the consists of sub-models, every sub-model may have its own list
                    parameters under the father model hierarchy - for instance:
                     {
                        'parent_model:
                        {sub_model1: [RangedParameter(..), ..],
                        {sub_model2: [RangedParameter(..), ..]}
                     }.
        :type hyper_parameters: dict of {str: list of :class:`automl_infrastructure.experiment.params.Parameter`} (, optional)

        :param observations: dictionary of observation name and its observation
                        object that defines some aggregation upon metric (e.g. Std(metric='precision')).
                        Note that the observation will be calculated on every class in the labels, and will be
                        shown in the final report by its name.
        :type observations: dict of {str: :class:`automl_infrastructure.experiment.observations.base.Observation`} (, optional)

        :param visualizations: dictionary of visualization name and its visualization object that defines some visualization that will be shown in the final report
                         by its name (e.g. ConfusionMatrix()).
        :type visualizations: dict of {str: :class:`automl_infrastructure.visualization.base.Visualization`} (, optional)

        :param objective: if hyper_parameters was supplied by the user, the optimization process will try to maximize or minimize the given objective.
                        If no objective supplied, 'accuracy' will be the default.
        :type objective: str or callable (, optional)

        :param objective_name: name of the objective that will be shown in the final report.
        :type objective_name: str (, optional)

        :param maximize: weather to maximize or minimize the objective during the hyper-parameters optimization process.
        :type maximize: bool (, optional)

        :param n_folds: number of folds to use in the repeated k-fold cross-validation splitting.
        :type n_folds: int (, optional)

        :param n_repetitions: number of repeats to use in the repeated k-fold cross-validation splitting.
        :type n_repetitions: int (, optional)

        :param additional_training_data_x: additional training data that won't
                        be divided in the cross-validation process, but will be added to the k-1 training folds on
                        all iterations.
        :type additional_training_data_x: pandas.DataFrame (, optional)

        :param additional_training_data_y: labels of the additional_training_data_x.
        :type additional_training_data_y: pandas.Series or list (, optional)
        """

        self._name = name
        self._x = x
        self._y = y
        self._additional_training_data_x = additional_training_data_x
        self._additional_training_data_y = additional_training_data_y
        self._models = models
        self._hyper_parameters = hyper_parameters
        self._observations = observations
        self._visualizations = visualizations
        self._objective_name = objective_name
        self._objective = self._parse_objective(objective)
        self._objective_direction = 'maximize' if maximize else 'minimize'

        # set parameters for repeated k-fold cross validation
        self._n_folds = n_folds
        self._n_repetitions = n_repetitions

        # initialize output results
        self._models_test_observations = {}
        self._models_train_observations = {}
        self._models_test_visualizations = {}
        self._models_train_visualizations = {}
        self._models_best_params = {}
        self._models_best_scores = {}
        self._models_train_best_scores = {}
        self._best_model_name = None

        self._start_time = None
        self._end_time = None

    @property
    def X(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def additional_training_data_X(self):
        return self._additional_training_data_x

    @property
    def additional_training_data_y(self):
        return self._additional_training_data_y

    @property
    def objective_name(self):
        return self._objective_name

    @property
    def best_model(self):
        """ returns the best model that was found during the experiment, with its best hyper-params"""

        best_model = None
        for model in self._models:
            if model.name == self._best_model_name:
                best_model = model
        best_model.set_params(self._models_best_params[best_model.name])
        return best_model

    @property
    def end_time(self):
        return self._end_time

    def objective_score(self, model_name, group='test'):
        """
        :param model_name: the name of the model.
        :param group: 'train' or 'test'.
        :return: the objective score of the given model, on the given group - 'train' or 'test'.
        """

        if group == 'train':
            best_scores = self._models_train_best_scores
        elif group == 'test':
            best_scores = self._models_best_scores
        else:
            raise Exception('Unsupported group {}, only [\'train\', \'test\'] are supported.'.format(group))

        if model_name not in best_scores:
            raise ('Could not find model named {}.'.format(model_name))
        return best_scores[model_name]

    def _parse_objective(self, objective):
        """
        :param objective: name of objective or callable.
                        Note that if callable is supplied, objective_name must also be supplied for the final report.
        :return: callable that receives true labels and classifier prediction, and returns scalar scoring.
        """
        if callable(objective):
            if self._objective_name is None:
                raise Exception('You must specified objective_name for callable objective function.')
            return objective
        elif isinstance(objective, str):
            if self._objective_name is None:
                self._objective_name = objective
            objective = ObjectiveFactory.create(objective)
            return lambda y_true, classifier_prediction: objective.measure(y_true, classifier_prediction)
        else:
            raise Exception('Only objective name or callable are supported.')

    @staticmethod
    def _build_hyper_params_translation(model_name, hyper_params):
        """
        The function shallows high-hierarchy dictionary of hyper-params, including renaming to avoid collisions.
        For example, imagine we have model named 'blending', with two sub-models:
            -input: 'blending', { 'blending':{ 'sub_lr1': [ListParameter('C', options=[0.1, 0.5])],
                                   'sub_lr2': [ListParameter('C', options=[0.1, 0.5])]}}
            -output: ({'C_03043': 'C', 'C_57731': 'C'},
                     {'C_03043': <automl_infrastructure.experiment.params.ListParameter at 0x153643f5e48>,
                      'C_57731': <automl_infrastructure.experiment.params.ListParameter at 0x153639fb6c8>},
                     {'sub_lr1': [<automl_infrastructure.experiment.params.ListParameter at 0x153643f5e48>],
                      'sub_lr2': [<automl_infrastructure.experiment.params.ListParameter at 0x153639fb6c8>]})

        :param model_name: name of a model.
        :param hyper_params: dictionary of all hyper-params, by their model name.
        :return: tuple of:
                    - mapping of new to old hyper-params names.
                    - mapping from new hyper-params to their new Parameter objects.
                    - mapping rom all sub-models to their new Parameter objects.
        """
        model_hyper_params = hyper_params[model_name]
        translation_result = {}
        new_params_flat = {}

        # check leaf
        if not isinstance(model_hyper_params, dict):
            new_params_hirerachy = []
            for param in model_hyper_params:
                random_name = '{0}_{1}'.format(param.name, random_str(length=5))
                translation_result[random_name] = param.name
                new_param = param.copy()
                new_param.set_name(random_name)
                new_params_flat[random_name] = new_param
                new_params_hirerachy.append(new_param)
        else:
            new_params_hirerachy = {}
            for key in model_hyper_params.keys():
                translation_iter, new_params_flat_iter, new_params_hirerachy[
                    key] = Experiment._build_hyper_params_translation(key, model_hyper_params)
                translation_result.update(translation_iter)
                new_params_flat.update(new_params_flat_iter)

        return translation_result, new_params_flat, new_params_hirerachy

    @staticmethod
    def _translate_best_params(new_hyper_parameters, translation, best_params):
        """
        The function translate from the new shallow params form, to the old form.
        :param new_hyper_parameters: the new shallow params form as dict.
        :param translation: mapping from new param name to old param name.
        :param best_params: mapping from new params names to its best found value.
        :return: best params hierarchy with the old params names and their best values.
        """

        result = {}
        if not isinstance(new_hyper_parameters, dict):
            for param, value in best_params.items():
                new_hyper_parameters_names = [p.name for p in new_hyper_parameters]
                if param in new_hyper_parameters_names:
                    result[translation[param]] = value
        else:
            for model_name, inner_hyper_parameters_dict in new_hyper_parameters.items():
                result[model_name] = Experiment._translate_best_params(inner_hyper_parameters_dict, translation,
                                                                       best_params)

        return result

    def run(self, n_trials=3, n_jobs=15):
        """
        This method is the core method of the Experiment class, that:
            - run hyper-param optimization on all models (optional, if hyper-params dict was supplied).
            - evaluate the given observations (metrics) on the models with their best params.
            - create visualizations on the models with their best params.
        In the process of evaluation and optimization we use the repeated k-fold validation method.

        :param n_trials: number of trials during the optimization process (look at Optuna for deep understanding).
        :param n_jobs: number of parallel workers to use during the
                    optimization process (look at Optuna for deep understanding).
        """
        # init starting time
        self._start_time = gmtime()
        for model in self._models:
            # check weather model have hyper-parameters
            if model.name not in self._hyper_parameters or n_trials <= 0:
                best_params = {}
            else:
                # translate params names
                translation, new_params_flat, new_params_hierarchy = Experiment._build_hyper_params_translation(
                    model.name,
                    self._hyper_parameters)
                best_params = self._optimize_model(model, n_jobs, self._n_folds, self._n_repetitions, n_trials,
                                                   new_params_flat, new_params_hierarchy, translation)
                best_params = Experiment._translate_best_params(new_params_hierarchy, translation, best_params)
            self._models_best_params[model.name] = best_params

        # update observations and best scores
        self.refresh()

        # init end time
        self._end_time = gmtime()

    def _optimize_model(self, model, n_jobs, n_folds, n_repeatations, n_trials, new_params_flat, new_params_hierarchy,
                        translation):
        """
        This function optimize given model using optuna.
        :param model: the model to optimize.
        :param n_jobs: number of parallel workers to use during the
                            optimization process (look at Optuna for deep understanding).
        :param n_folds: number of folds in the repeated k-fold validation.
        :param n_repeatations: number of repeats in the repeated k-fold validation.
        :param n_trials: number of trials during the optimization process (look at Optuna for deep understanding).
        :param new_params_flat: the new shallow params form as dict.
        :param new_params_hierarchy: params hierarchy.
        :param translation: mapping from new param name to old param name.
        :return: the best params found by optuna.
        """

        def optuna_objective(trial):
            # set params of model
            optuna_suggestor = OptunaParameterSuggester(trial)
            suggested_params = {}
            for new_param_name, new_param in new_params_flat.items():
                suggested_params[new_param_name] = new_param.suggest(optuna_suggestor)
            suggested_params_translated = Experiment._translate_best_params(new_params_hierarchy, translation,
                                                                            suggested_params)

            # copy model for multi-threaded support
            copied_model = copy.deepcopy(model)
            copied_model.set_params(suggested_params_translated)

            # repeat k fold
            for i in range(0, n_repeatations):
                # split training data to k folds
                k_fold = StratifiedKFold(n_splits=n_folds, shuffle=True)
                scores = []
                for train_index, test_index in k_fold.split(self._x, self._y):
                    X_train, X_test = self._x.iloc[train_index], self._x.iloc[test_index]
                    y_train, y_test = self._y.iloc[train_index], self._y.iloc[test_index]
                    if self._additional_training_data_x is not None:
                        X_train = X_train.append(self._additional_training_data_x)
                        y_train = y_train.append(self._additional_training_data_y)
                        X_train, y_train = shuffle(X_train, y_train)
                    copied_model.fit(X_train, y_train.values.ravel())

                    # wrap prediction
                    pred_y = copied_model.predict(X_test)
                    proba_y = copied_model.predict_proba(X_test)
                    classifier_prediction = ClassifierPrediction(pred_y, proba_y)

                    score = self._objective(y_test.values.ravel(), classifier_prediction)
                    scores.append(score)
            return np.mean(scores)

        study = optuna.create_study(study_name='{0}_{1}'.format(self._name, model.name),
                                    direction=self._objective_direction)
        study.optimize(optuna_objective, n_trials=n_trials, n_jobs=n_jobs)
        return study.best_params

    def refresh(self):
        """
        The method regenerate observations (metrics) and visualizations for all models.
        """
        current_best_score = None
        for model in self._models:
            best_params = self._models_best_params[model.name]
            # set models params for observation creation
            model.set_params(best_params)

            # generate observations and score of model
            self._generate_model_results(model, self._n_folds, self._n_repetitions)

            # update best model
            best_score = self._models_best_scores[model.name]
            if current_best_score is None or (
                    self._objective_direction == 'maximize' and best_score > current_best_score) \
                    or (self._objective_direction == 'minimize' and best_score < current_best_score):
                self._best_model_name = model.name
                current_best_score = best_score

    def _generate_model_results(self, model, n_folds, n_repetitions):
        """
        Same as refresh method, for a specified model.
        :param model: Classifier to evaluate.
        :param n_folds: number of folds in the repeated k-fold validation.
        :param n_repetitions: number of repeats in the repeated k-fold validation.
        """

        test_y_true_lst = []
        test_classifier_predictions_lst = []
        train_y_true_lst = []
        train_classifier_predictions_lst = []
        test_scores = []
        train_scores = []
        # repeat k fold
        for i in range(0, n_repetitions):
            # split training data to k folds
            k_fold = StratifiedKFold(n_splits=n_folds, shuffle=True)
            for train_index, test_index in k_fold.split(self._x, self._y):
                # X_train, X_test = self._x[train_index, :], self._x[test_index, :]
                X_train, X_test = self._x.iloc[train_index], self._x.iloc[test_index]
                y_train, y_test = self._y.iloc[train_index], self._y.iloc[test_index]
                if self._additional_training_data_x is not None:
                    X_train = X_train.append(self._additional_training_data_x)
                    y_train = y_train.append(self._additional_training_data_y)
                    X_train, y_train = shuffle(X_train, y_train)
                model.fit(X_train, y_train.values.ravel())

                # wrap prediction for test
                pred_y = model.predict(X_test)
                proba_y = model.predict_proba(X_test)
                test_classifier_predictions = ClassifierPrediction(pred_y, proba_y)
                test_classifier_predictions_lst.append(test_classifier_predictions)
                test_y_true_lst.append(y_test.values.ravel())
                score = self._objective(y_test.values.ravel(), test_classifier_predictions)
                test_scores.append(score)

                # wrap prediction for train
                pred_y = model.predict(X_train)
                proba_y = model.predict_proba(X_train)
                train_classifier_predictions = ClassifierPrediction(pred_y, proba_y)
                train_classifier_predictions_lst.append(train_classifier_predictions)
                train_y_true_lst.append(y_train.values.ravel())
                score = self._objective(y_train.values.ravel(), train_classifier_predictions)
                train_scores.append(score)

        # set best score
        self._models_best_scores[model.name] = np.mean(test_scores)
        self._models_train_best_scores[model.name] = np.mean(train_scores)

        # set observations
        if len(self._observations) > 0:
            self._generate_model_observations(model.name, train_y_true_lst, train_classifier_predictions_lst,
                                              test_y_true_lst, test_classifier_predictions_lst)
        # set visualizations
        if len(self._visualizations):
            self._generate_model_visualizations(model.name, train_y_true_lst, train_classifier_predictions_lst,
                                                test_y_true_lst, test_classifier_predictions_lst)

    def _generate_model_observations(self, model_name, train_y_true_lst, train_classifier_predictions_lst,
                                     test_y_true_lst, test_classifier_predictions_lst):
        """
        Generate observations of specific model, given list of training and testing groups with their labels
        and predictions.
        :param model_name: name of model to evaluate.
        :param train_y_true_lst: group of training sets.
        :param train_classifier_predictions_lst: group of predictions on the given training sets.
        :param test_y_true_lst: group of test sets.
        :param test_classifier_predictions_lst: group of predictions on the given test sets.
        """

        # generate observations and merge to one dataframe
        test_observations_dataframes = []
        train_observations_dataframes = []
        for observation in self._observations:
            observation_obj = self._observations[observation]

            # add observation to test
            df = observation_obj.observe(test_y_true_lst, test_classifier_predictions_lst, output_class_col='CLASS',
                                         output_observation_col=observation)
            test_observations_dataframes.append(df)

            # add observation to test
            df = observation_obj.observe(train_y_true_lst, train_classifier_predictions_lst, output_class_col='CLASS',
                                         output_observation_col=observation)
            train_observations_dataframes.append(df)

        self._models_test_observations[model_name] = \
            reduce(lambda x, y: pd.merge(x, y, on='CLASS'), test_observations_dataframes)
        self._models_train_observations[model_name] = \
            reduce(lambda x, y: pd.merge(x, y, on='CLASS'), train_observations_dataframes)

    def _generate_model_visualizations(self, model_name, train_y_true_lst, train_classifier_predictions_lst,
                                       test_y_true_lst, test_classifier_predictions_lst):
        """
        Generate visualizations for specific model, given list of training and testing groups with their labels
        and predictions.
        :param model_name: name of model to visualize.
        :param train_y_true_lst: group of training sets.
        :param train_classifier_predictions_lst: group of predictions on the given training sets.
        :param test_y_true_lst: group of test sets.
        :param test_classifier_predictions_lst: group of predictions on the given test sets.
        """
        self._models_train_visualizations[model_name] = {}
        self._models_test_visualizations[model_name] = {}
        for name, visualization in self._visualizations.items():
            # train
            train_visualization = copy.deepcopy(visualization)
            train_visualization.fit(train_y_true_lst, train_classifier_predictions_lst)
            self._models_train_visualizations[model_name][name] = train_visualization

            # test
            test_visualization = copy.deepcopy(visualization)
            test_visualization.fit(test_y_true_lst, test_classifier_predictions_lst)
            self._models_test_visualizations[model_name][name] = test_visualization

    def get_model_observations(self, model_name, observation_type='test'):
        """
        Given model name and training group ('train' or 'test'), and returns the observations of the model
        on the training group.

        :param model_name: the name of the model.
        :type model_name: str

        :param observation_type: type of training group, must be 'train' or 'test'.
        :type observation_type: str ,optional

        :return: the observations of the model on the training group.
        """
        if observation_type == 'test':
            return self._models_test_observations[model_name]
        elif observation_type == 'train':
            return self._models_train_observations[model_name]
        else:
            raise Exception('Unsupported objective_type {}, only train or test supported.'.format(observation_type))

    def get_model_visualizations(self, model_name, observation_type='test'):
        """
        Given model name and training group ('train' or 'test'), and returns the visualizations of the model
        on the training group.

        :param model_name: the name of the model.
        :type model_name: str

        :param observation_type: type of training group, must be 'train' or 'test'.
        :type observation_type: str ,optional

        :return: the visualizations of the model on the training group.
        """
        if observation_type == 'test':
            return self._models_test_visualizations[model_name]
        elif observation_type == 'train':
            return self._models_train_visualizations[model_name]
        else:
            raise Exception('Unsupported observation_type {}, only train or test supported.'.format(observation_type))

    def add_observation(self, name, observation):
        """
        Add observation to the report.

        :param name: the name of the observation to be shown in the report.
        :type name: str

        :param observation: the observation itself.
        :type observation: :class:`automl_infrastructure.experiment.observations.base.Observation`
        """
        if name in self._observations:
            raise Exception('Unable to add observation: observation named {} already exist.'.format(name))
        self._observations[name] = observation

    def add_visualization(self, name, visualization):
        """
        Add visualization to the report.

        :param name: the name of the visualization to be shown in the report.
        :type name: str

        :param visualization: the visualization itself.
        :type visualization: :class:`automl_infrastructure.visualization.base.Visualization`
        """
        if name in self._visualizations:
            raise Exception('Unable to add visualization: visualization named {} already exist.'.format(name))
        self._visualizations[name] = visualization

    def remove_visualization(self, name):
        """
        Remove visualization from the report, by name.

        :param name: name of visualization to remove.
        :type name: str
        """
        if name not in self._visualizations:
            raise Exception('Unable to remove visualization: visualization named {} does not exist.'.format(name))
        del self._visualizations[name]

    def print_report(self, print_func=print):
        """
        Print a full report of the experiment, including:
            - experiment's name.
            - experiment's start and end time.
            - params used (e.g. number of folds in the cross-validation process).
            - observations and visualizations for every model, sorted by models performances.
        :param print_func: function that prints a dataframe (e.g. 'display' in Jupyter Notebook).
        """
        print("Experiment's name: {}.".format(self._name))
        time_format = '%H:%M:%S - %d/%m/%y'
        print('Start time: {}.'.format(strftime(time_format, self._start_time)))
        print('End time: {}.'.format(strftime(time_format, self._end_time)))
        print('Num of folds: {}.'.format(self._n_folds))
        print('Num of k-folds repetitions: {}.'.format(self._n_repetitions))
        print()
        # sort models by score
        reverse = True if self._objective_direction == 'maximize' else False
        sorted_models_scores = [m[0] for m in
                                sorted(self._models_best_scores.items(), key=operator.itemgetter(1), reverse=reverse)]

        # print models results
        for model_name in sorted_models_scores:
            print('---------------------------------------------------------')
            print('Model name: {}.'.format(model_name))
            print('Score: {}.'.format(self._models_best_scores[model_name]))
            print()
            print('Best hyper-parameters: {}.'.format(self._models_best_params[model_name]))
            print()
            print("Train's observations:")
            print_func(self._models_train_observations[model_name])
            print()
            if len(self._visualizations) > 0:
                print("Train's visualizations:")
                for visualization in self._visualizations:
                    print('{}:'.format(visualization))
                    self._models_train_visualizations[model_name][visualization].show()
                print()
            print("Test's observations:")
            print_func(self._models_test_observations[model_name])
            if len(self._visualizations) > 0:
                print("Test's visualizations:")
                for visualization in self._visualizations:
                    print('{}:'.format(visualization))
                    self._models_test_visualizations[model_name][visualization].show()
                print()

            print()
        print('---------------------------------------------------------')

    def dump(self, path, add_date=True):
        effective_file_name = self._name
        if add_date:
            current_date = strftime('%d%m%y_%H%M%S', gmtime())
            effective_file_name = effective_file_name + '_{0}'.format(current_date)
        file_path = '{0}/{1}.pckl'.format(path, effective_file_name)
        with open(file_path, 'wb') as file:
            dill.dump(self, file)

    @staticmethod
    def load(path):
        with open(path, 'rb') as file:
            obj = dill.load(file)
            return obj
        return None
