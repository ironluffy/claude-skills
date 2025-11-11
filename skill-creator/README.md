# Skill Creator

Professional skill scaffolding and validation tools for creating and validating Claude skills against the v1.0 specification with comprehensive YAML frontmatter validation and best practice enforcement.

## Overview

Streamline Claude skill development with automated project generation, template management, and comprehensive validation. Ensures skills follow specification requirements and best practices from the start.

### Key Features

- **Skill Scaffolding** - Generate complete skill structure in seconds
- **Template Management** - Pre-configured SKILL.md and README.md templates
- **YAML Validation** - Comprehensive frontmatter structure and syntax checking
- **Best Practice Enforcement** - Writing style and naming convention validation
- **Professional Output** - Colored console feedback with detailed diagnostics
- **Zero Dependencies** - Uses Python stdlib + shared Logger utility
- **Extensible** - Easy to customize templates and validation rules

## Architecture

### Scripts

| Script | Purpose | Lines |
|--------|---------|-------|
| `init_skill.py` | Skill generation and scaffolding | 119 |
| `package_skill.py` | Validation and verification | 315 |
| `constants.py` | Templates and validation patterns | 320 |

**Total**: 754 lines of Python

### Technology Stack

- **Python 3.8+** - Core language
- **PyYAML** - YAML frontmatter parsing
- **Logger** - Professional colored output (from shared utilities)
- **Regex** - Pattern matching for validation

## Installation

### Prerequisites

```bash
# Python 3.8 or higher
python3 --version

# Install PyYAML for validation
pip install pyyaml

# Or use system package manager
# macOS: brew install pyyaml
# Linux: apt-get install python3-yaml
```

## Usage

### Create a New Skill

```bash
cd scripts

# Basic skill creation
python3 init_skill.py skill-name "Skill description"

# Example: Task analysis skill
python3 init_skill.py task-analyzer "Analyze and break down complex tasks into actionable subtasks"

# Example: Code review skill
python3 init_skill.py code-reviewer "Automated code review with security and performance analysis"
```

**Output**:
```
[*] Creating skill: task-analyzer
[*] Location: /path/to/claude-skills/task-analyzer

[✓]   ✓ Created task-analyzer/
[✓]   ✓ Created task-analyzer/scripts/
[✓]   ✓ Created task-analyzer/references/
[✓]   ✓ Created task-analyzer/templates/
[✓]   ✓ Created task-analyzer/examples/
[✓]   ✓ Created SKILL.md
[✓]   ✓ Created README.md

[✓]
✅ Skill 'task-analyzer' created successfully!
```

### Validate a Skill

```bash
# Validate current directory
python3 package_skill.py .

# Validate specific skill
python3 package_skill.py ../task-analyzer

# Validate with full path
python3 package_skill.py /path/to/my-skill
```

**Validation Output**:
```
[*] Validating skill: task-analyzer
[*] Location: /path/to/task-analyzer

[✓] ✓ YAML frontmatter is valid
[✓] ✓ Name field is valid: 'task-analyzer'
[✓] ✓ Description field is valid
[✓] ✓ Directory name matches name field
[✓] ✓ Markdown content present (835 characters)
[✓] ✓ Writing style looks good (imperative form)

============================================================
[✓]
✅ VALIDATION PASSED

Skill is ready for use!
============================================================
```

## Skill Structure

### Generated Directory Layout

```
my-skill/
├── SKILL.md              # Main skill definition (with YAML frontmatter)
├── README.md             # Development documentation
├── scripts/              # Executable Python/Bash scripts
│   └── .gitkeep
├── references/           # Detailed documentation and guides
│   └── .gitkeep
├── templates/            # Starter files and boilerplates
│   └── .gitkeep
└── examples/             # Example code and usage demonstrations
    └── .gitkeep
```

### SKILL.md Template

Automatically generated with:
- **YAML Frontmatter** - name, description, license
- **Skill Title** - Formatted from skill name
- **Instructions Section** - Best practices placeholder
- **Examples Section** - DO/DON'T code examples
- **Resources Section** - Links to references, scripts, templates
- **Best Practices** - Guidelines for skill usage

### README.md Template

Includes:
- Skill overview and description
- Structure explanation
- Development guidelines
- Validation instructions
- License information

## Validation Rules

### YAML Frontmatter

**Required Fields:**
- `name` - Skill identifier (lowercase, alphanumeric, hyphens only)
- `description` - Brief skill summary (10-200 characters recommended)

