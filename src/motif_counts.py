"""Data-free motif-counting helpers for caller-supplied directed graph protocols."""

from __future__ import annotations

from typing import AbstractSet, Hashable, Protocol


Node = Hashable


class DirectedGraph(Protocol):
    """Describe the minimal directed-graph operations required by this module."""

    def predecessors(self, node: Node) -> object:
        """Return nodes with edges directed into ``node``."""

    def has_edge(self, source: Node, target: Node) -> bool:
        """Return whether a directed edge connects ``source`` to ``target``."""


def count_convergent_targets(
    graph: DirectedGraph,
    source_nodes: AbstractSet[Node],
    target_nodes: AbstractSet[Node],
    minimum_sources: int = 2,
) -> int:
    """Count targets receiving edges from at least a chosen number of sources.

    Args:
        graph: Directed graph protocol supplied in memory by the caller.
        source_nodes: Nodes eligible to contribute incoming edges.
        target_nodes: Nodes evaluated as possible targets.
        minimum_sources: Minimum number of distinct eligible predecessors required.

    Returns:
        Number of target nodes meeting the distinct-predecessor threshold.

    Raises:
        ValueError: If ``minimum_sources`` is less than one.
    """
    if minimum_sources < 1:
        raise ValueError("minimum_sources must be at least one")
    return sum(
        sum(predecessor in source_nodes for predecessor in graph.predecessors(target))
        >= minimum_sources
        for target in target_nodes
    )


def count_reciprocal_cross_group_pairs(
    graph: DirectedGraph,
    first_group: AbstractSet[Node],
    second_group: AbstractSet[Node],
) -> int:
    """Count cross-group node pairs with an edge in both directions.

    Args:
        graph: Directed graph protocol supplied in memory by the caller.
        first_group: Nodes in the first caller-defined group.
        second_group: Nodes in the second caller-defined group.

    Returns:
        Number of pairs containing both directed cross-group edges.
    """
    return sum(
        graph.has_edge(first_node, second_node) and graph.has_edge(second_node, first_node)
        for first_node in first_group
        for second_node in second_group
    )


def count_feed_forward_triangles(
    graph: DirectedGraph,
    first_group: AbstractSet[Node],
    middle_group: AbstractSet[Node],
    final_group: AbstractSet[Node],
) -> int:
    """Count ordered three-group feed-forward triangles.

    Args:
        graph: Directed graph protocol supplied in memory by the caller.
        first_group: Nodes eligible for the first position.
        middle_group: Nodes eligible for the middle position.
        final_group: Nodes eligible for the final position.

    Returns:
        Number of ordered triples with first-to-middle, middle-to-final, and
        first-to-final edges.
    """
    count = 0
    for first_node in first_group:
        for middle_node in middle_group:
            if not graph.has_edge(first_node, middle_node):
                continue
            for final_node in final_group:
                if graph.has_edge(middle_node, final_node) and graph.has_edge(first_node, final_node):
                    count += 1
    return count
