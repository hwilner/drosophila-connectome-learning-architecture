"""Synthetic tests for in-memory labelled graph representation utilities."""

from primary_graph import Edge, Node, collapse_edges, select_nodes


def make_node(index: int, label: str) -> Node:
    """Create a small synthetic node fixture.

    Args:
        index: Synthetic node identifier.
        label: Synthetic node label.

    Returns:
        An in-memory node record for a test fixture.
    """
    return Node(index=index, label=label)


def test_select_nodes_uses_exact_labels() -> None:
    """Select only records with an exact included label."""
    selected = select_nodes(
        [make_node(2, "group_c"), make_node(1, "group_a"), make_node(3, "other")]
    )
    assert [item.index for item in selected] == [1, 2]


def test_collapse_edges_omits_self_edges_and_aggregates_pairs() -> None:
    """Aggregate eligible duplicate pairs without reading or writing files."""
    nodes = [
        make_node(1, "group_a"),
        make_node(2, "group_b"),
        make_node(3, "group_c"),
        make_node(4, "other"),
    ]
    edges = [
        Edge(1, 2, 3, "first"),
        Edge(1, 2, 5, "second"),
        Edge(2, 2, 7, "self"),
        Edge(2, 3, 11, "first"),
        Edge(3, 4, 13, "excluded"),
    ]
    collapsed = collapse_edges(nodes, edges)
    assert [(edge.source, edge.target, edge.weight, edge.raw_row_count) for edge in collapsed] == [
        (1, 2, 8, 2),
        (2, 3, 11, 1),
    ]
