---
name: skill-creator
description: Guide for developing, validating, and packaging new Claude skills following the v1.0 specification with automated tooling
license: Apache-2.0
---

# Skill Creator

Transform Claude into a specialized skill development agent. This skill bundles best practices, automated tooling, and templates for creating high-quality Claude skills.

## Skill Development Process

Follow this six-step workflow to create professional skills:

### 1. Understand with Examples

Gather concrete use cases before designing:
- Collect 3-5 real-world scenarios
- Identify common patterns and edge cases
- Document user needs and pain points
- Review existing similar skills for inspiration

### 2. Plan Reusable Contents

Identify what resources your skill needs:
- **Scripts** - Executable code for reliability (Python, Shell, JavaScript)
- **References** - Detailed documentation loaded as needed
- **Templates** - Starter files and boilerplates
- **Examples** - Demonstration code showing DO/DON'T patterns
- **Assets** - Resources, data files, or output samples

### 3. Initialize Skill Structure

Use the provided script to generate boilerplate:

```bash
cd skill-creator/scripts
python init_skill.py <skill-name> "<description>"
```

This creates:
- Directory with proper naming (lowercase-with-hyphens)
- SKILL.md with valid YAML frontmatter
- Standard subdirectories (scripts/, references/, etc.)
- README template

### 4. Edit and Develop

Write skill contents following best practices:

**SKILL.md Instructions:**
- Use imperative/infinitive form (verb-first)
- Keep high-level and concise
- Include clear examples
- Reference bundled resources
- Structure for grep-friendly discovery

**Scripts:**
- Make executable and reliable
- Include error handling
- Add usage examples in comments
- Test thoroughly

**References:**
- Organize detailed documentation
- Use clear section headers
- Include code examples
- Keep grep-friendly structure

### 5. Package and Validate

Validate your skill before distribution:

```bash
cd skill-creator/scripts
python package_skill.py <skill-directory>
```

This checks:
- Valid YAML frontmatter
- Required fields present (name, description)
- Directory name matches `name` field
- No restricted characters
- Proper markdown formatting
- Referenced files exist

### 6. Iterate and Refine

Test with real-world scenarios:
- Load skill in Claude Code
- Run through actual use cases
- Gather feedback
- Refine instructions and resources
- Re-validate and package

## Writing Style Guidelines

### Imperative Form (Required)

✅ **DO - Verb First:**
- "Create a new document"
- "Analyze the input data"
- "Generate test cases"
- "Validate API responses"

❌ **DON'T - Third Person:**
- "Creates a new document"
- "Analyzes the input data"
- "Generates test cases"
- "Validates API responses"

### Specific and Actionable

✅ **DO - Clear Steps:**
```markdown
1. Extract form fields using `scripts/extract_fields.py`
2. Validate field types against schema
3. Generate output in JSON format
4. Save to `output/extracted_data.json`
```

❌ **DON'T - Vague Instructions:**
```markdown
Process the form and extract the data somehow.
```

### Show Examples

Include DO/DON'T patterns for clarity:

```markdown
## Input Validation

✅ **DO**: Check for null values before processing
```python
if data is None or len(data) == 0:
    raise ValueError("Input data is required")
```

❌ **DON'T**: Assume input is always valid
```python
# This will crash if data is None
result = data.process()
```
```

## Content Organization Principles

### Keep SKILL.md Lean

SKILL.md should be concise and high-level:
- Core instructions and workflow
- Decision trees for complex paths
- References to detailed documentation
- Quick examples and patterns

### Move Details to References

Extensive documentation goes in `references/`:
- `references/api-guide.md` - Detailed API documentation
- `references/advanced-usage.md` - Complex scenarios
- `references/troubleshooting.md` - Common issues and solutions

### Structure for Discovery

Organize content for grep-friendly searching:
- Use consistent section headers
- Include keywords in headers
- Group related concepts together
- Add tags or labels where helpful

Example:
```markdown
## [WORKFLOW] Basic Document Processing
## [WORKFLOW] Advanced Multi-Document Processing
## [ERROR] Common Validation Errors
## [ERROR] Network and Timeout Errors
```

## Naming Conventions

### Skill Names
- Lowercase with hyphens only
- Alphanumeric characters permitted
- No spaces, underscores, or special characters
- Must match directory name exactly

✅ **Valid Names:**
- `task-decomposer`
- `pdf-analyzer`
- `mcp-server-builder`
- `api-docs-generator`

