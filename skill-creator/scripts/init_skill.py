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
import re
from pathlib import Path


def validate_skill_name(name: str) -> tuple[bool, str]:
    """Validate skill name follows specification."""
    if not name:
        return False, "Skill name cannot be empty"

    # Check for valid characters (lowercase alphanumeric and hyphens only)
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Skill name must contain only lowercase letters, numbers, and hyphens"

    # Check for valid hyphen usage
    if name.startswith('-') or name.endswith('-'):
        return False, "Skill name cannot start or end with a hyphen"

    if '--' in name:
        return False, "Skill name cannot contain consecutive hyphens"

    return True, "Valid skill name"


def create_skill_structure(skill_name: str, description: str, base_path: Path = None) -> bool:
    """Create complete skill directory structure."""

    # Validate name
    is_valid, message = validate_skill_name(skill_name)
    if not is_valid:
        print(f"❌ Error: {message}")
        return False

    # Determine base path (go up two levels from scripts/)
    if base_path is None:
        script_dir = Path(__file__).parent
        base_path = script_dir.parent.parent

    skill_dir = base_path / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Directory '{skill_name}' already exists")
        return False

    print(f"Creating skill: {skill_name}")
    print(f"Location: {skill_dir}")

    # Create directory structure
    directories = [
        skill_dir,
        skill_dir / "scripts",
        skill_dir / "references",
        skill_dir / "templates",
        skill_dir / "examples",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {directory.relative_to(base_path)}/")

    # Create SKILL.md
    skill_md_content = f"""---
name: {skill_name}
description: {description}
license: Apache-2.0
---

# {skill_name.replace('-', ' ').title()}

{description}

## Instructions

Provide clear, actionable instructions using imperative/infinitive form (verb-first).

### Basic Usage

1. Describe the primary workflow
2. Include specific steps
3. Reference bundled resources

### Examples

✅ **DO**: Show best practices
```
# Example of correct usage
```

❌ **DON'T**: Show what to avoid
```
# Example of incorrect usage
```

## Advanced Features

Document advanced functionality here, or move to `references/` for detailed guides.

## Resources

- Detailed documentation: `references/guide.md`
- Example scripts: `scripts/example.py`
- Templates: `templates/starter.txt`

## Best Practices

- Keep instructions specific and actionable
- Use imperative form (verb-first)
- Include concrete examples
- Reference bundled resources
- Test thoroughly
"""

    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content)
    print(f"  ✓ Created SKILL.md")

    # Create README.md
    readme_content = f"""# {skill_name.replace('-', ' ').title()}

{description}

## Structure

- **SKILL.md** - Main skill instructions and metadata
- **scripts/** - Executable code for automation
- **references/** - Detailed documentation
- **templates/** - Starter files and boilerplates
- **examples/** - Demonstration code

## Development

Edit SKILL.md with your skill's instructions following these guidelines:

1. Use imperative/infinitive form (verb-first)
2. Keep SKILL.md concise and high-level
3. Move detailed docs to references/
4. Include practical examples
5. Test with real scenarios

## Validation

Validate your skill before distribution:

```bash
cd ../skill-creator/scripts
python package_skill.py ../../{skill_name}
```

## License

Apache-2.0
"""

    readme_path = skill_dir / "README.md"
    readme_path.write_text(readme_content)
    print(f"  ✓ Created README.md")

    # Create .gitkeep files for empty directories
    for subdir in ["scripts", "references", "templates", "examples"]:
        gitkeep_path = skill_dir / subdir / ".gitkeep"
        gitkeep_path.write_text("")

    print(f"\n✅ Skill '{skill_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  1. cd {skill_name}")
    print(f"  2. Edit SKILL.md with your instructions")
    print(f"  3. Add scripts, references, and templates as needed")
    print(f"  4. Validate with: python ../skill-creator/scripts/package_skill.py .")
    print(f"  5. Test with real use cases")

    return True


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python init_skill.py <skill-name> \"<description>\"")
        print("\nExample:")
        print('  python init_skill.py task-analyzer "Analyze and break down complex tasks"')
        sys.exit(1)

    skill_name = sys.argv[1]
    description = sys.argv[2]

    success = create_skill_structure(skill_name, description)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
