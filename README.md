# Universal Claude Skills

A curated collection of universally useful Claude skills for development, project management, and workflow automation. Following the official [Agent Skills v1.0 specification](agent_skills_spec.md).

## Overview

This repository provides production-ready skills that enhance Claude's capabilities for:

- **Development workflows** - Creating, testing, and managing code
- **Project management** - Task decomposition, issue tracking, and planning
- **Workflow automation** - Streamlining repetitive tasks and processes
- **Skill development** - Tools for creating your own custom skills

## Quick Start

### Installation (Claude Code)

Install the entire skill collection:

```bash
# Register this repository
/plugin marketplace add ironluffy/claude-skills

# Install skills
/plugin install universal-claude-skills
```

Or install individual skills:

```bash
/plugin install skill-creator@universal-claude-skills
/plugin install task-decomposer@universal-claude-skills
/plugin install issue-manager@universal-claude-skills
```

### Using Skills

Once installed, skills activate automatically when you mention them:

```
"Use the task-decomposer skill to break down this feature into subtasks"
"Use the issue-manager skill to report this blocker"
"Use the skill-creator to help me build a new skill"
```

## Available Skills

### 1. skill-creator

**Meta-skill for developing new Claude skills**

Create, validate, and package custom skills following best practices.

**Features:**
- Generate skill boilerplate with `init_skill.py`
- Validate against v1.0 specification with `package_skill.py`
- Comprehensive best practices documentation
- Real-world examples and templates

**Usage:**
```bash
cd skill-creator/scripts
python init_skill.py my-awesome-skill "Description of what it does"
# ... develop your skill ...
python package_skill.py ../my-awesome-skill
```

**When to use:**
- Creating new custom skills
- Learning skill development
- Validating existing skills
- Following best practices

[Full Documentation](skill-creator/SKILL.md) | [Scripts](skill-creator/scripts/) | [References](skill-creator/references/)

---

### 2. task-decomposer

**Break down complex tasks into actionable, testifiable subtasks with intelligent agent/human assignment**

Transform high-level Linear/GitHub tasks into structured decompositions with rationale, risk assessment, and automatic assignment to AI agents or humans.

**Features:**
- **Intelligent assignment** - Auto-detect agent vs human work 🤖👤
- **Decomposition analysis** - As-is → to-be, gap analysis
- **Actionable subtasks** - 1-4 hour chunks with clear deliverables
- **Testifiable criteria** - Acceptance tests per subtask
- **Risk assessment** - Identify and mitigate blockers
- **Linear/GitHub export** - Direct integration with assignments

**Usage:**
```bash
# Basic task decomposition
python scripts/analyze_task.py "Implement user authentication" --project backend

# Export to Linear with intelligent assignment
python scripts/analyze_task.py "Build payment processing" \
  --export-linear --team-id TEAM123 \
  --agent-user "agent-bot" \
  --human-users "backend:user-abc,security:user-def,default:user-xyz"
```

Output:
- 🤖 Agent tasks (code, tests, refactoring)
- 👤 Human tasks (decisions, approvals, strategy)
- ⚠️ Agent tasks requiring human review (security, payments)
- Rationale for decomposition approach
- As-is vs. to-be state analysis
- 5-8 subtasks with estimates
- Dependency graph
- Risk matrix with mitigation
- Linear-ready format with assignments

**When to use:**
- Planning complex features
- Breaking down epics
- Sprint planning
- Estimating work
- Creating Linear issues

[Full Documentation](task-decomposer/SKILL.md) | [Scripts](task-decomposer/scripts/) | [Framework](task-decomposer/references/decomposition-framework.md)

---

### 3. issue-manager

**Comprehensive GitHub/Linear/Jira issue management with intelligent assignment**

Report blocks, split complex issues, bulk update metadata, and automatically assign to agents or humans based on task characteristics.

**Features:**
- **Smart assignment** - Auto-assign to agents or humans 🤖👤
- **Blocker reporting** - Document what's blocking with context
- **Issue splitting** - Break large issues into manageable pieces
- **Bulk operations** - Update multiple issues consistently
- **Related issues** - Create linked follow-ups and subtasks
- **Block analysis** - Find critical path and suggest unblocking

**Usage:**

Auto-assign issues:
```bash
# Automatically detect and assign
python scripts/issue_operations.py auto-assign \
  --issue ISSUE-123 \
  --agent-user "agent-bot" \
  --human-users "default:user-xyz"

# Manual assignment
python scripts/issue_operations.py assign \
  --issue ISSUE-456 \
  --assignee "agent-bot" \
  --assignee-type agent

# Reassign from agent to human
python scripts/issue_operations.py reassign \
  --issue ISSUE-789 \
  --from-assignee "agent-bot" \
  --to-assignee "user-xyz" \
  --reason "Requires stakeholder approval"
```

Report a blocker:
```bash
python scripts/issue_operations.py report-blocker \
  --issue TEAM-123 \
  --blocked-by "Waiting for API design" \
  --impact high \
  --notify @team-lead
```

