# Contributing

Contributions are welcome. This repository is maintained as an **independent, data-free research software foundation**. Proposed changes should be small, reviewable, and consistent with the scope and boundary documents linked below.

## What belongs here

Suitable contributions improve in-memory graph utilities, synthetic fixtures, deterministic validation, documentation, or release-boundary checks. Public callables should have Google-style docstrings that state their purpose and, where applicable, their arguments, return values, and raised exceptions. Comments should explain non-obvious implementation choices rather than repeat code.

## What must stay out

Do not add data, downloaded material, source-specific metadata, access logs, notebooks, archives, figures, generated outputs, or result-bearing documentation. Do not add numerical findings, outcome claims, or language that attributes biological, functional, or causal meaning to a graph pattern. Do not add personal contact details, affiliations, citations, or licensing material unless an owner explicitly authorizes them.

## Tests and checks

Add or update data-free tests for retained behaviour. Tests must use synthetic, in-memory fixtures and must not read from or write to repository data, result, figure, download, or archive paths. Run the validation commands in [the release boundary](docs/RELEASE_BOUNDARY.md) before requesting review.

## Scope changes

Changes that would introduce data access, empirical analysis, source references, output generation, or external dependencies require an owner decision before implementation. See [status and plan](docs/STATUS_AND_PLAN.md) and [deferred directions](docs/DEFERRED_AND_DROPPED_DIRECTIONS.md).
