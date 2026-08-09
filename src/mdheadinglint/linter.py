from __future__ import annotations

from typing import List

from mdheadinglint.model import HeadingIssue


def parse_headings(text: str) -> list[dict]:
    headings: list[dict] = []
    lines = text.splitlines()
    for index, line in enumerate(lines, start=1):
        if not line.startswith("#"):
            continue
        stripped = line.lstrip("#")
        if not stripped or stripped[0] != " ":
            continue
        level = len(line) - len(stripped.lstrip("#"))
        content = stripped.lstrip(" ").rstrip()
        if not content:
            continue
        headings.append({"line": index, "level": level, "content": content})
    return headings


def lint_spacing(text: str) -> List[HeadingIssue]:
    issues: List[HeadingIssue] = []
    lines = text.splitlines()
    for index, line in enumerate(lines, start=1):
        if not line.startswith("#"):
            continue
        stripped = line.lstrip("#")
        if not stripped:
            issues.append(
                HeadingIssue(line=index, message="Empty ATX heading has no content")
            )
            continue
        if stripped[0] != " ":
            issues.append(
                HeadingIssue(
                    line=index,
                    message="Add a space after the '#' characters in ATX heading",
                )
            )
            continue
        content = stripped[1:].lstrip(" ")
        if not content:
            issues.append(
                HeadingIssue(line=index, message="Empty ATX heading has no content")
            )
    return issues


_ARTICLE_WORDS = {"a", "an", "the", "and", "or", "but", "for", "nor", "of", "on", "in"}


def lint_heading_casing(text: str) -> List[HeadingIssue]:
    issues: List[HeadingIssue] = []
    headings = parse_headings(text)
    for heading in headings:
        words = heading["content"].split(" ")
        for index, word in enumerate(words):
            if index == 0 or word.lower() not in _ARTICLE_WORDS:
                if word != word.capitalize():
                    issues.append(
                        HeadingIssue(
                            line=heading["line"],
                            message=(
                                "Capitalize each significant word in the heading: "
                                + heading["content"]
                            ),
                        )
                    )
                    break
    return issues


def lint_ordering(text: str) -> List[HeadingIssue]:
    issues: List[HeadingIssue] = []
    headings = parse_headings(text)
    previous_level = 0
    for heading in headings:
        level = int(heading["level"])
        if not 1 <= level <= 6:
            issues.append(
                HeadingIssue(
                    line=heading["line"],
                    message="Heading level must be between 1 and 6",
                )
            )
            previous_level = level
            continue
        if previous_level and abs(level - previous_level) > 1:
            issues.append(
                HeadingIssue(
                    line=heading["line"],
                    message=(
                        "Heading level jumps from h"
                        + str(previous_level)
                        + " to h"
                        + str(level)
                    ),
                )
            )
        previous_level = level
    return issues


def lint_headings(text: str) -> List[HeadingIssue]:
    issues: List[HeadingIssue] = []
    issues.extend(lint_spacing(text))
    issues.extend(lint_ordering(text))
    issues.extend(lint_heading_casing(text))
    return issues
