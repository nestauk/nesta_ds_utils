import numpy as np
import itertools
import warnings
from typing import Union, List
from collections import Counter, defaultdict
from itertools import chain, combinations
import networkx as nx
import scipy as sp


def build_coocc(
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
