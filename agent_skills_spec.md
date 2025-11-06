# Agent Skills Specification v1.0

**Published**: October 16, 2025
**Status**: Stable

## Overview

Agent skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. This specification defines the format and requirements for creating valid agent skills.

## Skill Structure

### Required Components

Every skill MUST contain a `SKILL.md` file at the root of the skill directory.

### SKILL.md Format

The `SKILL.md` file MUST:
1. Begin with YAML frontmatter enclosed in triple dashes (`---`)
2. Include required metadata fields
3. Contain markdown content with skill instructions

### YAML Frontmatter

**Required Fields:**

- `name` (string): The identifier for the skill
  - MUST contain only lowercase Unicode alphanumeric characters and hyphens
  - MUST match the directory name exactly
  - No spaces, underscores, or special characters allowed
  - Example: `task-decomposer`, `pdf-analyzer`, `mcp-builder`

- `description` (string): Clear explanation of what the skill does and when to use it
  - Should explain the skill's purpose and appropriate use cases
  - Helps Claude determine when to activate the skill

**Optional Fields:**

- `license` (string): License identifier (e.g., `MIT`, `Apache-2.0`)
- `allowed-tools` (array): Pre-approved tools list (Claude Code only)
- `metadata` (object): String key-value pairs for client-specific properties

### Example SKILL.md

```markdown
---
name: example-skill
description: Demonstrate the structure and format of a valid skill following the v1.0 specification
license: Apache-2.0
---

# Example Skill

Provide clear, actionable instructions using imperative/infinitive form.

## Instructions

Use verb-first language:
- "Create a new file" (not "Creates a new file")
- "Analyze the input" (not "Analyzes the input")
- "Generate output" (not "Generates output")

## Organization

Keep SKILL.md lean and high-level. Move detailed documentation to reference files:
- `references/detailed-guide.md` - In-depth explanations
- `scripts/process.py` - Executable code
- `templates/starter.txt` - Template files
```

## Skill Recognition

Claude recognizes a directory as a skill when:
1. The directory contains a `SKILL.md` file
2. The YAML frontmatter is valid and includes required fields
3. The directory name matches the `name` field exactly

## Directory Naming

- Directory names MUST match the `name` field in SKILL.md
- Use lowercase hyphen-case format
- Example: Directory `task-decomposer/` must have `name: task-decomposer`

## Content Organization

While SKILL.md is the only required file, skills can include:

- `scripts/` - Executable code for reliability and efficiency
- `references/` - Detailed documentation loaded as needed
- `templates/` - Starter files and boilerplates
- `examples/` - Demonstration code
- `assets/` - Resources and output files

## Writing Style

**Use imperative/infinitive form** (verb-first):
- ✅ "Create a document"
- ❌ "Creates a document"
- ✅ "Analyze the data"
- ❌ "Analyzes the data"

**Keep instructions specific and actionable:**
- Include concrete examples
- Provide DO/DON'T patterns
- Reference bundled resources when helpful

**Organize for discovery:**
- Structure large documents with grep-friendly patterns
- Use clear section headers
- Keep SKILL.md high-level
- Move details to reference files

## Best Practices

1. **Start simple** - Use minimal structure initially
2. **Be specific** - Clear descriptions help Claude activate skills appropriately
3. **Stay organized** - Separate concerns (SKILL.md vs references)
4. **Use imperative form** - Verb-first instructions
5. **Include examples** - Show DO/DON'T patterns
6. **Bundle resources** - Scripts, templates, references as needed
7. **Test thoroughly** - Validate with real scenarios
8. **Keep lean** - SKILL.md for high-level, references for details
9. **Structure for discovery** - Grep-friendly organization
10. **Iterate** - Refine based on actual usage

## Validation

Skills should be validated for:
- Valid YAML frontmatter syntax
- Required fields present (`name`, `description`)
- Directory name matches `name` field
- No restricted characters in `name` field
- Proper markdown formatting

## Version History

- **v1.0** (October 16, 2025) - Initial stable specification

## References

- Official Repository: https://github.com/anthropics/skills
- Claude Documentation: https://docs.anthropic.com/
