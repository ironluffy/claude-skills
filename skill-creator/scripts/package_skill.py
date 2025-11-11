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

# Add shared utilities to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from logger import Logger
from constants import (
    SKILL_NAME_PATTERN,
    FILE_REFERENCE_PATTERNS,
    THIRD_PERSON_PATTERNS,
    REQUIRED_FIELDS,
    MIN_DESCRIPTION_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MIN_MARKDOWN_CONTENT_LENGTH,
    MAX_STYLE_WARNINGS,
    ERROR_MESSAGES,
    WARNING_MESSAGES,
    SUCCESS_MESSAGES,
    USAGE_MESSAGES,
    ICONS,
)


class SkillValidator:
    """Validate skill structure and contents."""

    def __init__(self, skill_path: Path, logger: Logger = None):
        self.skill_path = Path(skill_path).resolve()
        self.logger = logger or Logger()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.skill_data: Dict = {}

    def validate(self) -> bool:
        """Run all validation checks."""
        self.logger.info(f"Validating skill: {self.skill_path.name}")
        self.logger.info(f"Location: {self.skill_path}\n")

        # Check if directory exists
        if not self.skill_path.exists():
            self.errors.append(ERROR_MESSAGES["directory_not_found"].format(path=self.skill_path))
            return False

        if not self.skill_path.is_dir():
            self.errors.append(ERROR_MESSAGES["not_a_directory"].format(path=self.skill_path))
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
            self.errors.append(ERROR_MESSAGES["skill_md_not_found"])
        elif not skill_md.is_file():
            self.errors.append(ERROR_MESSAGES["skill_md_not_file"])

    def _validate_yaml_frontmatter(self):
        """Validate YAML frontmatter structure and syntax."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text()

        # Check for frontmatter delimiters
        if not content.startswith('---'):
            self.errors.append(ERROR_MESSAGES["no_frontmatter"])
            return

        # Extract frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            self.errors.append(ERROR_MESSAGES["frontmatter_not_closed"])
            return

        frontmatter = parts[1].strip()

        # Parse YAML
        try:
            self.skill_data = yaml.safe_load(frontmatter)
            if not isinstance(self.skill_data, dict):
                self.errors.append(ERROR_MESSAGES["frontmatter_not_dict"])
                return
        except yaml.YAMLError as e:
            self.errors.append(ERROR_MESSAGES["yaml_syntax_error"].format(error=e))
            return

        self.logger.success(f"{ICONS['success']} {SUCCESS_MESSAGES['yaml_valid']}")

    def _validate_name_field(self):
        """Validate the name field."""
        if 'name' not in self.skill_data:
            self.errors.append(ERROR_MESSAGES["missing_field"].format(field="name"))
            return

        name = self.skill_data['name']

        # Check type
        if not isinstance(name, str):
            self.errors.append(ERROR_MESSAGES["field_not_string"].format(field="name"))
            return

        # Check format
        if not SKILL_NAME_PATTERN.match(name):
            self.errors.append(ERROR_MESSAGES["invalid_name_format"])

        # Check hyphen usage
        if name.startswith('-') or name.endswith('-'):
            self.errors.append(ERROR_MESSAGES["name_hyphen_start_end"])

        if '--' in name:
            self.errors.append(ERROR_MESSAGES["name_consecutive_hyphens"])

        if len(self.errors) == 0 or all('name' not in e for e in self.errors[-3:]):
            self.logger.success(f"{ICONS['success']} {SUCCESS_MESSAGES['name_valid'].format(name=name)}")

    def _validate_description_field(self):
        """Validate the description field."""
        if 'description' not in self.skill_data:
            self.errors.append(ERROR_MESSAGES["missing_field"].format(field="description"))
            return

        description = self.skill_data['description']

        # Check type
        if not isinstance(description, str):
            self.errors.append(ERROR_MESSAGES["field_not_string"].format(field="description"))
            return

        # Check length
        if len(description.strip()) < MIN_DESCRIPTION_LENGTH:
            self.warnings.append(WARNING_MESSAGES["short_description"])

        if len(description.strip()) > MAX_DESCRIPTION_LENGTH:
            self.warnings.append(WARNING_MESSAGES["long_description"])

        self.logger.success(f"{ICONS['success']} {SUCCESS_MESSAGES['description_valid']}")

    def _validate_directory_name_match(self):
        """Verify directory name matches the name field."""
        if 'name' not in self.skill_data:
            return

        name = self.skill_data['name']
        dir_name = self.skill_path.name

        if name != dir_name:
            self.errors.append(
                ERROR_MESSAGES["name_mismatch"].format(dir_name=dir_name, name=name)
            )
        else:
            self.logger.success(f"{ICONS['success']} {SUCCESS_MESSAGES['name_match']}")

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
            self.warnings.append(WARNING_MESSAGES["no_content"])
        elif len(markdown_content) < MIN_MARKDOWN_CONTENT_LENGTH:
            self.warnings.append(WARNING_MESSAGES["minimal_content"])
        else:
            self.logger.success(
                f"{ICONS['success']} {SUCCESS_MESSAGES['content_present'].format(length=len(markdown_content))}"
            )

    def _check_file_references(self):
        """Check that referenced files exist."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text()

        # Find references to local files (relative paths in markdown)
        referenced_files = set()
        for pattern in FILE_REFERENCE_PATTERNS:
            matches = re.findall(pattern, content)
            referenced_files.update(matches)

        missing_files = []
        for ref in referenced_files:
            file_path = self.skill_path / ref
            if not file_path.exists():
                missing_files.append(ref)

        if missing_files:
            for missing in missing_files:
                self.warnings.append(WARNING_MESSAGES["missing_reference"].format(file=missing))
        elif referenced_files:
            self.logger.success(
                f"{ICONS['success']} {SUCCESS_MESSAGES['references_valid'].format(count=len(referenced_files))}"
            )

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

        lines = markdown_content.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern in THIRD_PERSON_PATTERNS:
                if re.search(pattern, line):
                    violations.append(WARNING_MESSAGES["style_violation"].format(line=i))

        if violations:
            # Only show first few violations
            for violation in violations[:MAX_STYLE_WARNINGS]:
                self.warnings.append(violation)
            if len(violations) > MAX_STYLE_WARNINGS:
                self.warnings.append(
                    WARNING_MESSAGES["more_style_warnings"].format(count=len(violations) - MAX_STYLE_WARNINGS)
                )
        else:
            self.logger.success(f"{ICONS['success']} {SUCCESS_MESSAGES['style_good']}")

    def _print_results(self):
        """Print validation results."""
        self.logger.info("\n" + "="*60)

        if self.errors:
            self.logger.error(f"\n{ICONS['error']} VALIDATION FAILED ({len(self.errors)} errors)\n")
            for error in self.errors:
                self.logger.error(f"  {ICONS['cross']} {error}")

        if self.warnings:
            self.logger.warning(f"\n{ICONS['warning']}  WARNINGS ({len(self.warnings)})\n")
            for warning in self.warnings:
                self.logger.warning(f"  {ICONS['info']} {warning}")

        if not self.errors and not self.warnings:
            self.logger.success(f"\n{ICONS['check']} {SUCCESS_MESSAGES['validation_passed']}")
            self.logger.info(f"\n{SUCCESS_MESSAGES['skill_ready']}")
        elif not self.errors:
            self.logger.success(f"\n{ICONS['check']} {SUCCESS_MESSAGES['validation_passed_warnings']}")
            self.logger.info(f"\n{SUCCESS_MESSAGES['skill_functional']}")

        self.logger.info("="*60)


def main():
    """Main entry point."""
    logger = Logger()

    if len(sys.argv) < 2:
        logger.info(USAGE_MESSAGES["package_skill"])
        sys.exit(1)

    skill_path = sys.argv[1]
    validator = SkillValidator(skill_path, logger=logger)

    success = validator.validate()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
