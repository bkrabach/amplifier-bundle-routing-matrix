"""Shared fixtures for routing hook tests."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture()
def tmp_matrix(tmp_path: Path) -> Path:
    """Create a minimal valid matrix YAML file and return its path."""
    content = textwrap.dedent("""\
        name: test-matrix
        description: "Test matrix for unit tests"
        updated: "2026-01-01"

        roles:
          general:
            description: "General purpose"
            candidates:
              - provider: anthropic
                model: claude-sonnet-4-20250514
          fast:
            description: "Fast tasks"
            candidates:
              - provider: openai
                model: gpt-4o-mini
    """)
    matrix_file = tmp_path / "test.yaml"
    matrix_file.write_text(content)
    return matrix_file


@pytest.fixture()
def sample_roles() -> dict[str, Any]:
    """Return a sample roles dict (as returned by load_matrix)."""
    return {
        "general": {
            "description": "General purpose",
            "candidates": [
                {"provider": "anthropic", "model": "claude-sonnet-4-20250514"},
            ],
        },
        "fast": {
            "description": "Fast tasks",
            "candidates": [
                {"provider": "openai", "model": "gpt-4o-mini"},
            ],
        },
        "coding": {
            "description": "Code generation",
            "candidates": [
                {"provider": "anthropic", "model": "claude-sonnet-*"},
                {"provider": "openai", "model": "gpt-4o"},
            ],
        },
    }
