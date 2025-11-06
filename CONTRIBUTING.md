# Contributing to Universal Claude Skills

Thank you for your interest in contributing! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Creating a New Skill](#creating-a-new-skill)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards other contributors

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, Claude Code version)
- **Screenshots or logs** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting an enhancement:

- **Use a clear, descriptive title**
- **Provide detailed description** of the proposed feature
- **Explain why this enhancement would be useful**
- **List any potential drawbacks**
- **Provide examples** if possible

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
6. **Push to your fork**
7. **Open a Pull Request**

## Development Setup

### Prerequisites

```bash
# Python 3.8 or higher
python3 --version

# Git
git --version

# Optional: PyYAML for validation
pip install pyyaml
```

### Clone and Setup

```bash
# Clone your fork
git clone https://github.com/ironluffy/claude-skills.git
cd claude-skills

# Create a branch for your changes
git checkout -b feature/my-new-skill

# Install development dependencies (if any)
pip install -r requirements-dev.txt  # If exists
```

## Creating a New Skill

### Using skill-creator

The easiest way to create a new skill is using the `skill-creator`:

```bash
cd skill-creator/scripts
python3 init_skill.py my-new-skill "Description of what it does"
cd ../../my-new-skill
```

### Manual Creation

If creating manually, follow this structure:

```
my-skill/
├── SKILL.md              # Required
├── scripts/              # Optional
│   └── main.py
├── references/           # Optional
│   └── guide.md
├── templates/            # Optional
│   └── template.txt
└── examples/             # Optional
    └── example.py
```

### SKILL.md Requirements

```markdown
---
name: my-skill
description: Clear, specific description of what the skill does and when to use it
license: Apache-2.0
---

# My Skill

High-level instructions using imperative form (verb-first).

## Usage

Provide clear, actionable examples.

## Examples

✅ **DO**: Show best practices
❌ **DON'T**: Show what to avoid
```

### Key Requirements

1. **name** field must:
   - Match directory name exactly
   - Use lowercase-with-hyphens format
   - Contain only letters, numbers, and hyphens

2. **description** must:
   - Clearly explain what the skill does
   - Indicate when to use it
   - Be concise but informative

3. **Instructions** must:
   - Use imperative form (verb-first)
   - Be specific and actionable
   - Include examples
   - Reference bundled resources

## Submitting Changes

### Before Submitting

1. **Validate your skill**
   ```bash
   cd skill-creator/scripts
   python3 package_skill.py ../../my-new-skill
   ```

2. **Test thoroughly**
   - Test with 3-5 real scenarios
   - Verify all file references work
   - Check scripts execute correctly
   - Validate documentation is clear

3. **Update documentation**
   - Add skill to main README.md
   - Update CHANGELOG.md
   - Add usage examples
   - Document any new dependencies

4. **Check code quality**
   - Python scripts follow PEP 8
   - No hardcoded credentials
   - Proper error handling
   - Clear variable names
   - Docstrings for functions

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add pdf-analyzer skill for document processing"
git commit -m "Fix: Handle empty input in task-decomposer"
git commit -m "Docs: Add GitHub integration guide"

# Bad
git commit -m "update stuff"
git commit -m "fix bug"
git commit -m "wip"
```

Format:
```
<type>: <subject>

<optional body>

<optional footer>
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Tests
- `chore:` Maintenance

### Pull Request Process

1. **Update documentation**
   - README.md (if adding new skill)
   - CHANGELOG.md
   - Skill-specific docs

2. **Ensure validation passes**
   ```bash
   python3 skill-creator/scripts/package_skill.py my-new-skill
   ```

3. **Create pull request**
   - Clear title describing the change
   - Detailed description
   - Link to related issues
   - Screenshots/examples if applicable

4. **Wait for review**
   - Address feedback promptly
   - Make requested changes
   - Keep discussion professional

## Style Guidelines

### Writing Style

**Instructions:**
- ✅ Use imperative form: "Create a file"
- ❌ Not third person: "Creates a file"
- ✅ Be specific: "Run `python script.py input.json`"
- ❌ Not vague: "Run the script somehow"

**Examples:**
- Always include DO/DON'T examples
- Show practical, real-world usage
- Explain why, not just what

**Organization:**
- Keep SKILL.md lean and high-level
- Move details to references/
- Use grep-friendly section headers
- Include clear navigation

### Code Style

**Python:**
- Follow PEP 8
- Use type hints where helpful
- Include docstrings
- Handle errors gracefully
- Add logging for debugging

```python
#!/usr/bin/env python3
"""
Brief description of script.

Usage:
    python script.py <arg1> <arg2>
"""

import sys
from typing import List, Dict


def process_data(input_data: Dict) -> List[str]:
    """
    Process input data and return results.

    Args:
        input_data: Dictionary containing input parameters

    Returns:
        List of processed results

    Raises:
        ValueError: If input_data is invalid
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise


if __name__ == "__main__":
    # Entry point
    pass
```

**Bash:**
- Use shellcheck if possible
- Add error handling
- Use meaningful variable names
- Comment complex sections

### Documentation Style

- Use Markdown formatting
- Include code blocks with syntax highlighting
- Add tables for structured data
- Use headings consistently
- Link to related content

## Testing

### Validation Testing

Every skill must pass validation:

```bash
cd skill-creator/scripts
python3 package_skill.py ../../my-skill
```

Expected output:
```
✓ YAML frontmatter is valid
✓ Name field is valid: 'my-skill'
✓ Description field is valid
✓ Directory name matches name field
✓ Markdown content present
✓ Writing style looks good

✅ VALIDATION PASSED
```

### Functional Testing

Test your skill with real scenarios:

1. **Basic usage** - Does it work for common cases?
2. **Edge cases** - Empty input, large files, special characters
3. **Error handling** - Invalid input, missing files, permission errors
4. **Integration** - Works with Linear/GitHub/Jira if applicable
5. **Documentation** - Can users follow your examples?

### Test Checklist

- [ ] Skill passes validation
- [ ] Scripts execute without errors
- [ ] All file references resolve correctly
- [ ] Examples in documentation work
- [ ] Error messages are helpful
- [ ] Edge cases are handled
- [ ] No hardcoded credentials
- [ ] Works on fresh environment

## Documentation

### Required Documentation

For new skills:

1. **SKILL.md** - Main skill instructions
2. **README.md entry** - Add to main README skill catalog
3. **CHANGELOG.md entry** - Document what was added
4. **References** - Detailed guides if needed

### Documentation Standards

- Clear, concise language
- Specific examples
- Step-by-step instructions
- Troubleshooting section
- Links to related resources

### Example Documentation Structure

```markdown
# My Skill

Brief overview paragraph.

## Overview

What the skill does and why it's useful.

## Quick Start

Minimal example to get started.

## Usage

### Basic Usage
Common use cases with examples.

### Advanced Features
More complex scenarios.

## Examples

Real-world examples with DO/DON'T patterns.

## Best Practices

Guidelines for effective use.

## Troubleshooting

Common issues and solutions.

## Resources

Links to additional documentation.
```

## Recognition

Contributors will be:
- Listed in repository contributors
- Mentioned in release notes (for significant contributions)
- Acknowledged in CHANGELOG.md

## Questions?

- **Issues**: [Open a GitHub issue](https://github.com/ironluffy/claude-skills/issues)
- **Discussions**: [Use GitHub Discussions](https://github.com/ironluffy/claude-skills/discussions)
- **Documentation**: Check README.md and skill documentation

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.

---

Thank you for contributing to Universal Claude Skills! 🚀
