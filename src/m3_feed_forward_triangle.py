"""Data-free compatibility helper for counting ordered feed-forward triangles."""

from __future__ import annotations

from typing import AbstractSet

from motif_counts import DirectedGraph, Node, count_feed_forward_triangles


def m3_kc_mbin_mbon_feed_forward_triangle_count(
    graph: DirectedGraph,
    kc_nodes: AbstractSet[Node],
    mbin_nodes: AbstractSet[Node],
    mbon_nodes: AbstractSet[Node],
) -> int:
    """Count ordered feed-forward triangles for three caller-defined node sets.

    The historical function name is retained for compatibility only. The helper does
    not load data, select node labels, write outputs, or make an empirical claim.

    Args:
        graph: Directed graph protocol supplied in memory by the caller.
        kc_nodes: Nodes eligible for the first triangle position.
        mbin_nodes: Nodes eligible for the middle triangle position.
        mbon_nodes: Nodes eligible for the final triangle position.

    Returns:
        Number of ordered triples linked by all three feed-forward edges.
    """
    return count_feed_forward_triangles(graph, kc_nodes, mbin_nodes, mbon_nodes)