Split complex issue:
```bash
python scripts/issue_operations.py split-issue \
  --issue TEAM-456 \
  --num-subtasks 4 \
  --strategy acceptance-criteria
```

Bulk update:
```bash
python scripts/issue_operations.py bulk-update \
  --filter "label:backend AND status:todo" \
  --add-label "needs-review" \
  --dry-run  # Preview first!
```

**When to use:**
- Managing blocked work
- Organizing large issues
- Bulk triaging
- Sprint planning
- Release tracking

[Full Documentation](issue-manager/SKILL.md) | [Scripts](issue-manager/scripts/) | [Workflows](issue-manager/references/issue-workflows.md)

---

### 4. system-design-reviewer

**Review system designs and generate comprehensive text diagrams with architecture, security, performance, and cost analysis**

Analyze existing systems and generate detailed review reports with multi-format diagrams (Mermaid + ASCII), identifying issues and optimization opportunities across all dimensions.

**Features:**
- **Multi-format diagrams** - Mermaid (GitHub-renderable) + ASCII (universal)
- **Architecture review** - Scalability, reliability, maintainability analysis
- **Security assessment** - OWASP Top 10, auth/encryption gaps, vulnerability detection
- **Performance optimization** - Caching strategies, N+1 queries, load balancing
- **Cost efficiency** - Right-sizing, serverless opportunities, cloud cost reduction

**Usage:**
```bash
# Complete system design review
python scripts/review_design.py /path/to/project --output design-review.md

# Security-focused analysis
python scripts/security_analyzer.py /path/to/project --output security-report.md

# Performance analysis
python scripts/performance_analyzer.py /path/to/project --output perf-report.md

# Cost optimization
python scripts/cost_optimizer.py /path/to/project --output cost-report.md

# Generate diagrams only
python scripts/generate_diagrams.py /path/to/project --output diagrams/ --formats mermaid,ascii
```

Output includes:
- 📊 Architecture diagrams (components, services, databases)
- 🔄 Sequence diagrams (API flows, authentication)
- 🗂️ Database/ER diagrams (schema relationships)
- 📈 Flowcharts (business logic, decision trees)
- 🏗️ Architecture findings (scalability, reliability issues)
- 🔒 Security findings (OWASP compliance, vulnerabilities)
- ⚡ Performance opportunities (caching, query optimization)
- 💰 Cost optimization (30-50% savings potential)

**When to use:**
- Reviewing system architecture
- Planning major refactors
- Security audits
- Performance optimization
- Cost reduction initiatives
- Technical documentation

[Full Documentation](system-design-reviewer/SKILL.md) | [Scripts](system-design-reviewer/scripts/) | [References](system-design-reviewer/references/)

---

### 5. template-skill

**Minimal starter template for creating new skills**

Reference implementation showing proper skill structure.

**Features:**
- Valid SKILL.md with YAML frontmatter
- Documented structure and conventions
- Inline comments explaining each section
- Validation checklist

**When to use:**
- Starting a new skill
- Understanding skill format
- Quick reference for structure

[Full Documentation](template-skill/SKILL.md)

---

## Repository Structure

```
claude-skills/
├── .claude-plugin/          # Plugin marketplace configuration
├── .gitignore              # Git ignore rules
├── LICENSE                 # Apache 2.0 license
├── README.md               # This file
├── agent_skills_spec.md    # v1.0 specification
│
├── template-skill/         # Minimal starter template
│   └── SKILL.md
│
├── skill-creator/          # Meta-skill for creating skills
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── init_skill.py
│   │   └── package_skill.py
│   └── references/
│       ├── best-practices.md
│       └── examples.md
│
├── task-decomposer/        # Task decomposition for Linear/GitHub
│   ├── SKILL.md
│   ├── scripts/
│   │   └── analyze_task.py
│   └── references/
│       ├── decomposition-framework.md
│       └── output-templates.md
│
└── issue-manager/          # GitHub/Linear issue management
    ├── SKILL.md
    ├── scripts/
    │   ├── issue_operations.py
    │   └── analyze_blocks.py
    └── references/
        └── issue-workflows.md
```

## Skill Development

Want to create your own skills? Use the **skill-creator** meta-skill:

### 1. Initialize New Skill

```bash
cd skill-creator/scripts
python init_skill.py my-new-skill "Description of what it does"
```

This creates:
- `my-new-skill/SKILL.md` with valid frontmatter
- Standard directory structure
- README template
- .gitkeep files

### 2. Develop Skill Contents

Edit `my-new-skill/SKILL.md`:
- Use **imperative form** (verb-first instructions)
- Keep SKILL.md lean and high-level
- Add scripts, references, templates as needed
- Include DO/DON'T examples

### 3. Validate

```bash
cd skill-creator/scripts
python package_skill.py ../../my-new-skill
```

Checks:
- ✓ Valid YAML frontmatter
- ✓ Required fields present
- ✓ Name matches directory
- ✓ No broken file references
- ✓ Proper writing style

### 4. Test

