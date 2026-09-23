# Contributing

Contributions are welcome. This repository is maintained as an **independent, data-free research software foundation**. Proposed changes should be small, reviewable, and consistent with the scope and boundary documents linked below.

## What belongs here

Suitable contributions improve in-memory graph utilities, synthetic fixtures, deterministic validation, documentation, or release-boundary checks. Public callables should have Google-style docstrings that state their purpose and, where applicable, their arguments, return values, and raised exceptions. Comments should explain non-obvious implementation choices rather than repeat code.

## What must stay out

Do not add data, downloaded material, source-specific metadata, access logs, notebooks, archives, figures, generated outputs, or result-bearing documentation. Do not add numerical findings, outcome claims, or language that attributes biological, functional, or causal meaning to a graph pattern. Do not add personal contact details, affiliations, citations, or licensing material unless an owner explicitly authorizes them.

## Project task workflow

Each atomic task is tracked by a GitHub issue and its matching Project card. When a pull request fully addresses one of those tasks, include `Fixes #<issue-number>`, `Closes #<issue-number>`, or `Resolves #<issue-number>` in the pull-request description. Use a closing keyword only for work that is genuinely complete; use ordinary discussion or a non-closing reference for proposals and partial work. This link gives reviewers a visible relationship between the change and its task, and supports the documented Project-status automation when it is enabled.

## Tests and checks

Add or update data-free tests for retained behaviour. Tests must use synthetic, in-memory fixtures and must not read from or write to repository data, result, figure, download, or archive paths. Run the validation commands in [the release boundary](docs/RELEASE_BOUNDARY.md) before requesting review.

## Future Testing Opportunities

The following contribution ideas preserve the repository's independent, data-free scope. They are opportunities to propose or review work; they do not authorize empirical analysis in this public tree.

### Data-free software or documentation tests contributors can work on now

- **Plain-language status review:** Check whether existing documentation consistently distinguishes completed, non-supportive, and unrun work, and propose concise wording improvements that preserve those distinctions.
- **Synthetic edge-case test plan:** Propose small, in-memory cases that would clarify the documented behavior of the retained graph and motif utilities without introducing empirical records or derived outputs.
- **Reference-family explanation review:** Improve or review reader-facing explanations of why comparison architectures can lead to different interpretations, using only synthetic examples and no outcome claims.
- **Boundary-compliance review:** Check proposed documentation or synthetic-test changes against the release boundary and identify language or paths that could inadvertently imply data access, empirical results, or causal meaning.

### Research-facing tests requiring maintainer approval and an appropriate data boundary

- **Feed-forward-triangle question:** Before any calculation, ask whether the defined triangle diagnostic gives a consistent interpretation across both approved reference families for a maintainer-approved graph.
- **Reciprocal-pair robustness question:** Before any calculation, ask whether a pre-specified representation and comparison procedure yields the same reciprocal-pair direction across the approved reference families.
- **Representation-sensitivity question:** Before any calculation, ask which pre-specified representation or label choices change the interpretation of a structural diagnostic.
- **Cross-reference consistency question:** Before any calculation, ask whether a pre-specified structural finding remains consistent when assessed against each approved reference family.

For every research-facing idea, maintainers must approve the question, data boundary, representation rules, diagnostic definition, comparison procedure, and handling of any materials or outputs before work begins. Empirical materials and derived outputs must remain outside this public repository unless their handling is separately approved.

## Scope changes

Changes that would introduce data access, empirical analysis, source references, output generation, or external dependencies require an owner decision before implementation. See [status and plan](docs/STATUS_AND_PLAN.md) and [deferred directions](docs/DEFERRED_AND_DROPPED_DIRECTIONS.md).
