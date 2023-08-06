from lime.lime_base import LimeBase
from lime.explanation import Explanation, DomainMapper
from functools import partial
from sklearn.utils import check_random_state
import scipy as sp
import sklearn
import numpy as np
import pandas as pd


class GraphDomainMapper(DomainMapper):
    """Maps nodes indices to vertices names"""

    def __init__(self, neighbors_lst):
        """Initializer.
        Args:
            neighbors_lst: list of neighbors as strings.
        """
        super().__init__()

        # sort neighbors in lexicographical order
        self._neighbors_lst = sorted(neighbors_lst)

    def map_exp_ids(self, exp, **kwargs):
        """Maps indices to nodes names.
        Args:
            exp: list of tuples [(idx, weight), (idx,weight)]
        Returns:
            list of tuples (node, weight)
        """

        exp = [(self._neighbors_lst[x[0]], x[1]) for x in exp]
        return exp


class LimeGraphExplainer(object):

    def __init__(self,
                 graph,
                 features_df,
                 node_col,
                 embedding_col,
                 classes,
                 kernel_width=25,
                 kernel=None,
                 feature_selection='auto',
                 random_state=None,
                 verbose=False):

        # initialize base lim
        if kernel is None:
            def kernel(d, kernel_width):
                return np.sqrt(np.exp(-(d ** 2) / kernel_width ** 2))

        kernel_fn = partial(kernel, kernel_width=kernel_width)
        self._random_state = check_random_state(random_state)
        self._base = LimeBase(kernel_fn, verbose,
                              random_state=self._random_state)

        self._graph = graph
        self._features_df = features_df
        self._classes = classes
        self._node_col = node_col
        self._embedding_col = embedding_col
        self._feature_selection = feature_selection
        self._nodes_embedding_dict = dict([(node, embedding) for node, embedding in
                                           zip(features_df[node_col], features_df[embedding_col])])
        self._non_embedding_cols = [c for c in features_df.columns if c not in (node_col, embedding_col)]

    def explain_instance(self,
                         node_name,
                         model,
                         num_features=10,
                         num_samples=50,
                         top_labels=None,
                         labels=None,
                         distance_metric='cosine'):

        data, yss, distances = self._data_labels_distances(
            node_name, model, num_samples,
            distance_metric=distance_metric)

        domain_mapper = GraphDomainMapper([n for n in self._graph.neighbors(node_name)])
        ret_exp = Explanation(domain_mapper=domain_mapper, class_names=self._classes,
                              random_state=self._random_state)
        ret_exp.predict_proba = yss[0]

        if labels is None:
            labels = self._classes
        if top_labels:
            labels = np.argsort(yss[0])[-top_labels:]
            ret_exp.top_labels = list(labels)
            ret_exp.top_labels.reverse()
        for label in labels:
            (ret_exp.intercept[label],
             ret_exp.local_exp[label],
             ret_exp.score, ret_exp.local_pred) = self._base.explain_instance_with_data(
                data, yss, distances, label, num_features,
                model_regressor=None,
                feature_selection=self._feature_selection)
        return ret_exp

    def _calculate_instance_embedding(self, nodes_lst):
        vec = np.mean([self._nodes_embedding_dict[n] for n in nodes_lst], axis=0)
        return vec

    def _data_labels_distances(self,
                               node_name,
                               model,
                               num_samples,
                               distance_metric='cosine'):
        node_neighbors = sorted([n for n in self._graph.neighbors(node_name)])
        neighbors_count = len(node_neighbors)
        node_non_embedding_features = \
            self._features_df[self._features_df[self._node_col] == node_name][self._non_embedding_cols].values.tolist()[0]

        def distance_fn(x):
            return sklearn.metrics.pairwise.pairwise_distances(
                x, x[0], metric=distance_metric).ravel() * 100

        def classifier_fn(instances_data):
            instances_embedding = []
            for i in range(len(instances_data)):
                # extract remaining neighbors
                remaining_neighbors = [node_neighbors[j] for j in range(neighbors_count) if instances_data[i][j] == 1]

                # calculate avg embedding
                instances_embedding.append([self._calculate_instance_embedding(remaining_neighbors)] +
                                           node_non_embedding_features)
            instances_embedding_df = pd.DataFrame(instances_embedding, columns=[self._embedding_col] +
                                           self._non_embedding_cols)

            # predict with rearranged columns order
            ordered_cols = [c for c in self._features_df.columns if c != self._node_col]
            return model.predict_proba(instances_embedding_df[ordered_cols])

        samples = self._random_state.randint(1, neighbors_count + 1, num_samples - 1)
        data = np.ones((num_samples, neighbors_count))
        data[0] = np.ones(neighbors_count)
        features_range = range(neighbors_count)
        for i, size in enumerate(samples, start=1):
            inactive = self._random_state.choice(features_range, size,
                                                 replace=False)
            data[i, inactive] = 0

            # if all chosen to be inactive, pick one neighbor randomly and activate him
            if len(inactive) == neighbors_count:
                random_neighbor_index = self._random_state.choice(neighbors_count)
                data[i, random_neighbor_index] = 1

        labels = classifier_fn(data)
        distances = distance_fn(sp.sparse.csr_matrix(data))
        return data, labels, distances

