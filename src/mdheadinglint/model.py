from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class HeadingIssue:
    line: int
    message: str

    def __str__(self) -> str:
        return f"Line {self.line}: {self.message}"


def format_issues(issues: List[HeadingIssue]) -> str:
    return "\n".join(str(issue) for issue in issues)
