"""Synthetic tests for directed degree-preserving rewiring utilities."""

import networkx as nx
import pytest

from null_models import degree_preserving_null, degree_signature


def synthetic_graph() -> nx.DiGraph:
    """Build a fixed synthetic directed fixture.

    Returns:
        A self-loop-free directed graph with room for degree-preserving swaps.
    """
    return nx.DiGraph(
        [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),
            (1, 3),
            (3, 5),
            (5, 2),
            (2, 4),
            (4, 5),
            (5, 1),
        ]
    )


def test_degree_preserving_null_retains_directed_degree_signature() -> None:
    """Rewire a synthetic graph without changing directed degrees."""
    graph = synthetic_graph()
    null = degree_preserving_null(graph, seed=17, swap_multiplier=2)
    assert set(null.nodes) == set(graph.nodes)
    assert null.number_of_edges() == graph.number_of_edges()
    assert degree_signature(null) == degree_signature(graph)
    assert all(source != target for source, target in null.edges)


def test_degree_preserving_null_is_reproducible_for_one_seed() -> None:
    """Produce identical rewiring for repeated calls that share a seed."""
    first = degree_preserving_null(synthetic_graph(), seed=17, swap_multiplier=2)
    second = degree_preserving_null(synthetic_graph(), seed=17, swap_multiplier=2)
    assert set(first.edges) == set(second.edges)


def test_degree_preserving_null_does_not_consume_the_global_random_stream() -> None:
    """Leave the caller's global random stream untouched by rewiring."""
    import random

    random.seed(1234)
    baseline = [random.random() for _ in range(3)]
    random.seed(1234)
    degree_preserving_null(synthetic_graph(), seed=17, swap_multiplier=2)
    assert [random.random() for _ in range(3)] == baseline


def test_degree_preserving_null_reports_unrewirable_input_as_value_error() -> None:
    """Raise ValueError, not a library exception, when the swap cannot complete.

    A graph with too few nodes or edges, and a graph too rigid to rewire within the
    attempt budget, both reach the underlying swap routine. The documented contract for
    this helper is ValueError, so callers must not have to catch library exceptions.
    """
    too_small = nx.DiGraph([(1, 2), (2, 1)])
    with pytest.raises(ValueError):
        degree_preserving_null(too_small, seed=3, swap_multiplier=2)

    rigid = nx.DiGraph([(0, 1), (1, 0), (1, 2), (1, 3), (2, 0), (2, 1), (3, 1)])
    with pytest.raises(ValueError):
        degree_preserving_null(rigid, seed=0, swap_multiplier=2)


def test_degree_preserving_null_rejects_nonpositive_multiplier() -> None:
    """Reject a multiplier that cannot request a positive number of swaps."""
    with pytest.raises(ValueError):
        degree_preserving_null(synthetic_graph(), seed=1, swap_multiplier=0)
