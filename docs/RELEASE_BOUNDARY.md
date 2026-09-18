# Release Boundary

## Purpose

This repository is a public-safe, data-free software staging tree. Its permitted content is limited to source code that operates on caller-supplied in-memory records, synthetic tests, standard project configuration, and explanatory documentation. The tree makes no empirical or source-specific claims.

## Excluded material

Do not track raw or derived data; result tables; figures or figure specifications; downloads; archives; external source material or metadata; access logs; notebooks; caches; generated outputs; or tests that read from or write to repository data or output locations. Do not retain numerical outcomes, source-specific descriptions, personal contact information, or external links that function as source provenance.

The `.gitignore` file provides a broad first layer of protection. It does not make an already tracked file safe; tracked content must be reviewed and removed when it violates this boundary.

## Scanner

`tools/check_public_release_boundary.py` deliberately inspects **only paths returned by `git ls-files` and the text of those tracked text files**. It does not enumerate untracked files, read local data directories, download material, or write output. It flags prohibited tracked path categories, common binary/output suffixes, external URLs, personal-email patterns, result-field markers, and tests that reference protected repository locations.

Run it from a Git working tree:

```bash
python tools/check_public_release_boundary.py
```

The scanner is a conservative guardrail, not a substitute for review. Reviewers should confirm that a change remains data-free and does not convey hidden results or provenance.

## Routine validation

```bash
python -m pytest
python tools/check_public_release_boundary.py
python -m compileall -q src tests tools
```

The staging directory supplied for this cleanup may not itself contain Git metadata. In that case the scanner correctly stops rather than expanding its scope beyond tracked files; run it after the intended repository is initialized or placed back in its Git working tree.
