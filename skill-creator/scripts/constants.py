#!/usr/bin/env python3
"""
Shared Constants for Skill Creator

Centralized validation patterns, error messages, templates, and configuration
for skill initialization and validation scripts.
"""

import re
from typing import List, Dict

# ============================================================================
# VALIDATION PATTERNS
# ============================================================================

# Skill name must be lowercase alphanumeric with hyphens only
SKILL_NAME_PATTERN = re.compile(r'^[a-z0-9-]+$')

# File reference patterns for checking SKILL.md references
FILE_REFERENCE_PATTERNS = [
    r'`([a-z-]+/[a-z0-9_.-]+(?:/[a-z0-9_.-]+)*)`',
    r'\(((?:scripts|references|templates|examples|assets)/[^)]+)\)',
]

# Writing style patterns - detect third-person form (should be imperative)
THIRD_PERSON_PATTERNS = [
    r'^\s*-\s+[A-Z][a-z]+s\s+',      # "- Creates", "- Analyzes"
    r'^\s*\d+\.\s+[A-Z][a-z]+s\s+',  # "1. Creates", "2. Analyzes"
]

# ============================================================================
# DIRECTORY STRUCTURE
# ============================================================================

# Standard skill directory structure
SKILL_DIRECTORIES = [
    "scripts",
    "references",
    "templates",
    "examples",
]

# ============================================================================
# VALIDATION RULES
# ============================================================================

# Required frontmatter fields
REQUIRED_FIELDS = ["name", "description"]

# Optional frontmatter fields
OPTIONAL_FIELDS = ["license", "version", "author", "tags"]

# Minimum and maximum description lengths
MIN_DESCRIPTION_LENGTH = 10
MAX_DESCRIPTION_LENGTH = 200

# Minimum markdown content length after frontmatter
MIN_MARKDOWN_CONTENT_LENGTH = 50

# Maximum style warnings to show
MAX_STYLE_WARNINGS = 3

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    # Validation errors
    "empty_name": "Skill name cannot be empty",
    "invalid_name_format": "Skill name must contain only lowercase letters, numbers, and hyphens",
    "name_hyphen_start_end": "Skill name cannot start or end with a hyphen",
    "name_consecutive_hyphens": "Skill name cannot contain consecutive hyphens",
    "directory_exists": "Directory '{skill_name}' already exists",

    # File errors
    "directory_not_found": "Directory does not exist: {path}",
    "not_a_directory": "Path is not a directory: {path}",
    "skill_md_not_found": "SKILL.md file not found (required)",
    "skill_md_not_file": "SKILL.md exists but is not a file",

    # YAML errors
    "no_frontmatter": "SKILL.md must start with YAML frontmatter (---)",
    "frontmatter_not_closed": "YAML frontmatter not properly closed with ---",
    "frontmatter_not_dict": "YAML frontmatter must be a dictionary",
    "yaml_syntax_error": "Invalid YAML syntax: {error}",

    # Field errors
    "missing_field": "Required field '{field}' is missing from frontmatter",
    "field_not_string": "Field '{field}' must be a string",
    "name_mismatch": "Directory name '{dir_name}' does not match name field '{name}'",
}

# ============================================================================
# WARNING MESSAGES
# ============================================================================

WARNING_MESSAGES = {
    "short_description": "Field 'description' is very short - consider adding more detail",
    "long_description": "Field 'description' is quite long - consider being more concise",
    "no_content": "SKILL.md has no content after frontmatter",
    "minimal_content": "SKILL.md content is very minimal",
    "missing_reference": "Referenced file not found: {file}",
    "style_violation": "Line {line}: Consider using imperative form",
    "more_style_warnings": "... and {count} more style warnings",
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_MESSAGES = {
    "yaml_valid": "YAML frontmatter is valid",
    "name_valid": "Name field is valid: '{name}'",
    "description_valid": "Description field is valid",
    "name_match": "Directory name matches name field",
    "content_present": "Markdown content present ({length} characters)",
    "references_valid": "All {count} referenced files exist",
    "style_good": "Writing style looks good (imperative form)",
    "validation_passed": "VALIDATION PASSED",
    "validation_passed_warnings": "VALIDATION PASSED (with warnings)",
    "skill_ready": "Skill is ready for use!",
    "skill_functional": "Skill is functional but consider addressing warnings.",
    "skill_created": "Skill '{skill_name}' created successfully!",
}

# ============================================================================
# ICONS
# ============================================================================

ICONS = {
    "success": "✓",
    "check": "✅",
    "error": "❌",
    "cross": "✗",
    "warning": "⚠️",
    "info": "!",
    "created": "✓",
}

# ============================================================================
# TEMPLATES
# ============================================================================

# SKILL.md template with placeholders: {skill_name}, {description}
SKILL_MD_TEMPLATE = """---
name: {skill_name}
description: {description}
license: Apache-2.0
---

# {skill_title}

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

# README.md template with placeholders: {skill_name}, {description}, {skill_title}
README_MD_TEMPLATE = """# {skill_title}

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

# ============================================================================
# USAGE MESSAGES
# ============================================================================

USAGE_MESSAGES = {
    "init_skill": """Usage: python init_skill.py <skill-name> "<description>"

Example:
  python init_skill.py task-analyzer "Analyze and break down complex tasks\"""",

    "package_skill": """Usage: python package_skill.py <skill-directory>

Example:
  python package_skill.py ../task-decomposer
  python package_skill.py /path/to/my-skill""",
}

# ============================================================================
# NEXT STEPS TEMPLATE
# ============================================================================

NEXT_STEPS_TEMPLATE = """
Next steps:
  1. cd {skill_name}
  2. Edit SKILL.md with your instructions
  3. Add scripts, references, and templates as needed
  4. Validate with: python ../skill-creator/scripts/package_skill.py .
  5. Test with real use cases
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_skill_name_format(name: str) -> tuple[bool, str]:
    """
    Validate skill name follows specification.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, ERROR_MESSAGES["empty_name"]

    if not SKILL_NAME_PATTERN.match(name):
        return False, ERROR_MESSAGES["invalid_name_format"]

    if name.startswith('-') or name.endswith('-'):
        return False, ERROR_MESSAGES["name_hyphen_start_end"]

    if '--' in name:
        return False, ERROR_MESSAGES["name_consecutive_hyphens"]

    return True, ""

def format_skill_title(skill_name: str) -> str:
    """Convert skill-name to Skill Name format."""
    return skill_name.replace('-', ' ').title()
