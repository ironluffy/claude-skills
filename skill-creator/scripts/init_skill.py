#!/usr/bin/env python3
"""
Skill Initialization Script

Generate boilerplate structure for a new Claude skill following v1.0 specification.

Usage:
    python init_skill.py <skill-name> "<description>"

Example:
    python init_skill.py task-analyzer "Analyze and break down complex tasks"
"""

import os
import sys
from pathlib import Path

# Add shared utilities to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from logger import Logger
from constants import (
    SKILL_DIRECTORIES,
    SKILL_MD_TEMPLATE,
    README_MD_TEMPLATE,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
    USAGE_MESSAGES,
    NEXT_STEPS_TEMPLATE,
    ICONS,
    validate_skill_name_format,
    format_skill_title,
)


def create_skill_structure(skill_name: str, description: str, base_path: Path = None, logger: Logger = None) -> bool:
    """Create complete skill directory structure."""
    logger = logger or Logger()

    # Validate name
    is_valid, error_message = validate_skill_name_format(skill_name)
    if not is_valid:
        logger.error(f"{ICONS['error']} Error: {error_message}")
        return False

    # Determine base path (go up two levels from scripts/)
    if base_path is None:
        script_dir = Path(__file__).parent
        base_path = script_dir.parent.parent

    skill_dir = base_path / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        logger.error(ERROR_MESSAGES["directory_exists"].format(skill_name=skill_name))
        return False

    logger.info(f"Creating skill: {skill_name}")
    logger.info(f"Location: {skill_dir}")

    # Create directory structure
    directories = [skill_dir] + [skill_dir / subdir for subdir in SKILL_DIRECTORIES]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.success(f"  {ICONS['created']} Created {directory.relative_to(base_path)}/")

    # Create SKILL.md from template
    skill_title = format_skill_title(skill_name)
    skill_md_content = SKILL_MD_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title,
        description=description
    )

    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content)
    logger.success(f"  {ICONS['created']} Created SKILL.md")

    # Create README.md from template
    readme_content = README_MD_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title,
        description=description
    )

    readme_path = skill_dir / "README.md"
    readme_path.write_text(readme_content)
    logger.success(f"  {ICONS['created']} Created README.md")

    # Create .gitkeep files for empty directories
    for subdir in SKILL_DIRECTORIES:
        gitkeep_path = skill_dir / subdir / ".gitkeep"
        gitkeep_path.write_text("")

    logger.success(f"\n{ICONS['check']} {SUCCESS_MESSAGES['skill_created'].format(skill_name=skill_name)}")
    logger.info(NEXT_STEPS_TEMPLATE.format(skill_name=skill_name))

    return True


def main():
    """Main entry point."""
    logger = Logger()

    if len(sys.argv) < 3:
        logger.info(USAGE_MESSAGES["init_skill"])
        sys.exit(1)

    skill_name = sys.argv[1]
    description = sys.argv[2]

    success = create_skill_structure(skill_name, description, logger=logger)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
