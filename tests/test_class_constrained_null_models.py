"""Synthetic tests for class-block-constrained directed rewiring utilities."""

import networkx as nx
import pytest

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


def test_class_constrained_null_is_reproducible_for_one_seed() -> None:
    """Produce identical rewiring for repeated calls that share a seed."""
    graph = nx.DiGraph([(1, 3), (2, 4), (3, 5), (4, 6), (5, 1), (6, 2)])
    classes = {1: "a", 2: "a", 3: "b", 4: "b", 5: "c", 6: "c"}
    first = class_constrained_degree_preserving_null(graph, classes, seed=5, swap_multiplier=1)
    second = class_constrained_degree_preserving_null(graph, classes, seed=5, swap_multiplier=1)
    assert set(first.edges) == set(second.edges)


def test_class_constrained_null_reports_structural_immobility() -> None:
    """Distinguish an input with no admissible swap from a budget shortfall.

    Every block here holds at least two edges, so the block-size eligibility test
    passes, yet no pair can be swapped: one block shares a target, one would produce
    self-loops, and the remaining pair would duplicate an existing edge. The helper
    must say that it made no progress rather than reporting a shortfall count.
    """
    graph = nx.DiGraph([(0, 1), (1, 0), (1, 2), (1, 3), (2, 0), (2, 1), (3, 1)])
    classes = {0: "a", 1: "c", 2: "c", 3: "a"}
    with pytest.raises(ValueError, match="no class block contains a swappable edge pair"):
        class_constrained_degree_preserving_null(graph, classes, seed=0, swap_multiplier=1)


def test_class_constrained_null_rejects_missing_class_assignment() -> None:
    """Reject a graph whose endpoints are not fully covered by class assignments."""
    graph = nx.DiGraph([(1, 3), (2, 4), (3, 5), (4, 6), (5, 1), (6, 2)])
    classes = {1: "a", 2: "a", 3: "b", 4: "b", 5: "c"}
    with pytest.raises(ValueError, match="needs a class assignment"):
        class_constrained_degree_preserving_null(graph, classes, seed=1, swap_multiplier=1)


def test_class_constrained_null_rejects_nonpositive_multiplier() -> None:
    """Reject a multiplier that cannot request a positive number of swaps."""
    graph = nx.DiGraph([(1, 3), (2, 4), (3, 5), (4, 6), (5, 1), (6, 2)])
    classes = {1: "a", 2: "a", 3: "b", 4: "b", 5: "c", 6: "c"}
    with pytest.raises(ValueError, match="must be positive"):
        class_constrained_degree_preserving_null(graph, classes, seed=1, swap_multiplier=0)
