"""Synthetic tests for class-block-constrained directed rewiring utilities."""

import networkx as nx

from class_constrained_null_models import (
    class_block_signature,
    class_constrained_degree_preserving_null,
)
from null_models import degree_signature


def test_rewiring_preserves_degrees_and_class_block_counts() -> None:
    """Rewire only within synthetic source-class and target-class blocks."""
    graph = nx.DiGraph(
        [
            (1, 3),
            (2, 4),
            (3, 5),
            (4, 6),
            (5, 1),
            (6, 2),
        ]
    )
    classes = {1: "a", 2: "a", 3: "b", 4: "b", 5: "c", 6: "c"}
    null = class_constrained_degree_preserving_null(graph, classes, seed=5, swap_multiplier=1)
    assert degree_signature(null) == degree_signature(graph)
    assert class_block_signature(null, classes) == class_block_signature(graph, classes)
    assert all(source != target for source, target in null.edges)
