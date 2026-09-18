# Drosophila Connectome Learning Architecture

This independent research repository contains **data-free, reusable graph-architecture utilities** and synthetic tests for exploring how labelled directed networks can be represented and compared. It does not include connectome data, downloaded source material, empirical outputs, figures, or claims about biological function.

## Current status

This staging tree is prepared as a public-safe foundation. The current documentation and source comments **supersede prior working-tree material** that described data retrieval, dataset-specific processing, numerical observations, or interpretations. Historical version-control records, where present in the source repository, remain historical records and are not endorsed by this current status statement.

## Contents

- `src/primary_graph.py` provides in-memory record types and deterministic labelled-node and edge-collapse utilities.
- `src/null_models.py` provides directed degree-preserving rewiring helpers.
- `src/class_constrained_null_models.py` provides class-block-constrained rewiring helpers.
- `tests/` contains synthetic, data-free unit tests.
- `tools/check_public_release_boundary.py` checks tracked paths and text for the documented public boundary.
- `docs/` describes scope, release boundaries, deferred directions, and contribution expectations.

## Keywords

Drosophila; connectome; network architecture; directed graphs; null models; synthetic testing; reproducible software.

## Contributing

Contributions are welcome, especially improvements to data-free utilities, tests, documentation, reviewability, and release-boundary protections. Please read [the contribution guide](CONTRIBUTING.md) and the [release boundary](docs/RELEASE_BOUNDARY.md) before opening a change.

## Public documentation

- [Status and plan](docs/STATUS_AND_PLAN.md)
- [Methods scope](docs/METHODS_SCOPE.md)
- [Deferred and dropped directions](docs/DEFERRED_AND_DROPPED_DIRECTIONS.md)
- [Release boundary](docs/RELEASE_BOUNDARY.md)

No license is supplied in this staging tree.
