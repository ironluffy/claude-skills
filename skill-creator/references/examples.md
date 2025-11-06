# Skill Examples

Real-world examples of well-structured skills demonstrating best practices.

## Example 1: Simple Utility Skill

### Structure
```
json-formatter/
├── SKILL.md
└── scripts/
    └── format.py
```

### SKILL.md
```markdown
---
name: json-formatter
description: Format and validate JSON files with customizable indentation and sorting
license: Apache-2.0
---

# JSON Formatter

Format and validate JSON files for improved readability and consistency.

## Basic Usage

Format a JSON file with standard 2-space indentation:
```bash
python scripts/format.py input.json output.json
```

## Options

- `--indent N` - Set indentation (default: 2)
- `--sort-keys` - Sort object keys alphabetically
- `--validate` - Validate only, don't format
- `--compact` - Minimize whitespace

## Examples

✅ **DO**: Format with sorted keys
```bash
python scripts/format.py --sort-keys --indent 4 data.json formatted.json
```

❌ **DON'T**: Modify files without backup
```bash
python scripts/format.py data.json data.json  # Overwrites original!
```

## Best Practices

1. Always validate before formatting
2. Keep backups of original files
3. Use consistent indentation across project
4. Sort keys for diff-friendly JSON
```

---

## Example 2: Workflow Skill with References

### Structure
```
api-docs-generator/
├── SKILL.md
├── scripts/
│   ├── generate.py
│   ├── validate.py
│   └── utils.py
├── references/
│   ├── openapi-guide.md
│   └── examples.md
└── templates/
    └── openapi-base.yaml
```

### SKILL.md
```markdown
---
name: api-docs-generator
description: Generate OpenAPI documentation from code annotations with validation and examples
license: Apache-2.0
---

# API Documentation Generator

Generate comprehensive OpenAPI 3.0 documentation from annotated source code.

## Workflow

### 1. Annotate Your Code

Add docstrings with OpenAPI metadata:
```python
def get_user(user_id: int) -> User:
    """
    Get user by ID.

    OpenAPI:
      summary: Retrieve user
      parameters:
        - name: user_id
          type: integer
          required: true
      responses:
        200: User object
        404: User not found
    """
```

### 2. Generate Documentation

Run the generator:
```bash
python scripts/generate.py src/ openapi.yaml
```

### 3. Validate Output

Ensure specification is valid:
```bash
python scripts/validate.py openapi.yaml
```

## Decision Tree

**Starting from scratch?**
→ Copy `templates/openapi-base.yaml`
→ See `references/openapi-guide.md` for structure

**Adding to existing docs?**
→ Use `--merge` flag
→ See `references/examples.md` for patterns

**Need custom formatting?**
→ See `references/openapi-guide.md` advanced section

## Examples

See `references/examples.md` for:
- REST API documentation
- WebSocket endpoints
- Authentication schemes
- Error response patterns
```

### references/openapi-guide.md
```markdown
# OpenAPI Documentation Guide

## Structure

OpenAPI 3.0 documents have this structure:

```yaml
openapi: 3.0.0
info:
  title: API Name
  version: 1.0.0
  description: API description

servers:
  - url: https://api.example.com
    description: Production

paths:
  /users/{id}:
    get:
      summary: Get user
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
```

## [PATTERN] Authentication

### Bearer Token
```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### API Key
```yaml
components:
  securitySchemes:
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - apiKey: []
```

## [ERROR] Common Issues

### Invalid References

❌ **Wrong:**
```yaml
$ref: '#/schemas/User'  # Missing /components/
```

✅ **Correct:**
```yaml
$ref: '#/components/schemas/User'
```

### Missing Required Fields

❌ **Wrong:**
```yaml
openapi: 3.0.0
paths: {}  # Missing info field
```

✅ **Correct:**
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths: {}
```
```

---

## Example 3: Complex Multi-Script Skill

### Structure
```
database-migrator/
├── SKILL.md
├── scripts/
│   ├── create_migration.py
│   ├── run_migrations.py
│   ├── rollback.py
│   ├── validate.py
│   └── utils/
│       ├── db.py
│       └── schema.py
├── references/
│   ├── migration-guide.md
│   ├── best-practices.md
│   └── troubleshooting.md
├── templates/
│   ├── migration_template.sql
│   └── config_template.json
└── examples/
    ├── add_column.sql
    └── create_table.sql
```

