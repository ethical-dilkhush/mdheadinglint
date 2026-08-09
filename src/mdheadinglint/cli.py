from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Sequence

from mdheadinglint.linter import lint_headings


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mdheadinglint",
        description="Lint Markdown heading structure and style.",
    )
    parser.add_argument("paths", nargs="+", help="Markdown files or directories to lint")
    parser.add_argument("--json", action="store_true", help="Output machine-readable issues as JSON")
    return parser.parse_args(list(argv))


def collect_markdown_files(paths: List[str]) -> List[Path]:
    files: List[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.rglob("*.md")):
                files.append(child)
        elif path.exists():
            files.append(path)
        else:
            files.append(path)
    return files


def format_text(relpath: Path, issues: List[str]) -> str:
    if not issues:
        return f"{relpath}: 0 heading issue(s)."
    lines = [f"{relpath}: {len(issues)} heading issue(s)."]
    lines.extend(issues)
    return "\n".join(lines)


def format_json(relpath: Path, issues: List[str]) -> str:
    if not issues:
        return "[]"
    import json

    payload = [
        {"file": str(relpath), "line": issue.split(":", 1)[0].replace("Line ", ""), "message": issue.split(":", 1)[1].strip()}
        for issue in issues
    ]
    try:
        return json.dumps(payload, indent=2)
    except TypeError:
        return "[]"


def run(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    markdown_files = collect_markdown_files(args.paths)
    total_issues = 0
    output_parts: List[str] = []

    for file_path in markdown_files:
        text = ""
        if file_path.exists():
            text = file_path.read_text(encoding="utf-8")
        relpath = file_path
        issues = lint_headings(text)
        rendered = [str(issue) for issue in issues]
        total_issues += len(rendered)
        if args.json:
            output_parts.append(format_json(relpath, rendered))
        else:
            output_parts.append(format_text(relpath, rendered))

    payload = "\n\n".join(output_parts)
    if payload:
        print(payload)
    if total_issues == 0:
        return 0
    return 1


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return run(argv if argv is not None else sys.argv[1:])
    except SystemExit:
        raise
    except BaseException as exc:  # pragma: no cover - safety net
        print(f"mdheadinglint failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
