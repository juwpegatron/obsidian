#!/usr/bin/env python3
"""Validate the built site for GitHub Pages compatibility.

Scans every *.html file in _site/ and checks each href/src that is not external:

  * FAIL if it starts with "/" - an absolute path breaks the /<repo>/ subpath.
  * FAIL if the resolved target file does not exist, using a CASE-SENSITIVE
    comparison against the real _site contents (mirrors Linux, where Pages
    runs).

Standard library only. Run from the vault root: python scripts/check_site.py
Exits 0 on success, 1 on any problem.
"""

from __future__ import annotations

import posixpath
import re
import sys
import urllib.parse
from pathlib import Path

REF_RE = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']')

EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "//",
    "mailto:",
    "tel:",
    "data:",
    "obsidian:",
    "javascript:",
)


def find_html_files(site_dir):
    """All HTML files in the site, sorted for deterministic output."""
    return sorted(site_dir.rglob("*.html"))


def collect_site_paths(site_dir):
    """Return (file_paths, dir_paths) as exact-case posix sets."""
    files = set()
    dirs = {""}
    for path in site_dir.rglob("*"):
        rel = path.relative_to(site_dir).as_posix()
        if path.is_dir():
            dirs.add(rel)
        elif path.is_file():
            files.add(rel)
    return files, dirs


def extract_refs(content):
    """Extract href/src values, ignoring templated ones (${...})."""
    return [ref for ref in REF_RE.findall(content) if "${" not in ref]


def should_skip(ref):
    """True for empty, external, special-scheme and fragment-only refs."""
    if not ref:
        return True
    if ref.startswith(EXTERNAL_PREFIXES):
        return True
    if ref.startswith("#"):
        return True
    return False


def split_target(ref):
    """Strip any query/fragment, returning the file part of a reference."""
    return re.split(r"[#?]", ref, maxsplit=1)[0]


def check_file(file_path, site_dir, file_set, dir_set):
    """Return a list of error strings for one HTML file."""
    errors = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [f"cannot read file: {exc}"]

    rel_html = file_path.relative_to(site_dir).as_posix()
    base_dir = posixpath.dirname(rel_html)

    for ref in extract_refs(content):
        if should_skip(ref):
            continue

        if ref.startswith("/"):
            errors.append(f"{rel_html}: absolute-root ref '{ref}' breaks subpath deployment")
            continue

        target = split_target(ref)
        if not target:
            continue

        decoded = urllib.parse.unquote(target)
        resolved = posixpath.normpath(posixpath.join(base_dir, decoded))

        if resolved == ".." or resolved.startswith("../"):
            errors.append(f"{rel_html}: ref '{ref}' resolves outside the site")
            continue

        is_dir_ref = decoded.endswith("/")
        if is_dir_ref:
            resolved = resolved.rstrip("/") or "."
            exists = resolved in dir_set
        else:
            exists = resolved in file_set

        if exists:
            continue

        # Distinguish a pure case mismatch from a genuinely missing target.
        lowered = resolved.lower()
        case_hit = next(
            (
                actual
                for actual in (file_set | dir_set)
                if actual.lower() == lowered and actual != resolved
            ),
            None,
        )
        if case_hit is not None:
            errors.append(
                f"{rel_html}: ref '{ref}' case mismatch - site has '{case_hit}'"
            )
        else:
            errors.append(f"{rel_html}: ref '{ref}' - target does not exist")

    return errors


def main():
    site_dir = Path.cwd() / "_site"

    if not site_dir.exists():
        print(f"ERROR: Site directory '{site_dir}' does not exist")
        print("Run 'python scripts/build_site.py' first")
        sys.exit(1)

    if not site_dir.is_dir():
        print(f"ERROR: '{site_dir}' is not a directory")
        sys.exit(1)

    file_set, dir_set = collect_site_paths(site_dir)
    html_files = find_html_files(site_dir)

    print(f"Checking site: {site_dir}")
    print(f"Files: {len(file_set)} · HTML pages: {len(html_files)}")
    print()

    all_errors = []
    for html_file in html_files:
        all_errors.extend(check_file(html_file, site_dir, file_set, dir_set))

    print()

    if all_errors:
        print("ERRORS:")
        for error in all_errors:
            print(f"  [FAIL] {error}")
        print()
        print(f"FAILED: {len(all_errors)} problem(s) across {len(html_files)} HTML file(s)")
        sys.exit(1)

    print(f"PASSED: {len(html_files)} HTML file(s) checked, all links resolve")
    print(f"  ({len(file_set)} file(s) in _site, no absolute paths)")
    sys.exit(0)


if __name__ == "__main__":
    main()
