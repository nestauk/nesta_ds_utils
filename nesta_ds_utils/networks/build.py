import numpy as np
import itertools
import warnings
from typing import Union, List
from collections import Counter, defaultdict
from itertools import chain, combinations
import networkx as nx
import scipy
import math


def build_coocc(
    sequences: Union[List[list], List[np.array]],
    graph_type: str = "networkx",
    directed: bool = False,
    as_adj: bool = False,
    use_node_weights: bool = False,
    edge_attributes: List = [],
) -> Union[nx.Graph, scipy.sparse._csr.csr_matrix]:
    """generates a co-occurence graph based on pairwise co-occurence of tokens.

    Args:
        sequences (Union[List[list], List[np.array]]):
            list of lists or list of numpy arrays containing tokens to use as nodes in the network.
        graph_type (str, optional): Python library to use for network generation.
            Currently only supports 'networkx' but future development should support 'graph-tool'
        directed (bool, optional): parameter to indicate if edges should be directed. Defaults to False.
            If True, creates a symmetric graph.
        as_adj (bool, optional): parameter to indicate if network should be returned as an adjacency matrix
            rather than a Graph object.
        use_node_weights (bool, optional): parameter to indicate if node frequency should be added as
            a node attribute.
        edge_attributes (List, optional): parameter to specify any attributes to add to the edges of the network.
            Available options are 'frequency', 'jaccard', 'association', 'cosine', or 'inclusion'.
            Defaults to []. Functions are based on van Eck and Waltman, 2009.

    Returns:
        nx.Graph: Returns networkx graph object. If directed=True returns nx.DiGraph, otherwise returns nx.Graph.
        if as_adj = True returns an adjacency matrix and set of nodes corresponding to rows/columns
    """
    if directed == True:
        network = nx.DiGraph()
    else:
        network = nx.Graph()

    # nodes will be all unique tokens in the corpus
    all_tokens = list(chain(*sequences))
    nodes = set(all_tokens)
    network.add_nodes_from(nodes)

    # if using node weights, weights will represent frequency in the corpus

    if use_node_weights:
        node_weights = Counter(all_tokens)
        nx.set_node_attributes(network, node_weights, "frequency")

    # edge weights are all times a pair of tokens have co-occured in the same sequence
    cooccurrences = _cooccurrence_counts(sequences)

    edges = {x: defaultdict() for x in cooccurrences.keys()}

    # if using similarity metrics as edge attributes, calculate those
    if "frequency" in edge_attributes:
        for node, freq in cooccurrences.items():
            edges[node]["frequency"] = freq
    if "jaccard" in edge_attributes:
        for node, sim in _jaccard_similarity(cooccurrences, all_tokens).items():
            edges[node]["jaccard_similarity"] = sim
    if "association" in edge_attributes:
        for node, sim in _association_strength(cooccurrences, all_tokens).items():
            edges[node]["association_strength"] = sim
    if "cosine" in edge_attributes:
        for node, sim in _cosine_sim(cooccurrences, all_tokens).items():
            edges[node]["cosine_similarity"] = sim
    if "inclusion" in edge_attributes:
        for node, sim in _inclusion_index(cooccurrences, all_tokens).items():
            edges[node]["inclusion_index"] = sim

    # add edges to network
    network.add_edges_from(list((u, v, edges[(u, v)]) for u, v in edges.keys()))

    if directed:
        network.add_edges_from(list((v, u, edges[(u, v)]) for u, v in edges.keys()))

    # if as_adj is true this will return a sparse matrix, otherwise it will return a networkx graph
    if as_adj:
        return nx.adjacency_matrix(network), nodes

    else:
        return network


def _cooccurrence_counts(sequences):
    """counts the pairs of cooccuring tokens in a sequence

    Args:
        sequences (list): list of lists or arrays containing tokens

    Returns:
        dict: key: pair of tokens, value: count of co-occurrence
    """
    combos = (combinations(sorted(set(sequence)), 2) for sequence in sequences)
    return Counter(chain(*combos))


def _node_frequency_counts(all_tokens: List) -> dict:
    """counts frequency of all tokens in corpus

    Args:
        all_tokens (List): list of all tokens in corpus

    Returns:
        dict: key: token, value: frequency
    """
    return Counter(all_tokens)


def _jaccard_similarity(edge_weights: dict, all_tokens: list) -> dict:
    """calculate the jaccard similarity between nodes in the network

    Args:
        edge_weights (dict): co-occurence counts of the nodes in the network
        all_tokens (list): list of all tokens in the corpus

    Returns:
        dict: key: pair of tokens, value: jaccard similarity
    """
    token_frequency = _node_frequency_counts(all_tokens)
    jaccard_sims = defaultdict(int)
    for key, val in edge_weights.items():
        jaccard_sims[key] = val / (
            (token_frequency[key[0]] + token_frequency[key[1]]) - val
        )
    return jaccard_sims


def _association_strength(edge_weights: dict, all_tokens: list) -> dict:
    """calculate the association strength between nodes in the network

    Args:
        edge_weights (dict): co-occurence counts of the nodes in the network
        all_tokens (list): list of all tokens in the corpus

    Returns:
        dict: key: pair of tokens, value: association strength
    """
    token_frequency = _node_frequency_counts(all_tokens)
    association_strengths = defaultdict(int)
    for key, val in edge_weights.items():
        association_strengths[key] = val / (
            token_frequency[key[0]] * token_frequency[key[1]]
        )
    return association_strengths


def _cosine_sim(edge_weights: dict, all_tokens: list) -> dict:
    """calculate the cosine similarity between nodes in the network

    Args:
        edge_weights (dict): co-occurence counts of the nodes in the network
        all_tokens (list): list of all tokens in the corpus

    Returns:
        dict: key: pair of tokens, value: cosine similarity
    """
    token_frequency = _node_frequency_counts(all_tokens)
    cosine_similarities = defaultdict(int)
    for key, val in edge_weights.items():
        cosine_similarities[key] = val / (
            math.sqrt(token_frequency[key[0]] * token_frequency[key[1]])
        )
    return cosine_similarities


def _inclusion_index(edge_weights: dict, all_tokens: list) -> dict:
    """calculate the inclusion index between nodes in the network

    Args:
        edge_weights (dict): co-occurence counts of the nodes in the network
        all_tokens (list): list of all tokens in the corpus

    Returns:
        dict: key: pair of tokens, value: inclusion index
    """
    token_frequency = _node_frequency_counts(all_tokens)
    inclusion_index = defaultdict(int)
    for key, val in edge_weights.items():
        inclusion_index[key] = val / min(
            token_frequency[key[0]], token_frequency[key[1]]
        )
    return inclusion_index
