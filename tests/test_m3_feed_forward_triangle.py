"""Synthetic tests for the retained feed-forward compatibility helper."""

from m3_feed_forward_triangle import m3_kc_mbin_mbon_feed_forward_triangle_count


class SimpleDiGraph:
    """Provide the minimal directed-graph protocol needed by this test."""

    def __init__(self, edges: list[tuple[int, int]]) -> None:
        """Initialize a graph from synthetic directed edge pairs.

        Args:
            edges: Directed pairs included in the in-memory fixture.
        """
        self._edges = set(edges)

    def predecessors(self, node: int) -> set[int]:
        """Return predecessors for protocol compatibility.

        Args:
            node: Node identifier to inspect.

        Returns:
            The empty set because this test exercises edge queries only.
        """
        return set()

    def has_edge(self, source: int, target: int) -> bool:
        """Return whether a synthetic directed edge is present.

        Args:
            source: Candidate edge source.
            target: Candidate edge target.

        Returns:
            True when the fixture contains the directed edge.
        """
        return (source, target) in self._edges


def test_feed_forward_helper_counts_complete_ordered_triples() -> None:
    """Count only complete synthetic three-group feed-forward triples."""
    graph = SimpleDiGraph([(1, 10), (10, 100), (1, 100), (10, 1), (100, 10)])
    assert m3_kc_mbin_mbon_feed_forward_triangle_count(graph, {1}, {10}, {100}) == 1


def test_feed_forward_helper_requires_all_directed_edges() -> None:
    """Reject synthetic triples missing any required edge direction."""
    graph = SimpleDiGraph([(1, 10), (10, 100)])
    assert m3_kc_mbin_mbon_feed_forward_triangle_count(graph, {1}, {10}, {100}) == 0