**Optional Fields:**
- `license` - Default: Apache-2.0
- `version` - Semantic versioning
- `author` - Creator information
- `tags` - Categorization labels

### Name Validation

**Valid Names:**
- `task-analyzer` ✅
- `code-review-helper` ✅
- `api-docs-generator` ✅

**Invalid Names:**
- `Task-Analyzer` ❌ (uppercase)
- `-task-analyzer` ❌ (leading hyphen)
- `task--analyzer` ❌ (consecutive hyphens)
- `task_analyzer` ❌ (underscores not allowed)
- `task.analyzer` ❌ (dots not allowed)

### Directory Name Matching

Directory name **must match** the `name` field in YAML frontmatter:

```yaml
---
name: task-analyzer  # Must match directory name exactly
---
```

### Writing Style

Validates for **imperative form** (verb-first):

**Good (Imperative)** ✅:
- "Analyze code for security vulnerabilities"
- "Generate API documentation from code"
- "Split tasks into actionable subtasks"

**Avoid (Third-person)** ⚠️:
- "Analyzes code for security vulnerabilities"
- "Generates API documentation from code"
- "Splits tasks into actionable subtasks"

### File References

Validates that referenced files exist:

```markdown
<!-- In SKILL.md -->
- See `scripts/analyze.py` for implementation
- Reference `references/guide.md` for details
- Use `templates/starter.txt` as template
```

Validator checks all files and warns if missing.

## Configuration

### constants.py Customization

#### Modify Templates

```python
# Edit SKILL.md template
SKILL_MD_TEMPLATE = """---
name: {skill_name}
description: {description}
license: Apache-2.0
custom_field: custom_value  # Add custom fields
---

# {skill_title}

Your custom template content...
"""
```

#### Add Validation Rules

```python
# Add custom required fields
REQUIRED_FIELDS = ["name", "description", "author"]

# Add custom patterns
CUSTOM_PATTERN = re.compile(r'your-pattern-here')

# Modify length limits
MIN_DESCRIPTION_LENGTH = 20
MAX_DESCRIPTION_LENGTH = 150
```

#### Customize Messages

```python
# Add custom error messages
ERROR_MESSAGES["custom_error"] = "Your custom error message"

# Add custom success messages
SUCCESS_MESSAGES["custom_check"] = "Custom validation passed"
```

## Advanced Usage

### Batch Skill Creation

```bash
# Create multiple skills from list
for skill in task-analyzer code-reviewer api-docs-gen; do
  python3 init_skill.py "$skill" "Description for $skill"
done
```

### Validation in CI/CD

```bash
#!/bin/bash
# validate-skills.sh

for skill_dir in */; do
  if [ -f "$skill_dir/SKILL.md" ]; then
    echo "Validating $skill_dir..."
    python3 package_skill.py "$skill_dir" || exit 1
  fi
done

echo "All skills validated successfully!"
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate all modified skills
git diff --cached --name-only | grep "SKILL.md" | while read file; do
  skill_dir=$(dirname "$file")
  python3 skill-creator/scripts/package_skill.py "$skill_dir" || exit 1
done
```

## Validation Output Explained

### Success Output

```
[✓] ✓ YAML frontmatter is valid          # YAML parses correctly
[✓] ✓ Name field is valid: 'skill-name'  # Name follows conventions
[✓] ✓ Description field is valid         # Description length OK
[✓] ✓ Directory name matches name field  # Directory == name
[✓] ✓ Markdown content present (N chars) # Has content after frontmatter
[✓] ✓ All N referenced files exist       # File refs validated
[✓] ✓ Writing style looks good           # Imperative form used
```

### Warning Output

```
[!] ⚠️  WARNINGS (3)

[!]   ! Referenced file not found: scripts/example.py
[!]   ! Line 45: Consider using imperative form
[!]   ! Field 'description' is very short - consider adding more detail
```

Warnings indicate **optional improvements** - skill still functional.

### Error Output

```
[!] ❌ VALIDATION FAILED (2 errors)

[!]   ✗ SKILL.md file not found (required)
[!]   ✗ Field 'name' must contain only lowercase letters, numbers, and hyphens
```

Errors indicate **required fixes** - skill won't work until resolved.

## Examples

### Example 1: Data Analysis Skill

```bash
python3 init_skill.py data-analyzer \
  "Analyze datasets and generate statistical insights with visualization"
```

