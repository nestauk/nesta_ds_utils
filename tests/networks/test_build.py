import pytest
from nesta_ds_utils.networks.build import build_coocc
import numpy as np
import scipy
import networkx as nx


def test_network_from_nested_lists():
    """tests that when a list of lists is passed to term_cooccurence_graph it returns the expected edge weights"""
    sequence = [
        ["I", "went", "to", "the", "party"],
        ["i", "had", "fun", "at", "the", "party"],
    ]
    network = build_coocc(sequence)
    assert network["the"]["party"]["weight"] == 2


def test_network_from_nested_arrays():
    """tests that when a list of arrays is passed to term_cooccurence_graph it returns the expected edge weights"""
    sequence = [
        np.array(["I", "went", "to", "the", "party"]),
        np.array(["i", "had", "fun", "at", "the", "party"]),
    ]
    network = build_coocc(sequence)
    assert network["the"]["party"]["weight"] == 2


def test_network_as_adjacency_matrix():
    """tests that when as_adj = True the function returns an adjacency matrix"""
    sequence = [
        ["I", "went", "to", "the", "party"],
        ["i", "had", "fun", "at", "the", "party"],
    ]
    network, node_list = build_coocc(sequence, as_adj=True)
    assert isinstance(network, scipy.sparse._csr.csr_matrix)


def test_network_node_weight():
    """tests that when use_node_weights = True the network has the correct node weights"""
    sequence = [
        ["I", "went", "to", "the", "party"],
        ["i", "had", "fun", "at", "the", "party"],
    ]
    network = build_coocc(sequence, use_node_weights=True)
    assert network.nodes["the"]["frequency"] == 2


def test_directed_network():
    """tests that when directed = True the number of edges is double when the network is not directed"""
    sequence = [
        ["I", "went", "to", "the", "party"],
        ["i", "had", "fun", "at", "the", "party"],
    ]
    directed_network = build_coocc(sequence, directed=True)
    undirected_network = build_coocc(sequence)

    assert (
        directed_network.number_of_edges() == 2 * undirected_network.number_of_edges()
    )


def test_jaccard_similarity():
    """tests that when the jaccard similarity is used as an edge attribute it returns the correct value"""
    sequence = [
        ["I", "went", "to", "the", "party"],
        ["i", "had", "fun", "at", "the", "party"],
    ]
    network = build_coocc(sequence, edge_attributes=["jaccard_similarity"])
    attrs = nx.get_edge_attributes(network, "jaccard_similarity")
    if ("went", "party") in attrs.keys():
        assert attrs[("went", "party")] == 1 / 2
    else:
        assert attrs[("party", "went")] == 1 / 2
