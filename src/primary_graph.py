"""In-memory utilities for labelled directed graph representations.

The module is data-free: callers supply all records, and no function reads files or
creates repository artifacts.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


DEFAULT_INCLUDED_LABELS = frozenset({"group_a", "group_b", "group_c"})


@dataclass(frozen=True)
class Node:
    """Represent a labelled node supplied by a caller.

    Attributes:
        index: Stable caller-supplied node identifier.
        label: Category used for caller-defined selection.
    """

    index: int
    label: str


@dataclass(frozen=True)
class Edge:
    """Represent a weighted directed edge supplied by a caller.

    Attributes:
        source: Source node identifier.
        target: Target node identifier.
        weight: Nonnegative caller-supplied edge weight.
        kind: Optional caller-supplied edge category.
    """

    source: int
    target: int
    weight: int
    kind: str = ""


@dataclass(frozen=True)
class CollapsedEdge:
    """Represent one aggregate edge in a directed simple graph.

    Attributes:
        source: Source node identifier.
        target: Target node identifier.
        weight: Sum of contributing edge weights.
        raw_row_count: Number of input edges aggregated into this pair.
    """

    source: int
    target: int
    weight: int
    raw_row_count: int


def select_nodes(
    nodes: Iterable[Node], included_labels: frozenset[str] = DEFAULT_INCLUDED_LABELS
) -> list[Node]:
    """Select and sort nodes whose labels appear in an allowed set.

    Args:
        nodes: In-memory node records supplied by the caller.
        included_labels: Exact labels eligible for selection.

    Returns:
        Selected records sorted by ascending node identifier.

    Raises:
        ValueError: If no supplied node has an included label.
    """
    selected = [node for node in nodes if node.label in included_labels]
    if not selected:
        raise ValueError("No nodes matched the supplied included_labels")
    return sorted(selected, key=lambda node: node.index)


def collapse_edges(
    nodes: Iterable[Node], edges: Iterable[Edge], included_labels: frozenset[str] = DEFAULT_INCLUDED_LABELS
) -> list[CollapsedEdge]:
    """Collapse eligible non-self edges into weighted directed simple edges.

    Args:
        nodes: In-memory node records defining eligible identifiers and labels.
        edges: In-memory directed edges, including optional repeated pairs.
        included_labels: Exact node labels that define the retained subgraph.

    Returns:
        Aggregated edges sorted by source and then target identifier.

    Raises:
        ValueError: If no eligible non-self edge is present.
    """
    included_indices = {node.index for node in select_nodes(nodes, included_labels)}
    aggregate_weights: dict[tuple[int, int], int] = defaultdict(int)
    aggregate_rows: dict[tuple[int, int], int] = defaultdict(int)
    for edge in edges:
        if edge.source not in included_indices or edge.target not in included_indices:
            continue
        if edge.source == edge.target:
            continue
        pair = (edge.source, edge.target)
        aggregate_weights[pair] += edge.weight
        aggregate_rows[pair] += 1
    collapsed = [
        CollapsedEdge(source, target, aggregate_weights[(source, target)], aggregate_rows[(source, target)])
        for source, target in aggregate_weights
    ]
    if not collapsed:
        raise ValueError("No eligible non-self edges were supplied")
    return sorted(collapsed, key=lambda edge: (edge.source, edge.target))
