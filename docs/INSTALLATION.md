# Installation Guide

Quick guide for installing and using Universal Claude Skills in Claude Code.

## Prerequisites

- Claude Code CLI installed
- Python 3.8+ (for script-based skills)
- Git (for cloning the repository)

## Installation Methods

### Method 1: Plugin Marketplace (Recommended)

Install the entire skill collection from the Claude Code marketplace:

```bash
# Add the repository to your marketplace
/plugin marketplace add ironluffy/claude-skills

# Install all skills
/plugin install universal-claude-skills
```

This installs all 5 skills:
- ✅ skill-creator
- ✅ task-decomposer
- ✅ issue-manager
- ✅ **system-design-reviewer** (NEW!)
- ✅ template-skill

### Method 2: Install Individual Skills

Install specific skills only:

```bash
/plugin install skill-creator@universal-claude-skills
/plugin install task-decomposer@universal-claude-skills
/plugin install issue-manager@universal-claude-skills
/plugin install system-design-reviewer@universal-claude-skills
```

### Method 3: Local Installation

Clone and use locally:

```bash
# Clone the repository
git clone https://github.com/ironluffy/claude-skills.git

# In Claude Code, point to the local directory
/plugin install /path/to/claude-skills
```

## Using Skills

Once installed, skills activate automatically when you mention them:

### System Design Reviewer

```
"Use the system-design-reviewer skill to analyze my project at /path/to/project"

"Review the architecture in this codebase and generate diagrams"

"Run a security analysis on the current project using system-design-reviewer"
```

### Task Decomposer

```
"Use the task-decomposer skill to break down this feature:
 Implement user authentication with JWT tokens"

"Decompose this epic into Linear-ready subtasks"
```

### Issue Manager

```
"Use the issue-manager skill to report a blocker on ISSUE-123"

"Split this complex issue into smaller tasks"
```

### Skill Creator

```
"Use the skill-creator to help me build a new skill for API documentation"
```

## Direct Script Usage

You can also run the Python scripts directly:

```bash
# System Design Review
cd system-design-reviewer/scripts
python3 review_design.py /path/to/project --output review.md

# Security Analysis
python3 security_analyzer.py /path/to/project

# Performance Analysis
python3 performance_analyzer.py /path/to/project

# Cost Optimization
python3 cost_optimizer.py /path/to/project

# Generate Diagrams
python3 generate_diagrams.py /path/to/project
```

## Verifying Installation

Check installed skills:

```bash
/plugin list
```

Should show:
```
universal-claude-skills (v1.1.0)
├─ skill-creator
├─ task-decomposer
├─ issue-manager
├─ system-design-reviewer ⭐ NEW
└─ template-skill
```

## Configuration

### Linear Integration (task-decomposer, issue-manager)

Set your Linear API key:

```bash
export LINEAR_API_KEY="lin_api_your_key_here"
```

### GitHub Integration (issue-manager)

Authenticate with GitHub CLI:

```bash
gh auth login
```

## Troubleshooting

### Skills Not Activating

1. Check installation: `/plugin list`
2. Verify SKILL.md exists in each skill directory
3. Try explicitly mentioning: "Use the [skill-name] skill to..."

### Python Scripts Failing

1. Verify Python 3.8+: `python3 --version`
2. Check script permissions: `chmod +x scripts/*.py`
3. Install dependencies if needed (most scripts have no external dependencies)

### Plugin Not Found

1. Ensure repository is added: `/plugin marketplace add ironluffy/claude-skills`
2. Try refreshing: `/plugin marketplace refresh`
3. Check GitHub repo is accessible: https://github.com/ironluffy/claude-skills

## Updates

Check for skill updates:

```bash
# Update all plugins
/plugin update

# Update specific plugin
/plugin update universal-claude-skills
```

## Uninstallation

```bash
# Uninstall all skills
/plugin uninstall universal-claude-skills

# Uninstall individual skill
/plugin uninstall system-design-reviewer@universal-claude-skills
```

## Getting Help

- **Documentation**: Each skill has comprehensive docs in its SKILL.md file
- **Issues**: https://github.com/ironluffy/claude-skills/issues
- **Examples**: Check the `examples/` directory in each skill
- **References**: Detailed guides in `references/` directories

## What's New in v1.1.0

🆕 **system-design-reviewer skill**
- Multi-format diagram generation (Mermaid + ASCII)
- Architecture, security, performance, and cost analysis
- Comprehensive review reports with actionable recommendations

📈 **Enhanced capabilities**
- 5 production-ready skills (up from 4)
- New architecture review category
- 30-50% cost optimization potential
- OWASP Top 10 security scanning

## Next Steps

1. ✅ Install the plugin
2. ✅ Try the system-design-reviewer on your project
3. ✅ Review the generated diagrams and recommendations
4. ✅ Explore other skills (task-decomposer, issue-manager)
5. ✅ Create your own skills using skill-creator

Happy coding! 🚀