Load your skill in Claude Code and test with real scenarios.

### 5. Share (Optional)

Submit a pull request to add your skill to this repository!

## Specification

All skills follow the [Agent Skills v1.0 specification](agent_skills_spec.md).

### Required: SKILL.md

Every skill must have a `SKILL.md` file with:

```markdown
---
name: skill-name-in-hyphen-case
description: Clear explanation of what the skill does and when to use it
license: Apache-2.0
---

# Skill Name

Instructions in imperative form (verb-first).

## Usage

Provide clear examples and guidance.
```

### Key Requirements

- **name** field must match directory name exactly
- Use lowercase-with-hyphens format
- Write instructions using imperative form
- Include specific, actionable guidance
- Add examples showing DO/DON'T patterns

## Best Practices

### Writing Skills

1. **Use imperative form** - "Create a file" not "Creates a file"
2. **Be specific** - Concrete steps, not vague instructions
3. **Show examples** - DO/DON'T patterns clarify intent
4. **Keep SKILL.md lean** - Move details to references
5. **Structure for discovery** - Grep-friendly organization

### Organizing Skills

```
skill-name/
├── SKILL.md                # Lean, high-level instructions
├── scripts/                # Executable automation
│   └── main.py
├── references/             # Detailed documentation
│   └── guide.md
├── templates/              # Starter files
│   └── config.json
└── examples/               # Demonstration code
    └── example.py
```

### Testing Skills

- Test with 3-5 real scenarios
- Verify all referenced files exist
- Validate with `package_skill.py`
- Get feedback from actual usage
- Iterate and refine

## Contributing

We welcome contributions! Here's how:

### Adding a New Skill

1. Fork this repository
2. Create your skill using `skill-creator`
3. Validate with `package_skill.py`
4. Test thoroughly
5. Submit a pull request

### Improving Existing Skills

1. Fork this repository
2. Make your improvements
3. Validate changes
4. Submit a pull request

### Reporting Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/ironluffy/claude-skills/issues).

## Skill Catalog

| Skill | Category | Purpose | Key Features |
|-------|----------|---------|--------------|
| **skill-creator** | Meta | Create new skills | Boilerplate generation, validation |
| **task-decomposer** | Project Management | Break down tasks | Decomposition, rationale, risk assessment |
| **issue-manager** | Project Management | Manage issues | Blockers, splitting, bulk operations |
| **template-skill** | Reference | Starter template | Minimal valid skill example |

## Platform Support

### Claude Code

✅ Full support via plugin installation

```bash
/plugin install universal-claude-skills
```

### Claude.ai

✅ Upload skills via Skills interface (paid plans)

### Claude API

✅ Use skills programmatically via API

See [API documentation](https://docs.anthropic.com/) for details.

## Platform Integration

### Linear

```bash
# Task decomposition with Linear export
python task-decomposer/scripts/analyze_task.py "..." \
  --export-linear --team-id TEAM123

# Issue management for Linear
export LINEAR_API_KEY="your-key"
python issue-manager/scripts/issue_operations.py --platform linear ...
```

### GitHub

```bash
# Task decomposition with GitHub export
python task-decomposer/scripts/analyze_task.py "..." \
  --export-github --repo owner/repo

# Issue management for GitHub
export GITHUB_TOKEN="your-token"
python issue-manager/scripts/issue_operations.py --platform github ...
```

### Jira

```bash
# Issue management for Jira
export JIRA_API_TOKEN="your-token"
export JIRA_DOMAIN="your-domain.atlassian.net"
python issue-manager/scripts/issue_operations.py --platform jira ...
```

## Requirements

### Python Scripts

Most skills include Python scripts requiring:

- Python 3.8+
- Dependencies listed in individual skill directories

Install dependencies:
```bash
pip install pyyaml  # For skill-creator validation
```

### Environment Variables

For platform integrations:

```bash
# Linear
export LINEAR_API_KEY="your-linear-api-key"

# GitHub
export GITHUB_TOKEN="your-github-token"

# Jira
export JIRA_API_TOKEN="your-jira-token"
export JIRA_DOMAIN="your-domain.atlassian.net"
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [Anthropic's Skills Repository](https://github.com/anthropics/skills)
- Follows the [Agent Skills v1.0 Specification](agent_skills_spec.md)
- Built for the Claude Code community

## Support

- **Documentation:** See individual skill README files
- **Issues:** [GitHub Issues](https://github.com/ironluffy/claude-skills/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ironluffy/claude-skills/discussions)

## Roadmap

Planned skills:

- [ ] **code-reviewer** - Automated code review with best practices
- [ ] **test-generator** - Generate comprehensive test suites
- [ ] **api-docs** - Generate API documentation from code
- [ ] **migration-planner** - Plan and execute migrations
- [ ] **performance-analyzer** - Analyze and optimize performance

Want to contribute one of these or suggest others? Open an issue!

---

**Happy Skill Building! 🚀**

For questions or feedback, please [open an issue](https://github.com/ironluffy/claude-skills/issues).
