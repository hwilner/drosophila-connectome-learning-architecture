# Methods Scope

## Retained utilities

The retained source modules are small, in-memory utilities for labelled directed graphs. `primary_graph.py` selects records with caller-chosen labels and collapses repeated directed edges while omitting self-loops. `null_models.py` exposes a directed degree-preserving rewiring helper. `class_constrained_null_models.py` adds preservation of edge counts across caller-supplied source-class and target-class blocks. `motif_counts.py` contains generic helpers that count caller-defined convergence, reciprocal cross-group pairs, and ordered feed-forward triangles.

The utilities accept records or graphs supplied by the caller. They do not locate files, retrieve material, create repository outputs, or encode an empirical input. Default labels are provided solely as a convenience for synthetic architecture examples; callers remain responsible for defining and documenting any use outside the included tests.

## Interpretation limit

These routines support software-level representation and invariance checks only. They do not identify a biological circuit, establish statistical evidence, validate a model, or support functional or causal conclusions. Synthetic tests demonstrate expected code behaviour, not external applicability.

## Engineering constraints

Public functions use Google-style docstrings. Tests are constructed from small, in-memory fixtures. Deterministic seeds are implementation defaults rather than a scientific protocol. Any future use involving empirical materials, methodological choices, or interpretation is outside this public tree and requires an owner decision.