❌ **Invalid Names:**
- `Task_Decomposer` (uppercase, underscore)
- `pdf analyzer` (space)
- `api-docs-generator!` (special character)
- `PDFAnalyzer` (uppercase, no hyphens)

### Directory Structure
```
skill-name/
├── SKILL.md              (Required)
├── scripts/              (Optional)
│   ├── process.py
│   └── validate.sh
├── references/           (Optional)
│   ├── api-guide.md
│   └── examples.md
├── templates/            (Optional)
│   └── starter.json
└── assets/               (Optional)
    └── logo.png
```

## Validation Requirements

Skills must pass these checks:

### Required
- [ ] SKILL.md file exists
- [ ] Valid YAML frontmatter
- [ ] `name` field present and valid
- [ ] `description` field present and descriptive
- [ ] Directory name matches `name` field
- [ ] Instructions use imperative form

### Recommended
- [ ] License specified
- [ ] Scripts are executable
- [ ] References are well-organized
- [ ] Examples show DO/DON'T patterns
- [ ] Tested with real scenarios
- [ ] No broken references to files

## Bundled Tools

### scripts/init_skill.py

Generate new skill boilerplate:

```bash
python init_skill.py my-skill "Description of what this skill does"
```

Creates complete directory structure with:
- Valid SKILL.md template
- Standard subdirectories
- README with instructions
- .gitkeep files for empty directories

### scripts/package_skill.py

Validate and package skill:

```bash
python package_skill.py ../my-skill
```

Performs:
- YAML frontmatter validation
- Name format checking
- Directory name verification
- File reference validation
- Markdown syntax checking
- Generates validation report

Output:
- ✅ Validation passed - Skill is ready
- ❌ Validation failed - Lists specific issues to fix

## Best Practices Summary

1. **Start with concrete examples** - Real use cases drive good design
2. **Plan before coding** - Identify needed resources upfront
3. **Use provided tools** - init_skill.py and package_skill.py save time
4. **Write imperative instructions** - Verb-first, actionable steps
5. **Keep SKILL.md lean** - Move details to references
6. **Show examples** - DO/DON'T patterns clarify intent
7. **Structure for discovery** - Grep-friendly organization
8. **Validate thoroughly** - Use package_skill.py before distribution
9. **Test with real scenarios** - Ensure skill works as intended
10. **Iterate based on feedback** - Refine and improve over time

## Common Patterns

### Decision Trees

For complex workflows with multiple paths:

```markdown
## Workflow Selection

**If** you need to create a new document:
→ Use `scripts/create_new.py`
→ See `references/creation-guide.md`

**If** you need to edit existing document:
→ Use `scripts/edit_existing.py`
→ See `references/editing-guide.md`

**If** you need to analyze document:
→ Use `scripts/analyze.py`
→ See `references/analysis-guide.md`
```

### Batching Strategies

For operations that benefit from grouping:

```markdown
## Batch Processing

Group related changes together (3-10 items per batch):

1. Collect all changes
2. Validate batch coherence
3. Execute batch operation
4. Verify results
5. Handle errors individually
```

### Resource References

Link to bundled files effectively:

```markdown
## Advanced Configuration

For detailed API reference, see `references/api-guide.md`

Use the starter template: `templates/config.json`

Run validation: `scripts/validate.sh --strict`
```

## Quality Checklist

Before publishing your skill:

- [ ] Skill name is descriptive and follows naming conventions
- [ ] Description clearly explains purpose and use cases
- [ ] Instructions are specific and actionable
- [ ] Examples show DO/DON'T patterns
- [ ] Scripts are tested and reliable
- [ ] References are well-organized
- [ ] No broken file references
- [ ] Validation passes (package_skill.py)
- [ ] Tested with 3-5 real scenarios
- [ ] Documentation is clear and complete

## Getting Help

For questions or issues:
- Review `references/best-practices.md` for detailed guidance
- Check `references/examples.md` for skill examples
- Examine existing skills in the repository
- Consult the agent_skills_spec.md specification

## Next Steps

Ready to create your first skill?

1. Run `python scripts/init_skill.py <name> "<description>"`
2. Edit the generated SKILL.md
3. Add scripts and references as needed
4. Validate with `python scripts/package_skill.py <skill-dir>`
5. Test with real use cases
6. Iterate and refine
7. Share your skill!
