"""Data-free class-block-constrained directed graph rewiring helpers."""

from __future__ import annotations

import random
from collections import Counter, defaultdict
from collections.abc import Mapping

import networkx as nx

from null_models import degree_signature


DEFAULT_N2_SEED = 0
DEFAULT_N2_SWAP_MULTIPLIER = 10


def class_block_signature(graph: nx.DiGraph, node_classes: Mapping[int, str]) -> dict[tuple[str, str], int]:
    """Count edges in each source-class and target-class block.

    Args:
        graph: Directed graph whose edges are counted.
        node_classes: Class assignment for every graph endpoint.

    Returns:
        Mapping from class-pair tuples to their directed edge counts.

    Raises:
        KeyError: If a graph endpoint has no supplied class assignment.
    """
    return dict(Counter((node_classes[source], node_classes[target]) for source, target in graph.edges))


def class_constrained_degree_preserving_null(
    graph: nx.DiGraph,
    node_classes: Mapping[int, str],
    seed: int = DEFAULT_N2_SEED,
    swap_multiplier: int = DEFAULT_N2_SWAP_MULTIPLIER,
) -> nx.DiGraph:
    """Rewire a graph while retaining degrees and class-block edge counts.

    Args:
        graph: Self-loop-free simple directed graph to rewire in memory.
        node_classes: Class assignment for every graph node.
        seed: Integer seed used by the local random-number generator.
        swap_multiplier: Requested successful within-block swaps per edge.

    Returns:
        A rewired graph retaining node degrees and class-block edge counts.

    Raises:
        ValueError: If inputs are incomplete, invalid, or cannot meet invariants.
    """
    if swap_multiplier <= 0:
        raise ValueError("swap_multiplier must be positive")
    if set(graph.nodes) - set(node_classes):
        raise ValueError("Every graph node needs a class assignment")
    if any(source == target for source, target in graph.edges):
        raise ValueError("Input graph must be self-loop free")
    null = graph.copy()
    original_degrees = degree_signature(graph)
    original_blocks = class_block_signature(graph, node_classes)
    blocks: dict[tuple[str, str], list[tuple[int, int]]] = defaultdict(list)
    for source, target in null.edges:
        blocks[(node_classes[source], node_classes[target])].append((source, target))
    eligible_blocks = [edges for edges in blocks.values() if len(edges) >= 2]
    if not eligible_blocks:
        raise ValueError("No class block contains at least two edges for rewiring")
    rng = random.Random(seed)
    requested = graph.number_of_edges() * swap_multiplier
    successful = 0
    attempts = 0
    max_attempts = requested * 100
    while successful < requested and attempts < max_attempts:
        attempts += 1
        block = rng.choice(eligible_blocks)
        first_index, second_index = rng.sample(range(len(block)), 2)
        source_one, target_one = block[first_index]
        source_two, target_two = block[second_index]
        if source_one == source_two or target_one == target_two:
            continue
        candidate_one = (source_one, target_two)
        candidate_two = (source_two, target_one)
        # Reject pairs that would introduce self-loops or duplicate simple-graph edges.
        if source_one == target_two or source_two == target_one:
            continue
        if candidate_one in null.edges or candidate_two in null.edges:
            continue
        null.remove_edge(source_one, target_one)
        null.remove_edge(source_two, target_two)
        null.add_edge(*candidate_one)
        null.add_edge(*candidate_two)
        block[first_index] = candidate_one
        block[second_index] = candidate_two
        successful += 1
    if successful < requested:
        raise ValueError(f"Rewiring completed {successful} of {requested} requested swaps")
    if degree_signature(null) != original_degrees:
        raise ValueError("Rewiring did not preserve individual directed degrees")
    if class_block_signature(null, node_classes) != original_blocks:
        raise ValueError("Rewiring did not preserve class-block edge counts")
    if any(source == target for source, target in null.edges):
        raise ValueError("Rewiring produced a self-loop")
    return null
