import pytest
from nesta_ds_utils.networks.build import build_coocc
import numpy as np
import scipy
import networkx as nx
import math


def test_network_from_nested_lists():
    """tests that when a list of lists is passed to term_cooccurence_graph it returns the expected edge weights"""
    sequence = [
        [0, 1, 2, 3, 4],
        [0, 5, 6, 7, 3, 4],
    ]
    network = build_coocc(sequence, edge_attributes=["frequency"])
    assert network[3][4]["frequency"] == 2


def test_network_from_nested_arrays():
    """tests that when a list of arrays is passed to term_cooccurence_graph it returns the expected edge weights"""
    sequence = [
        np.array([0, 1, 2, 3, 4]),
        np.array([0, 5, 6, 7, 3, 4]),
    ]
    network = build_coocc(sequence, edge_attributes=["frequency"])
    assert network[3][4]["frequency"] == 2


def test_network_as_adjacency_matrix():
    """tests that when as_adj = True the function returns an adjacency matrix"""
    sequence = [
        [0, 1, 2, 3, 4],
        [0, 5, 6, 7, 3, 4],
    ]
    network, node_list = build_coocc(sequence, as_adj=True)
    assert isinstance(network, scipy.sparse._csr.csr_matrix)


def test_network_node_weight():
    """tests that when use_node_weights = True the network has the correct node weights"""
    sequence = [
        [0, 1, 2, 3, 4],
        [0, 5, 6, 7, 3, 4],
    ]
    network = build_coocc(
        sequence, use_node_weights=True, edge_attributes=["frequency"]
    )
    assert network.nodes[3]["frequency"] == 2


def test_directed_network():
    """tests that when directed = True the number of edges is double when the network is not directed"""
    sequence = [
        [0, 1, 2, 3, 4],
        [0, 5, 6, 7, 3, 4],
    ]
    directed_network = build_coocc(sequence, directed=True)
    undirected_network = build_coocc(sequence)

    assert (
        directed_network.number_of_edges() == 2 * undirected_network.number_of_edges()
    )


def test_jaccard_similarity():
    """tests that when the jaccard similarity is used as an edge attribute it returns the correct value"""
    sequence = [
        [0, 1, 2, 3, 4],
        [0, 5, 6, 7, 3, 4],
    ]
    network = build_coocc(sequence, edge_attributes=["jaccard"])
    attrs = nx.get_edge_attributes(network, "jaccard_similarity")
    if (1, 4) in attrs.keys():
        assert attrs[(1, 4)] == 1 / 2
    else:
        assert attrs[(4, 1)] == 1 / 2


def test_association_strength():
    """tests that when the association strength is used as an edge attribute it returns the correct value"""
    sequence = [
        [0, 1, 2, 3, 4],
        [0, 5, 6, 7, 3, 4],
    ]
    network = build_coocc(sequence, edge_attributes=["association"])
    attrs = nx.get_edge_attributes(network, "association_strength")
    if (1, 4) in attrs.keys():
        assert attrs[(1, 4)] == 1 / 2
    else:
        assert attrs[(4, 1)] == 1 / 2


def test_cosine():
    """tests that when the cosine similarity is used as an edge attribute it returns the correct value"""
    sequence = [
        [0, 1, 2, 3, 4],
        [0, 5, 6, 7, 3, 4],
    ]
    network = build_coocc(sequence, edge_attributes=["cosine"])
    attrs = nx.get_edge_attributes(network, "cosine_similarity")
    if (1, 4) in attrs.keys():
        assert attrs[(1, 4)] == 1 / math.sqrt(2)
    else:
        assert attrs[(4, 1)] == 1 / math.sqrt(2)


def test_inclusion():
    """tests that when the inclusion index is used as an edge attribute it returns the correct value"""
    sequence = [
        [0, 1, 2, 3, 4],
        [0, 5, 6, 7, 3, 4],
    ]
    network = build_coocc(sequence, edge_attributes=["inclusion"])
    attrs = nx.get_edge_attributes(network, "inclusion_index")
    if (1, 4) in attrs.keys():
        assert attrs[(1, 4)] == 1
    else:
        assert attrs[(4, 1)] == 1
