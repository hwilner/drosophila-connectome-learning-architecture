#!/usr/bin/env python3
"""Check tracked text and paths against this repository's public release boundary."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PATH_PARTS = frozenset(
    {
        "access_logs",
        "archives",
        "artifacts",
        "cache",
        "caches",
        "data",
        "downloads",
        "external",
        "external_docs",
        "figures",
        "notebooks",
        "outputs",
        "reports",
        "results",
        "source_material",
        "source_metadata",
    }
)
FORBIDDEN_SUFFIXES = frozenset(
    {
        ".7z",
        ".bz2",
        ".csv",
        ".feather",
        ".gif",
        ".gz",
        ".h5",
        ".hdf5",
        ".ipynb",
        ".jpeg",
        ".jpg",
        ".json",
        ".jsonl",
        ".npy",
        ".npz",
        ".parquet",
        ".pdf",
        ".pkl",
        ".pickle",
        ".png",
        ".rar",
        ".svg",
        ".tar",
        ".tif",
        ".tiff",
        ".tsv",
        ".xz",
        ".zip",
    }
)
TEXT_MARKERS = {
    "external URL": re.compile(r"https?" + r"://", re.IGNORECASE),
    "personal email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "result field": re.compile(
        r"\b(?:observed" + r"_count|null" + r"_counts|null" + r"_mean|p" + r"_value|effect" + r"_size|result" + r"_table)\b",
        re.IGNORECASE,
    ),
}
PROTECTED_TEST_PATH = re.compile(
    r"(?:[\"']|\b)(?:data|results|figures|outputs|downloads|archives)(?:[\"']|/|\b)"
)
TEXT_SUFFIXES = frozenset({".md", ".py", ".toml", ".txt"})


def tracked_paths(repository_root: Path) -> list[Path]:
    """Return repository-relative paths reported by Git.

    Args:
        repository_root: Directory from which Git should report tracked paths.

    Returns:
        Sorted paths that Git currently tracks.

    Raises:
        RuntimeError: If the directory is not a Git working tree or Git cannot list paths.
    """
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "ls-files", "-z"],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or "Git could not list tracked paths")
    return sorted(Path(item) for item in completed.stdout.decode("utf-8").split("\0") if item)


def find_violations(repository_root: Path, paths: Iterable[Path]) -> list[str]:
    """Find boundary violations in tracked paths and tracked text files only.

    Args:
        repository_root: Root used to resolve the supplied repository-relative paths.
        paths: Paths obtained from Git's tracked-file listing.

    Returns:
        Human-readable violations in the order of the supplied paths.
    """
    violations: list[str] = []
    for relative_path in paths:
        parts = set(relative_path.parts)
        if parts & FORBIDDEN_PATH_PARTS:
            violations.append(f"{relative_path}: prohibited tracked path category")
        if relative_path.suffix.lower() in FORBIDDEN_SUFFIXES:
            violations.append(f"{relative_path}: prohibited tracked file suffix")
        if relative_path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if relative_path == Path("docs/INTRODUCTION.md"):
            continue
        text = (repository_root / relative_path).read_text(encoding="utf-8", errors="replace")
        for description, pattern in TEXT_MARKERS.items():
            if pattern.search(text):
                violations.append(f"{relative_path}: {description} marker")
        if relative_path.parts and relative_path.parts[0] == "tests" and PROTECTED_TEST_PATH.search(text):
            violations.append(f"{relative_path}: test references a protected repository location")
    return violations


def main() -> int:
    """Run the tracked-file boundary check and return a process status.

    Returns:
        Zero when no violations are found; otherwise a nonzero process status.
    """
    try:
        paths = tracked_paths(REPOSITORY_ROOT)
    except RuntimeError as error:
        print(f"Boundary check requires a Git working tree: {error}", file=sys.stderr)
        return 2
    violations = find_violations(REPOSITORY_ROOT, paths)
    if violations:
        print("Public release boundary violations:", file=sys.stderr)
        for violation in violations:
            print(f"- {violation}", file=sys.stderr)
        return 1
    print(f"Public release boundary check passed for {len(paths)} tracked paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
