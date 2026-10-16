# Mdheadinglint

Lint Markdown heading structure and style: spacing, ordering, casing, and hierarchy.

## About

`mdheadinglint` checks ATX-style Markdown headings and reports common structure issues:
- missing spaces after the `#` prefix
- completely empty headings
- level jumps or skipped levels
- capitalization style violations

It is designed for docs, READMEs, and notes where consistent heading structure improves readability.

## Features

- Spacing checks for ATX headings (`#Heading` vs `# Heading`)
- Empty heading detection
- Heading ordering and level jump analysis
- Capitalization checks for significant words
- Text and JSON output modes
- File and directory stdin paths

## Installation

```bash
pip install .
```

## Usage

```bash
mdheadinglint README.md docs/
mdheadinglint --json README.md
```

### Exit Codes

- `0` — no issues found
- `1` — one or more heading issues found
- `2` — unexpected failure

## Project Structure

```
Week-27/mdheadinglint
├── LICENSE
├── README.md
├── pyproject.toml
├── src/mdheadinglint
│   ├── __init__.py
│   ├── cli.py
│   ├── linter.py
│   └── model.py
└── tests
    └── test_mdheadinglint.py
```

## Tags

markdown, lint, heading, documentation, style, cli

---
[Repository](https://github.com/ethical-dilkhush/mdheadinglint)
