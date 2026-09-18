"""Synthetic tests for directed degree-preserving rewiring utilities."""

import networkx as nx

from null_models import degree_preserving_null, degree_signature


def test_degree_preserving_null_retains_directed_degree_signature() -> None:
    """Rewire a synthetic graph without changing directed degrees."""
    graph = nx.DiGraph(
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
    null = degree_preserving_null(graph, seed=17, swap_multiplier=2)
    assert set(null.nodes) == set(graph.nodes)
    assert null.number_of_edges() == graph.number_of_edges()
    assert degree_signature(null) == degree_signature(graph)
    assert all(source != target for source, target in null.edges)
