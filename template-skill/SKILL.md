---
name: template-skill
description: Minimal starter template for creating new Claude skills following the v1.0 specification
license: Apache-2.0
---

# Template Skill

Use this template as a starting point for creating new Claude skills. This file demonstrates the proper structure and format required by the v1.0 specification.

## Required Components

### YAML Frontmatter
- **name**: Must match directory name exactly (lowercase, hyphens only)
- **description**: Clear explanation of what the skill does and when to use it
- **license**: (Optional) License identifier

### Instructions

Write clear, actionable instructions using imperative/infinitive form (verb-first):

✅ **DO**: "Create a new file"
❌ **DON'T**: "Creates a new file"

✅ **DO**: "Analyze the input data"
❌ **DON'T**: "Analyzes the input data"

## Skill Organization

Keep SKILL.md lean and high-level. For larger skills, organize additional resources:

- `scripts/` - Executable code for reliability and automation
- `references/` - Detailed documentation loaded as needed
- `templates/` - Starter files and boilerplates
- `examples/` - Demonstration code
- `assets/` - Resources and output files

## Instructions Format

Provide specific, actionable guidance:

1. **Step-by-step procedures** - Clear workflow for common tasks
2. **Examples** - Show DO/DON'T patterns
3. **References** - Link to bundled resources when helpful
4. **Decision trees** - Guide complex workflows

## Best Practices

- Be specific and concrete
- Use imperative verb-first language
- Include practical examples
- Keep SKILL.md concise
- Move detailed documentation to reference files
- Structure for grep-friendly discovery
- Test with real scenarios

## Customization

To create a new skill from this template:

1. Copy this directory to a new skill name (lowercase-with-hyphens)
2. Update the `name` field to match your directory name
3. Write a clear, specific `description`
4. Replace these instructions with your skill's guidance
5. Add scripts, references, and other resources as needed
6. Validate the YAML frontmatter
7. Test with actual use cases

## Validation Checklist

- [ ] Directory name matches `name` field exactly
- [ ] `name` uses only lowercase letters, numbers, and hyphens
- [ ] `description` clearly explains purpose and use cases
- [ ] Instructions use imperative/infinitive form
- [ ] YAML frontmatter is valid
- [ ] All referenced files exist
- [ ] Skill tested with real scenarios
