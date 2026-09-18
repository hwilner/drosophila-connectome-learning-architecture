# Status and Plan

## Current status

The public staging scope is limited to data-free graph-architecture utilities, synthetic tests, and documentation that explains their boundaries. It is appropriate for independent research discussion and software review, but it is not a record of empirical work. No dataset, source-specific metadata, result table, figure, or inference is included.

This status note supersedes earlier working-tree documentation and source comments that may have described retrieval activity, dataset-specific transformations, numerical observations, or interpretations. Such material is excluded from the current public tree. Historical version-control records, if available in the originating repository, are retained as history rather than as a current claim.

## Near-term plan

The immediate maintenance priorities are to preserve deterministic in-memory utilities, broaden synthetic edge-case coverage, keep public-callable documentation clear, and run the release-boundary scanner with routine validation. Changes should remain dependency-neutral unless an owner approves a specific need.

## Boundary for future work

Any work involving external material, empirical graph preparation, output generation, visualization, or interpretation is deferred until an owner defines an appropriate non-public workflow and an explicit release decision. It must not be introduced through tests, examples, fixtures, or documentation by implication.

See [methods scope](METHODS_SCOPE.md), [deferred directions](DEFERRED_AND_DROPPED_DIRECTIONS.md), and [release boundary](RELEASE_BOUNDARY.md).
