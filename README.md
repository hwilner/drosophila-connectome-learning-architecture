# Drosophila Connectome Learning Architecture

This independent research repository records a completed structural assessment of a labelled directed *Drosophila* connectome and provides data-free graph utilities for transparent review and extension.

## Research status

| Completed work | Outcome |
|---|---|
| Directed-graph representation and structural audits | A fixed labelled directed representation and two constrained reference families were established for the limited structural comparisons. |
| Convergence diagnostic | Non-discriminative under both predefined reference families; it does not support enrichment or depletion. |
| Reciprocal-pair diagnostic | Its direction changed across the two predefined reference families; it does not support a reference-independent result. |
| Feed-forward triangle diagnostic | Formally defined and tested on synthetic graphs only; no empirical calculation has been run. |

**Current conclusion:** the completed diagnostics are **inconclusive for enrichment, mechanism, or causal interpretation**. They do demonstrate that the choice of constrained reference architecture materially affects the reciprocal-pair statistic.

## What is included

| Path | Contents |
|---|---|
| `src/` | In-memory labelled directed-graph, null-model, and motif utilities. |
| `tests/` | Synthetic tests for graph, rewiring, and motif invariants. |
| `tools/check_public_release_boundary.py` | Tracked-text and tracked-path release-boundary scanner. |
| `docs/` | Research status, methods scope, deferred directions, and contribution guidance. |

## Use and validation

Install the Python requirements in an isolated environment, then run:

```bash
python -m pytest -q
python tools/check_public_release_boundary.py
```

## Keywords

*Drosophila*, connectomics, directed graphs, null models, network science, computational neuroscience, reproducible structural analysis.

## Contributing

Contributions are welcome for data-free graph methods, synthetic tests, documentation, accessibility, and release safeguards. Please read [Contributing](CONTRIBUTING.md) and the [research status](docs/STATUS_AND_PLAN.md) before opening a change.

## Documentation

- [Introduction for new readers](docs/INTRODUCTION.md)
- [Extended introduction from zero background](docs/EXTENDED_INTRODUCTION.md)
- [Methods and contributor decision guide](docs/METHODS.md)
- [Current results and discussion](docs/CURRENT_RESULTS_AND_DISCUSSION.md)
- [Research status and plan](docs/STATUS_AND_PLAN.md)
- [Methods scope](docs/METHODS_SCOPE.md)
- [Release boundary](docs/RELEASE_BOUNDARY.md)
- [Deferred and dropped directions](docs/DEFERRED_AND_DROPPED_DIRECTIONS.md)
