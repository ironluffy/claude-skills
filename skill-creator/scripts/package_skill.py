#!/usr/bin/env python3
"""
Skill Packaging and Validation Script

Validate Claude skills against the v1.0 specification.

Usage:
    python package_skill.py <skill-directory>

Example:
    python package_skill.py ../task-decomposer
    python package_skill.py /path/to/my-skill
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


class SkillValidator:
    """Validate skill structure and contents."""

    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path).resolve()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.skill_data: Dict = {}

    def validate(self) -> bool:
        """Run all validation checks."""
        print(f"Validating skill: {self.skill_path.name}")
        print(f"Location: {self.skill_path}\n")

        # Check if directory exists
        if not self.skill_path.exists():
            self.errors.append(f"Directory does not exist: {self.skill_path}")
            return False

        if not self.skill_path.is_dir():
            self.errors.append(f"Path is not a directory: {self.skill_path}")
            return False

        # Run validation checks
        self._check_skill_md_exists()
        if self.errors:
            return False

        self._validate_yaml_frontmatter()
        self._validate_name_field()
        self._validate_description_field()
        self._validate_directory_name_match()
        self._check_markdown_content()
        self._check_file_references()
        self._check_writing_style()

        # Print results
        self._print_results()

        return len(self.errors) == 0

    def _check_skill_md_exists(self):
        """Verify SKILL.md file exists."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.errors.append("SKILL.md file not found (required)")
        elif not skill_md.is_file():
            self.errors.append("SKILL.md exists but is not a file")

    def _validate_yaml_frontmatter(self):
        """Validate YAML frontmatter structure and syntax."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text()

        # Check for frontmatter delimiters
        if not content.startswith('---'):
            self.errors.append("SKILL.md must start with YAML frontmatter (---)")
            return

        # Extract frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            self.errors.append("YAML frontmatter not properly closed with ---")
            return

        frontmatter = parts[1].strip()

        # Parse YAML
        try:
            self.skill_data = yaml.safe_load(frontmatter)
            if not isinstance(self.skill_data, dict):
                self.errors.append("YAML frontmatter must be a dictionary")
                return
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML syntax: {e}")
            return

        print("✓ YAML frontmatter is valid")

    def _validate_name_field(self):
        """Validate the name field."""
        if 'name' not in self.skill_data:
            self.errors.append("Required field 'name' is missing from frontmatter")
            return

        name = self.skill_data['name']

        # Check type
        if not isinstance(name, str):
            self.errors.append("Field 'name' must be a string")
            return

        # Check format
        if not re.match(r'^[a-z0-9-]+$', name):
            self.errors.append(
                "Field 'name' must contain only lowercase letters, numbers, and hyphens"
            )

        # Check hyphen usage
        if name.startswith('-') or name.endswith('-'):
            self.errors.append("Field 'name' cannot start or end with a hyphen")

        if '--' in name:
            self.errors.append("Field 'name' cannot contain consecutive hyphens")

        if len(self.errors) == 0 or all('name' not in e for e in self.errors[-3:]):
            print(f"✓ Name field is valid: '{name}'")

    def _validate_description_field(self):
        """Validate the description field."""
        if 'description' not in self.skill_data:
            self.errors.append("Required field 'description' is missing from frontmatter")
            return

        description = self.skill_data['description']

        # Check type
        if not isinstance(description, str):
            self.errors.append("Field 'description' must be a string")
            return

        # Check length
        if len(description.strip()) < 10:
            self.warnings.append(
                "Field 'description' is very short - consider adding more detail"
            )

        if len(description.strip()) > 200:
            self.warnings.append(
                "Field 'description' is quite long - consider being more concise"
            )

        print(f"✓ Description field is valid")

    def _validate_directory_name_match(self):
        """Verify directory name matches the name field."""
        if 'name' not in self.skill_data:
            return

        name = self.skill_data['name']
        dir_name = self.skill_path.name

        if name != dir_name:
            self.errors.append(
                f"Directory name '{dir_name}' does not match name field '{name}'"
            )
        else:
            print(f"✓ Directory name matches name field")

    def _check_markdown_content(self):
        """Check for markdown content after frontmatter."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text()
        parts = content.split('---', 2)

        if len(parts) < 3:
            return

        markdown_content = parts[2].strip()

        if not markdown_content:
            self.warnings.append("SKILL.md has no content after frontmatter")
        elif len(markdown_content) < 50:
            self.warnings.append("SKILL.md content is very minimal")
        else:
            print(f"✓ Markdown content present ({len(markdown_content)} characters)")

    def _check_file_references(self):
        """Check that referenced files exist."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text()

        # Find references to local files (relative paths in markdown)
        # Pattern: references/, scripts/, templates/, examples/, etc.
        patterns = [
            r'`([a-z-]+/[a-z0-9_.-]+(?:/[a-z0-9_.-]+)*)`',
            r'\(((?:scripts|references|templates|examples|assets)/[^)]+)\)',
        ]

        referenced_files = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            referenced_files.update(matches)

        missing_files = []
        for ref in referenced_files:
            file_path = self.skill_path / ref
            if not file_path.exists():
                missing_files.append(ref)

        if missing_files:
            for missing in missing_files:
                self.warnings.append(f"Referenced file not found: {missing}")
        elif referenced_files:
            print(f"✓ All {len(referenced_files)} referenced files exist")

    def _check_writing_style(self):
        """Check for imperative/infinitive form (basic heuristics)."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text()
        parts = content.split('---', 2)

        if len(parts) < 3:
            return

        markdown_content = parts[2]

        # Look for common patterns that violate imperative form
        violations = []

        # Pattern: "This skill does..." or "Creates a..."
        third_person_patterns = [
            r'^\s*-\s+[A-Z][a-z]+s\s+',  # "- Creates", "- Analyzes"
            r'^\s*\d+\.\s+[A-Z][a-z]+s\s+',  # "1. Creates", "2. Analyzes"
        ]

        lines = markdown_content.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern in third_person_patterns:
                if re.search(pattern, line):
                    violations.append(f"Line {i}: Consider using imperative form")

        if violations:
            # Only show first few violations
            for violation in violations[:3]:
                self.warnings.append(violation)
            if len(violations) > 3:
                self.warnings.append(f"... and {len(violations) - 3} more style warnings")
        else:
            print("✓ Writing style looks good (imperative form)")

    def _print_results(self):
        """Print validation results."""
        print("\n" + "="*60)

        if self.errors:
            print(f"\n❌ VALIDATION FAILED ({len(self.errors)} errors)\n")
            for error in self.errors:
                print(f"  ✗ {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)})\n")
            for warning in self.warnings:
                print(f"  ! {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ VALIDATION PASSED")
            print("\nSkill is ready for use!")
        elif not self.errors:
            print("\n✅ VALIDATION PASSED (with warnings)")
            print("\nSkill is functional but consider addressing warnings.")

        print("="*60)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill-directory>")
        print("\nExample:")
        print("  python package_skill.py ../task-decomposer")
        print("  python package_skill.py /path/to/my-skill")
        sys.exit(1)

    skill_path = sys.argv[1]
    validator = SkillValidator(skill_path)

    success = validator.validate()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