**Generated Structure**:
- SKILL.md with data analysis instructions template
- README.md with development guidelines
- scripts/ for Python analysis scripts
- templates/ for report templates
- examples/ for sample datasets

### Example 2: DevOps Automation

```bash
python3 init_skill.py deploy-automation \
  "Automated deployment pipelines with rollback and monitoring"
```

**Use Cases**:
- CI/CD pipeline templates
- Deployment scripts
- Monitoring configurations
- Rollback procedures

### Example 3: Documentation Generator

```bash
python3 init_skill.py api-docs-gen \
  "Generate API documentation from code with examples and schemas"
```

**Features**:
- OpenAPI/Swagger generation
- Code comment parsing
- Example generation
- Schema validation

## Best Practices

### 1. Descriptive Names

Use clear, descriptive skill names:
- ✅ `security-audit-tool`
- ✅ `performance-analyzer`
- ❌ `tool1`
- ❌ `helper`

### 2. Complete Descriptions

Provide specific, actionable descriptions:
- ✅ "Analyze Python code for security vulnerabilities and generate remediation reports"
- ❌ "Code analyzer"

### 3. Organize Resources

Use directories appropriately:
- `scripts/` - Executable automation
- `references/` - Detailed guides and documentation
- `templates/` - Reusable boilerplates
- `examples/` - Working demonstrations

### 4. Validate Early

Run validation before distributing:
```bash
# After creating skill
python3 package_skill.py ../my-skill

# Fix any errors or warnings
# Re-validate
python3 package_skill.py ../my-skill
```

### 5. Imperative Instructions

Write SKILL.md in imperative form:
- ✅ "Run the analyzer with `python analyze.py`"
- ✅ "Configure settings in config.yaml"
- ❌ "The analyzer runs with `python analyze.py`"
- ❌ "Settings are configured in config.yaml"

## Troubleshooting

### PyYAML Not Found

**Error**: `ModuleNotFoundError: No module named 'yaml'`

**Solution**:
```bash
pip install pyyaml
# Or
pip3 install --break-system-packages pyyaml  # macOS
```

### Directory Already Exists

**Error**: `Directory 'skill-name' already exists`

**Solution**:
```bash
# Rename or remove existing directory
mv skill-name skill-name.old
# Or
rm -rf skill-name

# Then recreate
python3 init_skill.py skill-name "Description"
```

### Validation Fails

**Error**: Multiple validation errors

**Solution**:
1. Read error messages carefully
2. Fix YAML frontmatter syntax
3. Ensure directory name matches `name` field
4. Add missing required fields
5. Fix naming conventions
6. Re-validate

### File Reference Warnings

**Warning**: `Referenced file not found: scripts/example.py`

**Solution**:
```bash
# Either create the referenced file
touch scripts/example.py

# Or remove the reference from SKILL.md
```

## Development

### Project Structure

```
skill-creator/
├── SKILL.md              # Skill definition
├── README.md             # This file
└── scripts/
    ├── init_skill.py         # Skill generation
    ├── package_skill.py      # Validation and packaging
    └── constants.py          # Templates and config
```

### Testing

```bash
# Test skill creation
python3 init_skill.py test-skill "Test description"

# Test validation
python3 package_skill.py ../test-skill

# Clean up
rm -rf ../test-skill
```

### Extending Validation

Add custom validation checks in `package_skill.py`:

```python
class SkillValidator:
    def _check_custom_requirement(self):
        """Add your custom validation logic"""
        if not self.skill_path / "custom-file.txt":
            self.warnings.append("Custom file not found")
```

## Refactoring History

**Date**: 2025-11-11
**Changes**: Refactored to eliminate code duplication and standardize logging

- Replaced 40 print() statements with Logger
- Extracted templates to constants.py (SKILL.md, README.md)
- Centralized validation patterns and messages
- Added helper functions (validate_skill_name_format, format_skill_title)
- Reduced init_skill.py LOC by 42% (205→119 lines)
- Professional colored console output

**See**: `/tmp/qa-refactor/SKILL_CREATOR_REFACTORING_SUMMARY.md`

## License

Apache-2.0

## Support

- **Documentation**: See `SKILL.md` for detailed instructions
- **Examples**: All generated skills include example structure
- **Shared Utilities**: See `../shared/README.md` for Logger documentation
- **Validation Help**: Run with invalid inputs to see detailed error messages

---

**Last Updated**: 2025-11-11
**Version**: 2.0.0 (Post-refactoring)
