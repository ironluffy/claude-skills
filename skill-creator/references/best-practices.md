# Skill Development Best Practices

Comprehensive guidelines for creating high-quality Claude skills.

## Design Philosophy

### Skills as Onboarding Guides

Think of skills as onboarding materials that transform Claude into a specialized agent:

- **Bundle procedural knowledge** - Step-by-step workflows and processes
- **Include tool integrations** - Scripts and utilities for automation
- **Provide domain expertise** - Best practices and common patterns
- **Enable self-sufficiency** - Everything needed to complete tasks

### Information Architecture

**SKILL.md stays lean:**
- Core instructions and workflows
- Decision trees for complexity
- Quick reference examples
- Pointers to detailed resources

**References contain depth:**
- Extensive API documentation
- Advanced usage scenarios
- Troubleshooting guides
- Comprehensive examples

## Writing Guidelines

### Imperative Form (Critical)

Always use verb-first imperative/infinitive form:

**✅ Correct (Imperative):**
- "Create a new project"
- "Analyze the input data"
- "Generate test cases"
- "Validate API responses"
- "Transform the document"

**❌ Incorrect (Third Person):**
- "Creates a new project"
- "Analyzes the input data"
- "Generates test cases"
- "Validates API responses"
- "Transforms the document"

### Specificity and Clarity

Provide concrete, actionable instructions:

**✅ Specific Steps:**
```markdown
1. Install dependencies: `npm install`
2. Configure environment: Copy `.env.example` to `.env`
3. Run migrations: `npm run migrate`
4. Start server: `npm start`
5. Verify: Visit `http://localhost:3000/health`
```

**❌ Vague Instructions:**
```markdown
Set up the project and make sure it works.
```

### Examples and Patterns

Always include DO/DON'T examples:

**✅ Effective Example:**
```markdown
## Error Handling

✅ **DO**: Catch specific exceptions
```python
try:
    result = process_data(input)
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    return None
except IOError as e:
    logger.error(f"File error: {e}")
    raise
```

❌ **DON'T**: Use bare except clauses
```python
try:
    result = process_data(input)
except:
    pass  # Silently fails, hard to debug
```
```

## Content Organization

### Directory Structure

Organize resources logically:

```
skill-name/
├── SKILL.md                    # Lean, high-level instructions
├── scripts/                    # Executable automation
│   ├── main.py                 # Primary script
│   ├── utils.py                # Helper functions
│   └── validate.sh             # Validation script
├── references/                 # Detailed documentation
│   ├── api-reference.md        # Complete API docs
│   ├── advanced-usage.md       # Complex scenarios
│   ├── troubleshooting.md      # Common issues
│   └── examples.md             # Extended examples
├── templates/                  # Starter files
│   ├── config.json             # Configuration template
│   └── starter.py              # Boilerplate code
└── examples/                   # Demonstration code
    ├── basic-example.py        # Simple use case
    └── advanced-example.py     # Complex use case
```

### Grep-Friendly Structure

Make content easy to search:

**Use consistent prefixes:**
```markdown
## [WORKFLOW] Basic Document Processing
## [WORKFLOW] Advanced Multi-Document Processing
## [WORKFLOW] Batch Processing

## [ERROR] Common Validation Errors
## [ERROR] Network and Timeout Errors
## [ERROR] Authentication Failures

## [CONFIG] Environment Variables
## [CONFIG] Command-Line Options
## [CONFIG] Configuration Files
```

**Include searchable keywords:**
```markdown
<!-- Keywords: authentication, oauth, jwt, token -->
## Authentication Setup

<!-- Keywords: error handling, exceptions, logging -->
## Error Management

<!-- Keywords: performance, optimization, caching -->
## Performance Tuning
```

## Script Development

### Make Scripts Reliable

**Include proper error handling:**
```python
#!/usr/bin/env python3
"""
Script description and usage.
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        # Main logic
        result = process()
        logger.info("Processing completed successfully")
        return 0
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
```

**Add usage documentation:**
```python
"""
Data Processor Script

Process input data and generate reports.

Usage:
    python process.py input.json output.json
    python process.py --validate input.json
    python process.py --help

Arguments:
    input.json      Input data file
    output.json     Output destination

Options:
    --validate      Validate only, don't process
    --verbose       Enable debug logging
    --help          Show this help message

Examples:
    python process.py data.json results.json
    python process.py --validate --verbose data.json
