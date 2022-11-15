import pytest
from nesta_ds_utils.networks.generate import term_cooccurrence_graph
import numpy as np


def test_network_from_string_list():
    """tests that when a list of strings is passed to term_cooccurence_graph it returns the expected edge weights"""
    sequence = ["I went to the party", "i had fun at the party"]
    network = term_cooccurrence_graph(sequence)
    assert network["the"]["party"]["weight"] == 2


def test_network_from_nested_lists():
    """tests that when a list of lists is passed to term_cooccurence_graph it returns the expected edge weights"""
    sequence = [
        ["I", "went", "to", "the", "party"],
        ["i", "had", "fun", "at", "the", "party"],
    ]
    network = term_cooccurrence_graph(sequence)
    assert network["the"]["party"]["weight"] == 2


def test_network_from_nested_arrays():
    """tests that when a list of arrays is passed to term_cooccurence_graph it returns the expected edge weights"""
    sequence = [
        np.array(["I", "went", "to", "the", "party"]),
        np.array(["i", "had", "fun", "at", "the", "party"]),
    ]
    network = term_cooccurrence_graph(sequence)
    assert network["the"]["party"]["weight"] == 2


def test_network_with_cases():
    """tests that when lowercase=False the tokens are treated differently based on casing"""
    sequence = [
        ["I", "went", "to", "the", "party"],
        ["i", "had", "fun", "at", "the", "party"],
    ]
    network = term_cooccurrence_graph(sequence, lowercase=False)
    node_list = list(network.nodes)
    assert ("I" in node_list) and ("i" in node_list)


def test_network_with_stopwords():
    """tests that when a list of stopwords is passed to the network, the tokens are not in the node list"""
    stop_words = ["I", "had", "at"]
    sequence = [
        ["I", "went", "to", "the", "party"],
        ["i", "had", "fun", "at", "the", "party"],
    ]
    network = term_cooccurrence_graph(sequence, stopwords=stop_words)
    node_list = list(network.nodes)
    assert (
        ("i" not in node_list) and ("had" not in node_list) and ("at" not in node_list)
    )
