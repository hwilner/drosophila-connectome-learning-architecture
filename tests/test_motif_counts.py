"""Synthetic checks for in-memory directed motif-counting helpers."""

from motif_counts import (
    count_convergent_targets,
    count_feed_forward_triangles,
    count_reciprocal_cross_group_pairs,
)


class SimpleDiGraph:
    """Provide the minimal directed-graph protocol needed by these checks."""

    def __init__(self, edges: list[tuple[int, int]]) -> None:
        """Initialize a graph from synthetic directed edge pairs.

        Args:
            edges: Directed pairs included in the in-memory fixture.
        """
        self._edges = set(edges)
        self._predecessors: dict[int, set[int]] = {}
        for source, target in edges:
            self._predecessors.setdefault(target, set()).add(source)

    def predecessors(self, node: int) -> set[int]:
        """Return synthetic predecessors for a node.

        Args:
            node: Node identifier to inspect.

        Returns:
            Set of predecessor node identifiers.
        """
        return self._predecessors.get(node, set())

    def has_edge(self, source: int, target: int) -> bool:
        """Return whether a synthetic directed edge is present.

        Args:
            source: Candidate edge source.
            target: Candidate edge target.

        Returns:
            True when the fixture contains the directed edge.
        """
        return (source, target) in self._edges


def test_convergent_target_count_uses_distinct_predecessors() -> None:
    """Count synthetic targets that meet a distinct-predecessor threshold."""
    graph = SimpleDiGraph([(1, 10), (2, 10), (1, 11), (3, 12), (4, 12), (5, 12)])
    assert count_convergent_targets(graph, {1, 2, 3, 4, 5}, {10, 11, 12}) == 2


def test_convergent_target_count_rejects_invalid_threshold() -> None:
    """Reject thresholds that cannot define a positive predecessor requirement."""
    try:
        count_convergent_targets(SimpleDiGraph([]), set(), set(), minimum_sources=0)
    except ValueError as error:
        assert "at least one" in str(error)
    else:
        raise AssertionError("Expected ValueError for a nonpositive threshold")


def test_reciprocal_pair_count_requires_both_directions() -> None:
    """Count each synthetic cross-group reciprocal pair exactly once."""
    graph = SimpleDiGraph([(1, 10), (10, 1), (2, 10), (11, 2), (1, 2), (10, 11)])
    assert count_reciprocal_cross_group_pairs(graph, {1, 2}, {10, 11}) == 1


def test_feed_forward_triangle_count_requires_all_edges() -> None:
    """Count only complete synthetic ordered feed-forward triples."""
    graph = SimpleDiGraph([(1, 10), (10, 100), (1, 100), (10, 1), (100, 10)])
    assert count_feed_forward_triangles(graph, {1}, {10}, {100}) == 1
