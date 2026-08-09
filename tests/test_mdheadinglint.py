from __future__ import annotations

from mdheadinglint.linter import lint_headings


def lint(text: str):
    return sorted(str(issue) for issue in lint_headings(text))


def test_no_issues_on_valid_markdown() -> None:
    markdown = "# My Title\n\nSome paragraph.\n\n## Section Details\nMore text."
    assert lint(markdown) == []


def test_missing_space_after_hashes() -> None:
    markdown = "#Title without space\n##Another skip"
    issues = lint(markdown)
    assert len(issues) == 2
    assert "Add a space after the '#' characters in ATX heading" in issues[0]
    assert "Add a space after the '#' characters in ATX heading" in issues[1]


def test_empty_heading_detection() -> None:
    markdown = "# \n##\n"
    issues = lint(markdown)
    assert len(issues) == 2
    for issue in issues:
        assert issue.startswith("Line")


def test_heading_level_jumps() -> None:
    markdown = "# Title\n### Skipped level\n#### Another skip\n"
    issues = lint(markdown)
    assert len(issues) == 3
    assert any("Heading level jumps from h1 to h3" in issue for issue in issues)
    assert any("Capitalize each significant word" in issue for issue in issues)


def test_unsupported_heading_level() -> None:
    markdown = "####### Too deep\n"
    issues = lint(markdown)
    assert any("Heading level must be between 1 and 6" in issue for issue in issues)


def test_valid_setext_heading_is_ignored() -> None:
    markdown = "Title\n=====\n"
    assert lint(markdown) == []


def test_missing_file_path_produces_zero_issues() -> None:
    from mdheadinglint.linter import lint_headings

    assert lint_headings("") == []


def test_markdown_with_no_headings() -> None:
    markdown = "Just plain text.\nNo headings here.\n"
    assert lint(markdown) == []
