#!/usr/bin/env python3
"""Audit a staged release tree without following links or exposing secrets."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

SCHEMA_VERSION = "1"
DEFAULT_MAX_BYTES = 8_000_000
SKIP_METADATA = {".git", ".hg", ".svn", ".venv", "__pycache__", ".hermes"}
TEXT_SUFFIXES = {
    ".c", ".cc", ".cpp", ".h", ".hpp", ".json", ".md", ".py", ".rs",
    ".sh", ".toml", ".txt", ".yaml", ".yml",
}
PATH_RE = re.compile("/(?:" + "home|tmp|mnt|Users)/|(?:" + "beowulf-workspace|BH_AGENT_)")
INTERNAL_RE = re.compile(
    "(?:" + "session_id|subagent_id|deleg_[0-9a-f]{6,}|\\." + "hermes/)", re.IGNORECASE
)
SECRET_RE = re.compile(
    r"(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|"
    r"xox[baprs]-[A-Za-z0-9-]{12,}|Bearer\s+[A-Za-z0-9._-]{20,}|"
    r"-----BEGIN [A-Z ]+ PRIVATE KEY-----|"
    r"(?:password|passwd|secret)\s*[:=]\s*(?!\[REDACTED\])\S{8,})",
    re.IGNORECASE,
)


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def finding(path: str, line: int, rule: str, severity: str, snippet: str):
    return {
        "file": path,
        "line": line,
        "rule": rule,
        "severity": severity,
        "snippet": snippet,
    }


def masked(kind: str) -> str:
    return f"[{kind} redacted]"


def safe_root(raw: str) -> Path:
    supplied = Path(raw)
    if raw in {".", "..", "/", "~", "$HOME"} or not supplied.is_absolute() and supplied == Path.cwd():
        raise ValueError("staging directory must be an explicit directory, not cwd or root")
    root = supplied.expanduser().resolve(strict=True)
    if not root.is_dir() or root == Path(root.anchor):
        raise ValueError("staging directory must be a non-root directory")
    if root == Path.home():
        raise ValueError("home directory is not an allowed staging directory")
    return root


def inside(root: Path, path: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root)
        return True
    except ValueError:
        return False


def add_path_finding(rows, rel, rule, severity, line=0):
    rows.append(finding(rel, line, rule, severity, masked(rule)))


def scan(root: Path, max_bytes: int, extra_terms: tuple[str, ...], allow_large: set[str]):
    rows = []
    scanned = 0
    warnings = []
    stack = [root]
    while stack:
        directory = stack.pop()
        entries = sorted(os.scandir(directory), key=lambda e: e.name)
        for entry in entries:
            path = Path(entry.path)
            rel = relative(root, path)
            if entry.is_symlink():
                add_path_finding(rows, rel, "symlink", "error")
                continue
            if not inside(root, path):
                add_path_finding(rows, rel, "containment", "error")
                continue
            if entry.is_dir(follow_symlinks=False):
                if entry.name in SKIP_METADATA:
                    add_path_finding(rows, rel, "vcs-or-runtime-metadata", "error")
                else:
                    stack.append(path)
                continue
            if not entry.is_file(follow_symlinks=False):
                continue
            scanned += 1
            try:
                info = entry.stat(follow_symlinks=False)
            except OSError:
                add_path_finding(rows, rel, "stat-error", "error")
                continue
            if not (info.st_mode & (stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)):
                add_path_finding(rows, rel, "unreadable", "error")
                continue
            if info.st_size > max_bytes:
                if rel in allow_large:
                    warnings.append({"file": rel, "rule": "large-file", "suppressed": True})
                else:
                    warnings.append({"file": rel, "rule": "large-file", "bytes": info.st_size})
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES or path.name == "publication_hygiene.py":
                continue
            try:
                raw = path.read_bytes()
            except OSError:
                add_path_finding(rows, rel, "read-error", "error")
                continue
            if b"\x00" in raw[:4096]:
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                warnings.append({"file": rel, "rule": "non-utf8-text"})
                continue
            for number, line in enumerate(text.splitlines(), 1):
                if PATH_RE.search(line):
                    add_path_finding(rows, rel, "path-leak", "error", number)
                if INTERNAL_RE.search(line):
                    add_path_finding(rows, rel, "internal-metadata", "error", number)
                if SECRET_RE.search(line):
                    add_path_finding(rows, rel, "credential", "error", number)
                lower = line.lower()
                for term in extra_terms:
                    if term and term.lower() in lower:
                        add_path_finding(rows, rel, "custom-private-term", "error", number)
    rows.sort(key=lambda row: (row["file"], row["line"], row["rule"]))
    warnings.sort(key=lambda row: (row["file"], row["rule"]))
    return scanned, rows, warnings


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("staging_dir", type=Path)
    parser.add_argument("--json", action="store_true", help="emit deterministic JSON")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--allow-large", action="append", default=[], metavar="RELATIVE_PATH")
    parser.add_argument("--term", action="append", default=[], metavar="TERM")
    parser.add_argument("--out", type=Path, help="write the report outside the staging tree")
    return parser.parse_args(argv)


def main(argv=None):
    try:
        args = parse_args(argv)
        root = safe_root(str(args.staging_dir))
        if args.max_bytes < 1:
            raise ValueError("--max-bytes must be positive")
        if args.out and inside(root, args.out):
            raise ValueError("--out must be outside the staging directory")
        allow_large = {Path(item).as_posix() for item in args.allow_large}
        scanned, rows, warnings = scan(root, args.max_bytes, tuple(args.term), allow_large)
        exit_code = 1 if rows else 0
        result = {
            "schema_version": SCHEMA_VERSION,
            "status": "FAIL" if rows else "PASS",
            "exit_code": exit_code,
            "scanned_files": scanned,
            "findings": rows,
            "warnings": warnings,
        }
        output = json.dumps(result, sort_keys=True, separators=(",", ":")) if args.json else None
        if output is None:
            print(result["status"])
            for row in rows:
                print(f"{row['file']}:{row['line']}: {row['rule']}")
            for row in warnings:
                print(f"warning: {row['file']}: {row['rule']}")
        else:
            print(output)
        if args.out:
            args.out.write_text(output or json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return exit_code
    except (OSError, ValueError) as exc:
        print(f"publication_hygiene: {exc}", file=sys.stderr)
        return 3 if isinstance(exc, OSError) else 2


if __name__ == "__main__":
    raise SystemExit(main())
