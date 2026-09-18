"""Data-free helpers for directed degree-preserving graph rewiring."""

from __future__ import annotations

from collections.abc import Iterable

import networkx as nx
from networkx.algorithms.swap import directed_edge_swap

from primary_graph import CollapsedEdge


DEFAULT_NULL_SEED = 0
DEFAULT_SWAP_MULTIPLIER = 10


def graph_from_collapsed_edges(edges: Iterable[CollapsedEdge]) -> nx.DiGraph:
    """Build an unweighted directed topology from aggregate edge records.

    Args:
        edges: Collapsed directed edges supplied in memory.

    Returns:
        A directed graph containing one edge for each input source-target pair.

    Raises:
        ValueError: If no edge is supplied or a self-loop is present.
    """
    graph = nx.DiGraph()
    for edge in edges:
        graph.add_edge(edge.source, edge.target)
    if graph.number_of_edges() == 0:
        raise ValueError("At least one collapsed edge is required")
    if any(source == target for source, target in graph.edges):
        raise ValueError("Input edges must be self-loop free")
    return graph


def degree_signature(graph: nx.DiGraph) -> dict[int, tuple[int, int]]:
    """Return the in-degree and out-degree of every graph node.

    Args:
        graph: Directed graph to describe.

    Returns:
        Mapping from node identifier to its in-degree and out-degree.
    """
    return {node: (graph.in_degree(node), graph.out_degree(node)) for node in graph.nodes}


def degree_preserving_null(
    graph: nx.DiGraph,
    seed: int = DEFAULT_NULL_SEED,
    swap_multiplier: int = DEFAULT_SWAP_MULTIPLIER,
) -> nx.DiGraph:
    """Return a rewired simple directed graph with the same degree signature.

    Args:
        graph: Self-loop-free simple directed graph to rewire in memory.
        seed: Integer seed passed to the rewiring routine.
        swap_multiplier: Requested swaps per input edge; must be positive.

    Returns:
        A rewired copy with the same node set, edge count, and directed degrees.

    Raises:
        ValueError: If the multiplier is invalid or a preservation invariant fails.
    """
    if swap_multiplier <= 0:
        raise ValueError("swap_multiplier must be positive")
    if any(source == target for source, target in graph.edges):
        raise ValueError("Input graph must be self-loop free")
    null = graph.copy()
    original_signature = degree_signature(graph)
    requested_swaps = graph.number_of_edges() * swap_multiplier
    directed_edge_swap(null, nswap=requested_swaps, max_tries=requested_swaps * 50, seed=seed)
    if degree_signature(null) != original_signature:
        raise ValueError("Directed rewiring did not preserve the degree signature")
    if any(source == target for source, target in null.edges):
        raise ValueError("Directed rewiring produced a self-loop")
    return null
