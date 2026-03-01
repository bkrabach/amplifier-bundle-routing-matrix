"""Validation tests for context/routing-instructions.md.

Verifies the routing instructions file contains the updated content
with all 13 roles, agent author examples, delegation examples,
and a reference to role-definitions.md.
"""

from __future__ import annotations

from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# Walk up from tests/ -> hooks-routing/ -> modules/ -> bundle root -> context/
BUNDLE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INSTRUCTIONS_PATH = BUNDLE_ROOT / "context" / "routing-instructions.md"

# All 13 roles that must appear in the table
ALL_ROLES = [
    "general",
    "fast",
    "coding",
    "ui-coding",
    "security-audit",
    "reasoning",
    "critique",
    "creative",
    "writing",
    "research",
    "vision",
    "image-gen",
    "critical-ops",
]


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def instructions_content() -> str:
    """Load the routing-instructions.md content once for all tests."""
    assert INSTRUCTIONS_PATH.exists(), (
        f"routing-instructions.md not found at {INSTRUCTIONS_PATH}"
    )
    return INSTRUCTIONS_PATH.read_text()


# ---------------------------------------------------------------------------
# Tests: File exists and has title
# ---------------------------------------------------------------------------


class TestFileStructure:
    """Basic file structure checks."""

    def test_file_exists(self) -> None:
        assert INSTRUCTIONS_PATH.exists()

    def test_has_model_routing_title(self, instructions_content: str) -> None:
        assert instructions_content.startswith("# Model Routing")


# ---------------------------------------------------------------------------
# Tests: Available Roles table with all 13 roles
# ---------------------------------------------------------------------------


class TestAvailableRolesTable:
    """The file must have an 'Available Roles (13)' section with a table."""

    def test_has_available_roles_heading(self, instructions_content: str) -> None:
        assert "## Available Roles (13)" in instructions_content

    @pytest.mark.parametrize("role", ALL_ROLES)
    def test_table_contains_role(self, instructions_content: str, role: str) -> None:
        """Each of the 13 roles must appear in the roles table."""
        # Roles appear as `role` in the table
        assert f"| `{role}` |" in instructions_content, (
            f"Role '{role}' not found in Available Roles table"
        )

    def test_table_has_13_role_rows(self, instructions_content: str) -> None:
        """The table should have exactly 13 data rows (excluding header and separator)."""
        # Extract the Available Roles section
        start = instructions_content.index("## Available Roles (13)")
        try:
            next_section = instructions_content.index("\n## ", start + 1)
        except ValueError:
            next_section = len(instructions_content)
        section = instructions_content[start:next_section]

        # Count rows that start with "| `" (role rows)
        role_rows = [line for line in section.split("\n") if line.startswith("| `")]
        assert len(role_rows) == 13, f"Expected 13 role rows, found {len(role_rows)}"


# ---------------------------------------------------------------------------
# Tests: For Agent Authors section
# ---------------------------------------------------------------------------


class TestForAgentAuthors:
    """The file must have a 'For Agent Authors' section with frontmatter examples."""

    def test_has_agent_authors_heading(self, instructions_content: str) -> None:
        assert "## For Agent Authors" in instructions_content

    def test_has_single_role_example(self, instructions_content: str) -> None:
        """Shows a single model_role example."""
        assert "model_role: coding" in instructions_content

    def test_has_fallback_chain_example(self, instructions_content: str) -> None:
        """Shows a fallback chain example."""
        assert "model_role: [ui-coding, coding, general]" in instructions_content

    def test_has_utility_agent_example(self, instructions_content: str) -> None:
        """Shows a fast/utility agent example."""
        assert "model_role: fast" in instructions_content

    def test_has_yaml_code_block(self, instructions_content: str) -> None:
        """The section should contain a yaml code block."""
        start = instructions_content.index("## For Agent Authors")
        try:
            next_section = instructions_content.index("\n## ", start + 1)
        except ValueError:
            next_section = len(instructions_content)
        section = instructions_content[start:next_section]
        assert "```yaml" in section


# ---------------------------------------------------------------------------
# Tests: For Delegating Agents section
# ---------------------------------------------------------------------------


class TestForDelegatingAgents:
    """The file must have a 'For Delegating Agents' section with override example."""

    def test_has_delegating_agents_heading(self, instructions_content: str) -> None:
        assert "## For Delegating Agents" in instructions_content

    def test_has_model_role_override_example(self, instructions_content: str) -> None:
        """Shows model_role override in a delegation JSON example."""
        start = instructions_content.index("## For Delegating Agents")
        section = instructions_content[start:]
        assert '"model_role"' in section or "model_role" in section

    def test_has_json_code_block(self, instructions_content: str) -> None:
        """The section should contain a json code block."""
        start = instructions_content.index("## For Delegating Agents")
        section = instructions_content[start:]
        assert "```json" in section

    def test_has_vision_role_in_example(self, instructions_content: str) -> None:
        """The delegation example should use the 'vision' role (not old 'coding-image')."""
        start = instructions_content.index("## For Delegating Agents")
        section = instructions_content[start:]
        assert '"vision"' in section


# ---------------------------------------------------------------------------
# Tests: References role-definitions context file
# ---------------------------------------------------------------------------


class TestReferencesRoleDefinitions:
    """The file must reference role-definitions for detailed descriptions."""

    def test_references_role_definitions(self, instructions_content: str) -> None:
        assert "role-definitions" in instructions_content

    def test_no_stale_role_references(self, instructions_content: str) -> None:
        """Should not reference old removed roles."""
        # Check that old roles are not in the table
        assert "| `agentic`" not in instructions_content
        assert "| `planning`" not in instructions_content
        assert "| `coding-image`" not in instructions_content