### SKILL.md
```markdown
---
name: database-migrator
description: Manage database schema migrations with validation, versioning, and rollback support
license: Apache-2.0
---

# Database Migrator

Safely manage database schema changes with automated migration tracking.

## Quick Start

### Create Migration

Generate migration from schema changes:
```bash
python scripts/create_migration.py "add_user_email_column"
```

Edits: `migrations/001_add_user_email_column.sql`

### Run Migrations

Apply pending migrations:
```bash
python scripts/run_migrations.py --config config.json
```

### Validate

Check migration integrity:
```bash
python scripts/validate.py
```

## Workflow Selection

**New table?**
→ `python scripts/create_migration.py "create_<table>_table"`
→ See `templates/create_table.sql`
→ Reference: `references/migration-guide.md` schema section

**Modify column?**
→ `python scripts/create_migration.py "alter_<table>_<column>"`
→ See `examples/add_column.sql`
→ Reference: `references/migration-guide.md` alter section

**Data migration?**
→ `python scripts/create_migration.py "migrate_<description>"`
→ See `references/best-practices.md` data migration section

**Rollback needed?**
→ `python scripts/rollback.py --steps N`
→ See `references/troubleshooting.md` rollback section

## Safety Features

1. **Automatic Backups**: Snapshots before migrations
2. **Validation**: Schema integrity checks
3. **Transactions**: Atomic operations
4. **Rollback**: Undo capabilities
5. **Dry Run**: Preview changes

## Best Practices

See `references/best-practices.md` for:
- Migration naming conventions
- Testing strategies
- Production deployment
- Data preservation
- Performance considerations

## Troubleshooting

See `references/troubleshooting.md` for:
- Failed migration recovery
- Conflict resolution
- Performance issues
- Connection problems
```

### scripts/create_migration.py
```python
#!/usr/bin/env python3
"""
Create a new database migration file.

Usage:
    python create_migration.py "description"
    python create_migration.py "add_user_email" --template add_column

Examples:
    python create_migration.py "create_users_table"
    python create_migration.py "add_email_to_users" --template add_column
"""

import sys
import os
from datetime import datetime
from pathlib import Path


def create_migration(description: str, template: str = None) -> str:
    """Create new migration file."""

    # Generate migration number
    migrations_dir = Path("migrations")
    migrations_dir.mkdir(exist_ok=True)

    existing = sorted(migrations_dir.glob("*.sql"))
    next_num = len(existing) + 1

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{next_num:03d}_{description}_{timestamp}.sql"
    filepath = migrations_dir / filename

    # Load template
    if template:
        template_path = Path("templates") / f"{template}.sql"
        if template_path.exists():
            content = template_path.read_text()
        else:
            print(f"Warning: Template {template} not found, using default")
            content = get_default_template()
    else:
        content = get_default_template()

    # Create migration file
    filepath.write_text(content)

    print(f"Created migration: {filepath}")
    print(f"\nEdit the file and run:")
    print(f"  python scripts/run_migrations.py")

    return str(filepath)


def get_default_template() -> str:
    """Get default migration template."""
    return """-- Migration: [Description]
-- Created: [Date]

-- UP Migration
BEGIN;

-- Add your schema changes here


COMMIT;

-- DOWN Migration (for rollback)
BEGIN;

-- Add rollback logic here


COMMIT;
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    description = sys.argv[1]
    template = sys.argv[2] if len(sys.argv) > 2 else None

    create_migration(description, template)
```

---

## Key Patterns Demonstrated

### 1. Progressive Complexity
- Start with simple examples
- Introduce advanced features gradually
- Always link to detailed references

### 2. Clear Decision Trees
- Help users choose the right workflow
- Provide specific paths for common scenarios
- Link to relevant documentation

### 3. Executable Scripts
- Make tools reliable and robust
- Include proper error handling
- Provide clear usage documentation

### 4. Reference Organization
- Detailed guides for complex topics
- Grep-friendly structure with tags
- Comprehensive troubleshooting

### 5. Template Usage
- Provide starter files
- Show common patterns
- Reduce boilerplate

## Quality Indicators

Good skills demonstrate:

✓ Imperative instructions
✓ Clear examples with DO/DON'T
✓ Logical organization
✓ Reliable scripts
✓ Comprehensive references
✓ Grep-friendly structure
✓ Proper error handling
✓ Validation tools
✓ Troubleshooting guides
✓ Real-world testing