"""
```

### Make Scripts Executable

```bash
# Add shebang
#!/usr/bin/env python3

# Make executable
chmod +x scripts/process.py

# Test directly
./scripts/process.py --help
```

## Reference Documentation

### API Documentation

Provide complete API references:

```markdown
## API Reference

### `process_data(input_data, options=None)`

Process input data according to specified options.

**Parameters:**
- `input_data` (dict): Input data structure
  - `type` (str): Data type ("json", "xml", "csv")
  - `content` (str): Raw content
  - `encoding` (str, optional): Character encoding (default: "utf-8")
- `options` (dict, optional): Processing options
  - `validate` (bool): Validate before processing (default: True)
  - `strict` (bool): Strict mode (default: False)

**Returns:**
- `dict`: Processed data structure
  - `status` (str): "success" or "error"
  - `data` (any): Processed content
  - `errors` (list): Error messages if any

**Raises:**
- `ValueError`: Invalid input data
- `IOError`: File access errors
- `RuntimeError`: Processing errors

**Example:**
```python
input_data = {
    "type": "json",
    "content": '{"key": "value"}'
}
options = {"validate": True, "strict": True}
result = process_data(input_data, options)
```
```

### Troubleshooting Guides

Document common issues:

```markdown
## Troubleshooting

### Error: "Invalid API Key"

**Symptoms:**
- Authentication failures
- 401 Unauthorized responses

**Causes:**
- API key not set
- Incorrect key format
- Expired key

**Solutions:**
1. Verify API key in `.env` file
2. Check key format (should be `sk-...`)
3. Regenerate key if expired
4. Ensure no extra whitespace

**Example:**
```bash
# Check current key
echo $API_KEY

# Set correct key
export API_KEY="sk-your-key-here"
```

### Performance Issues

**Symptoms:**
- Slow processing
- High memory usage
- Timeouts

**Solutions:**
1. Enable caching: `--cache-enabled`
2. Reduce batch size: `--batch-size 10`
3. Use streaming: `--stream`
4. Monitor resources: `scripts/monitor.sh`
```

## Quality Standards

### Validation Checklist

Before releasing a skill:

**Structure:**
- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] Name follows specification (lowercase-with-hyphens)
- [ ] Directory name matches `name` field
- [ ] All referenced files exist

**Content:**
- [ ] Instructions use imperative form
- [ ] Examples show DO/DON'T patterns
- [ ] Clear, specific, actionable steps
- [ ] No vague or ambiguous instructions

**Organization:**
- [ ] SKILL.md is lean and high-level
- [ ] Detailed docs in references/
- [ ] Scripts are reliable and tested
- [ ] Grep-friendly structure

**Testing:**
- [ ] Tested with 3-5 real scenarios
- [ ] Edge cases handled
- [ ] Error messages are helpful
- [ ] Scripts execute successfully

**Documentation:**
- [ ] Clear description in frontmatter
- [ ] Usage examples included
- [ ] API reference complete
- [ ] Troubleshooting guide provided

### Code Quality

**Scripts should:**
- Use proper error handling
- Include logging
- Have clear variable names
- Include docstrings
- Follow language conventions
- Be well-commented

**Documentation should:**
- Use clear, simple language
- Include concrete examples
- Avoid jargon (or define it)
- Have proper formatting
- Be up-to-date

## Common Patterns

### Decision Trees

Guide users through complex choices:

```markdown
## Workflow Selection

**Creating new resource?**
→ `scripts/create.py`
→ See `references/creation-guide.md`

**Modifying existing resource?**
  - **Simple edit?**
    → `scripts/edit.py`
    → See `references/editing-basics.md`

  - **Complex transformation?**
    → `scripts/transform.py`
    → See `references/transformation-guide.md`

**Analyzing resource?**
→ `scripts/analyze.py`
→ See `references/analysis-guide.md`
```

### Batching Strategies

Optimize for efficiency:

```markdown
## Batch Processing

Group related operations (recommended: 3-10 items per batch):

1. **Collect**: Gather all pending changes
2. **Validate**: Check batch coherence
   ```python
   if not all(item.type == batch_type for item in batch):
       split_by_type(batch)
   ```
3. **Execute**: Process batch atomically
4. **Verify**: Confirm all succeeded
5. **Handle**: Process failures individually
```

### Progressive Disclosure

Start simple, reveal complexity as needed:

```markdown
## Getting Started

Basic usage (90% of cases):
```bash
python process.py input.txt
```

### Advanced Options

Need more control? Add options:
```bash
python process.py input.txt --format json --validate
```

See `references/advanced-usage.md` for:
- Custom processors
- Batch operations
- Performance tuning
- Integration patterns
```

## Maintenance

### Keep Skills Current

- Update for API changes
- Refine based on feedback
- Add new patterns as discovered
- Fix bugs promptly
- Improve documentation

### Version Documentation

```markdown
## Changelog

### v1.1.0 (2025-01-15)
- Added batch processing support
- Improved error messages
- Updated API reference

### v1.0.0 (2025-01-01)
- Initial release
```

## Summary

1. **Write imperative** - Verb-first instructions
2. **Be specific** - Concrete, actionable steps
3. **Show examples** - DO/DON'T patterns
4. **Organize logically** - Lean SKILL.md, detailed references
5. **Make grep-friendly** - Searchable structure
6. **Build reliable scripts** - Error handling, logging
7. **Document thoroughly** - API reference, troubleshooting
8. **Test extensively** - Real scenarios, edge cases
9. **Iterate continuously** - Refine based on usage
10. **Validate rigorously** - Use package_skill.py
