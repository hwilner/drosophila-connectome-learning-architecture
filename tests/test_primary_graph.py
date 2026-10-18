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
    """Aggregate eligible duplicate pairs without reading or writing files.

    Also covers the error contract: when every supplied edge is either a
    self-loop or touches a node whose label is excluded, no eligible non-self
    edge remains and ``collapse_edges`` must raise ``ValueError``.
    """
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

    # Second in-memory fixture: every edge is a self-loop or touches an
    # excluded-label node, so no eligible non-self edge survives filtering.
    # Eligible nodes are included so the rejection comes from the edge filter
    # in collapse_edges, not from the earlier no-matching-nodes guard.
    excluded_or_self_nodes = [
        make_node(1, "group_a"),
        make_node(2, "group_b"),
        make_node(3, "other"),
    ]
    excluded_or_self_edges = [
        Edge(1, 1, 3, "self"),
        Edge(2, 2, 5, "self"),
        Edge(1, 3, 7, "excluded"),
        Edge(3, 2, 11, "excluded"),
    ]
    try:
        collapse_edges(excluded_or_self_nodes, excluded_or_self_edges)
    except ValueError as error:
        # Pin the specific contract so a different ValueError cannot pass.
        assert "No eligible non-self edges" in str(error)
    else:
        raise AssertionError("Expected ValueError when no eligible non-self edge exists")
