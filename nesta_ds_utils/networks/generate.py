import numpy as np
import itertools
import warnings
from typing import Union, List
from collections import Counter, defaultdict
from itertools import chain, combinations
import networkx as nx
import scipy as sp


def build_cooccurrence_graph(
    sequences: Union[List[list], List[np.array]],
    graph_type: str = "networkx",
    weighted: bool = True,
    directed: bool = False,
    as_adj: bool = False,
) -> Union[nx.Graph, sp.sparse]:
    """generates a co-occurence graph based on pairwise co-occurence of terms.

    Args:
        sequences (Union[List[list], List[np.array]]):
            list of lists or list of numpy arrays containing tokens to use as nodes in the network.
        graph_type (str, optional): Python library to use for network generation.
            Currently only supports 'networkx' but future development should support 'graph-tool'
        weighted (bool, optional): parameter to indicate of edges should be weighted. Defaults to True.
            If True, edge weights represent number of co-occurences.
        directed (bool, optional): parameter to indicate if edges should be directed. Defaults to False.
            If True, edge directions are determined based on order of tokens. CURRENTLY NOT SUPPORTED.
        as_adj (bool, optional): parameter to indicate if network should be returned as an adjacency matrix
            rather than a Graph object.

    Returns:
        nx.Graph: Returns networkx graph object. If directed=True returns nx.DiGraph, otherwise returns nx.Graph.
        Currently only supports undirected.
    """
    if directed == True:
        warnings.warn(
            "Directed graphs are not currently supported by this function. Generating undirected Graph."
        )

    network = nx.Graph()

    # nodes will be all unique tokens in the corpus
    nodes = set(itertools.chain(*sequences))
    network.add_nodes_from(nodes)

    # edge weights are all times a pair of tokens have co-occured in the same sequence
    edge_weights = _cooccurrence_counts(sequences)
    for key, val in edge_weights.items():
        if weighted:
            network.add_edge(key[0], key[1], weight=val)
        else:
            network.add_edge(key[0], key[1])

    return network


def _clean_tokens(
    sequences: Union[List[list], List[np.array]], lowercase: bool, stopwords: bool
) -> List[list]:
    """clean tokens based on parameters passed to network generation function

    Args:
        sequences (Union[List[list], List[np.array]]): list of term lists, list of numpy arrays containing terms, or list of strings.
        lowercase (bool): parameter to indicate if tokens should be lowercase.
        stopwords (bool): list of stopwords to tokens to exclude from vertices.

    Returns:
        List[list]: sequences with modified tokens
    """
    # if there are stopwords and lowercase is true remove stopwords and lowercase in one iteration
    if len(stopwords) > 0 and lowercase:
        stopwords = [word.lower() for word in stopwords]
        return [
            [item.lower() for item in sublist if item.lower() not in stopwords]
            for sublist in sequences
        ]

    # if lowercase is false, but there are stopwords only remove stopwords
    elif len(stopwords) > 0 and not lowercase:
        return [
            [item for item in sublist if item not in stopwords] for sublist in sequences
        ]

    # if lowercase is true, but there are no stopwords only lowercase tokens
    elif lowercase and len(stopwords) == 0:
        return [[item.lower() for item in sublist] for sublist in sequences]

    else:
        return sequences


def _cooccurrence_counts(sequences):
    """cooccurrence_counts
    Counts the cooccurring pairs from a nested sequence.
    Parameters
    ----------
    sequences : :obj:`iter` of :obj:`iter`
    Returns
    -------
    :obj:`collections.Counter`

    """
    combos = (combinations(sorted(sequence), 2) for sequence in sequences)
    return Counter(chain(*combos))
