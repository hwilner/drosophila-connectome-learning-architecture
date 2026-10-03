"""Synthetic tests for the public release boundary scanner.

The scanner previously had no test coverage, and its protected-location rule matched
bare prose mentions of the protected directory names. That produced a false positive on
the vocabulary CONTRIBUTING.md requires contributors to use, so these tests pin both the
genuine detections and the prose exclusions.
"""

from pathlib import Path

from check_public_release_boundary import (
    FORBIDDEN_PATH_PARTS,
    FORBIDDEN_SUFFIXES,
    PROTECTED_TEST_PATH,
    find_violations,
)

# Path-like strings are assembled from fragments so that this test file does not itself
# trip the protected-location rule it exercises when the scanner reviews the tests tree.
_DATA = "da" + "ta"
_RESULTS = "res" + "ults"
_OUTPUTS = "out" + "puts"


def test_protected_rule_matches_quoted_and_relative_locations() -> None:
    """Detect a protected directory used as a path segment or quoted literal."""
    detected = [
        f'open("{_DATA}/run.csv")',
        f"Path('{_RESULTS}')",
        f'x = "../{_OUTPUTS}/plot"',
        f'"{_DATA}"',
        f'"a/b/{_DATA}/c"',
    ]
    assert all(PROTECTED_TEST_PATH.search(text) for text in detected)


def test_protected_rule_ignores_repository_scope_vocabulary() -> None:
    """Ignore prose and hyphenated uses of the same words in synthetic test text."""
    ignored = [
        "data-free",
        "Add or update data-free tests for retained behaviour.",
        '"""Synthetic, data-free fixture."""',
        "Tests must use synthetic, in-memory fixtures",
        "metadata",
        "database",
        "the data",
        "DATA_FREE",
    ]
    assert not any(PROTECTED_TEST_PATH.search(text) for text in ignored)


def test_find_violations_flags_prohibited_paths_and_suffixes() -> None:
    """Report a tracked path whose directory or suffix is prohibited.

    Both fixtures use a non-text suffix so the check resolves on the path and suffix
    rules alone, without any file being opened.
    """
    root = Path(__file__).resolve().parents[1]
    violations = find_violations(root, [Path(f"{_DATA}/run.csv"), Path(f"{_RESULTS}/note.pkl")])
    assert any("prohibited tracked path category" in item for item in violations)
    assert any("prohibited tracked file suffix" in item for item in violations)


def test_find_violations_exempts_owner_approved_figure_directory() -> None:
    """Skip the owner-approved generated-illustration directory entirely."""
    root = Path(__file__).resolve().parents[1]
    exempt = Path("docs/figures/01-concept-schematic.png")
    assert exempt.parts[:2] == ("docs", "figures")
    assert find_violations(root, [exempt]) == []


def test_forbidden_sets_cover_the_documented_categories() -> None:
    """Keep the guardrail tables aligned with the documented boundary."""
    assert {"data", "results", "figures", "outputs", "downloads", "archives"} <= FORBIDDEN_PATH_PARTS
    assert {".csv", ".json", ".png", ".ipynb", ".pdf"} <= FORBIDDEN_SUFFIXES
