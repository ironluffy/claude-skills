# Quick Start Guide

Get up and running with Universal Claude Skills in 5 minutes!

## 1. Installation (Choose One)

### Option A: Claude Code Plugin (Recommended)

```bash
# In Claude Code
/plugin marketplace add yourusername/claude-skills
/plugin install universal-claude-skills
```

### Option B: Clone Repository

```bash
git clone https://github.com/yourusername/claude-skills.git
cd claude-skills
```

## 2. First Skill Usage

### Using skill-creator

```bash
# Create a new skill
./skill-helper.sh create my-first-skill "Analyze code quality"

# Validate it
./skill-helper.sh validate my-first-skill
```

### Using task-decomposer

```bash
# Decompose a task
./skill-helper.sh decompose "Build user authentication system"

# Or run the example
./skill-helper.sh decompose-example
```

### Using issue-manager

```bash
# Report a blocker
./skill-helper.sh block TEAM-123 "Waiting for API design"

# Split an issue
./skill-helper.sh split TEAM-456
```

## 3. Platform Integration

### Linear

```bash
# Set API key
export LINEAR_API_KEY="your-linear-api-key"

# Use with task decomposer
python3 task-decomposer/scripts/analyze_task.py \
  "Implement feature" \
  --export-linear \
  --team-id TEAM123
```

### GitHub

```bash
# Set token
export GITHUB_TOKEN="your-github-token"

# Use with issue manager
python3 issue-manager/scripts/issue_operations.py \
  --platform github \
  report-blocker \
  --issue "123" \
  --blocked-by "Design approval needed"
```

## 4. Key Commands

### Helper Script

```bash
# List all skills
./skill-helper.sh list

# Test all skills
./skill-helper.sh test-all

# Show examples
./skill-helper.sh examples

# Get help
./skill-helper.sh help
```

### Skill Creator

```bash
cd skill-creator/scripts

# Create new skill
./init_skill.py my-skill "Description"

# Validate skill
./package_skill.py ../../my-skill
```

### Task Decomposer

```bash
cd task-decomposer/scripts

# Basic decomposition
./analyze_task.py "Task description"

# With options
./analyze_task.py "Task" \
  --project backend \
  --complexity high \
  --output decomposition.md
```

### Issue Manager

```bash
cd issue-manager/scripts

# Report blocker
./issue_operations.py report-blocker \
  --issue TEAM-123 \
  --blocked-by "Reason"

# Split issue
./issue_operations.py split-issue \
  --issue TEAM-456 \
  --num-subtasks 4

# Bulk update (with dry-run!)
./issue_operations.py bulk-update \
  --filter "label:backend" \
  --add-label "needs-review" \
  --dry-run
```

## 5. Common Workflows

### Creating a Custom Skill

```bash
# 1. Create boilerplate
./skill-helper.sh create pdf-analyzer "Analyze PDF documents"

# 2. Edit SKILL.md
cd pdf-analyzer
# Edit SKILL.md with your instructions

# 3. Add scripts (optional)
mkdir scripts
touch scripts/analyze_pdf.py

# 4. Validate
cd ..
./skill-helper.sh validate pdf-analyzer

# 5. Test with real scenarios
# Use the skill and verify it works
```

### Sprint Planning Workflow

```bash
# 1. Decompose epics into tasks
./skill-helper.sh decompose "Epic: Payment Processing"

# 2. Export to Linear
python3 task-decomposer/scripts/analyze_task.py \
  "Payment Processing" \
  --export-linear \
  --team-id TEAM123

# 3. Label sprint issues
python3 issue-manager/scripts/issue_operations.py \
  bulk-update \
  --filter "label:ready AND priority:p0,p1" \
  --add-label "sprint-42" \
  --dry-run  # Review first!

# 4. Assign to team
python3 issue-manager/scripts/issue_operations.py \
  bulk-update \
  --filter "label:sprint-42 AND label:backend" \
  --set-assignee "@backend-team" \
  --execute
```

### Blocker Management Workflow

```bash
# 1. Report blocker
./skill-helper.sh block TEAM-123 "Waiting for design approval"

# 2. Analyze blockers across project
python3 issue-manager/scripts/analyze_blocks.py \
  --critical-path \
  --project my-project

# 3. Auto-escalate stale blocks
python3 issue-manager/scripts/analyze_blocks.py \
  --auto-escalate \
  --threshold 3d
```

## 6. Examples & Documentation

### View Examples

```bash
# Task decomposition example
cat examples/task-decomposer/example-auth-decomposition.md

# Blocker report example
cat examples/issue-manager/example-blocker-report.md
```

### Read Documentation

- **README.md** - Full repository overview
- **CONTRIBUTING.md** - Contribution guidelines
- **CHANGELOG.md** - Version history
- **Skill SKILL.md files** - Individual skill documentation
- **references/** - Detailed guides per skill

## 7. Troubleshooting

### Permission Denied on Scripts

```bash
# Make scripts executable
chmod +x skill-creator/scripts/*.py
chmod +x task-decomposer/scripts/*.py
chmod +x issue-manager/scripts/*.py
chmod +x skill-helper.sh
```

### Python Module Not Found

```bash
# Install dependencies (if validation fails)
pip install pyyaml  # For package_skill.py validation
```

### Plugin Not Found

```bash
# Check plugin is registered
/plugin list

# Re-add if needed
/plugin marketplace add yourusername/claude-skills
```

## 8. Next Steps

### Learn More

1. Read skill documentation in each skill's `SKILL.md`
2. Study examples in `examples/` directory
3. Review reference guides in `references/` subdirectories
4. Check out `CONTRIBUTING.md` for skill development

### Customize

1. Fork the repository
2. Create your own skills
3. Modify existing skills for your workflow
4. Submit PRs to share with community

### Get Help

- **Issues**: https://github.com/yourusername/claude-skills/issues
- **Discussions**: https://github.com/yourusername/claude-skills/discussions
- **Documentation**: README.md and skill docs

## Quick Reference Card

| Task | Command |
|------|---------|
| List skills | `./skill-helper.sh list` |
| Create skill | `./skill-helper.sh create <name> "<desc>"` |
| Validate skill | `./skill-helper.sh validate <name>` |
| Decompose task | `./skill-helper.sh decompose "<task>"` |
| Report blocker | `./skill-helper.sh block <issue> "<reason>"` |
| Split issue | `./skill-helper.sh split <issue>` |
| Show examples | `./skill-helper.sh examples` |
| Get help | `./skill-helper.sh help` |

---

**Ready to start?** Pick a skill and try it out! 🚀

For detailed documentation, see [README.md](README.md)
