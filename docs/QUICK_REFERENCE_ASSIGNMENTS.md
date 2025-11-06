# Quick Reference: Agent/Human Assignment

## TL;DR

🤖 **Agents** = Automated coding, testing, refactoring
👤 **Humans** = Decisions, approvals, strategy
⚠️ **Review** = Critical systems needing expert validation

## Commands

### Task Decomposition

```bash
# Preview (default - no actual Linear issues created)
python task-decomposer/scripts/analyze_task.py "Build feature" \
  --export-linear --team-id TEAM123

# Actually create Linear issues
python task-decomposer/scripts/analyze_task.py "Build feature" \
  --export-linear --team-id TEAM123 \
  --create-linear \
  --agent-user "agent-bot-id" \
  --human-users "backend:user-1,security:user-2,default:user-3"
```

### Issue Assignment

```bash
# Auto-assign based on content
python issue-manager/scripts/issue_operations.py auto-assign \
  --issue ISSUE-123 \
  --agent-user "agent-bot"

# Manual assign
python issue-manager/scripts/issue_operations.py assign \
  --issue ISSUE-456 \
  --assignee "agent-bot" \
  --assignee-type agent

# Reassign
python issue-manager/scripts/issue_operations.py reassign \
  --issue ISSUE-789 \
  --from-assignee "agent" \
  --to-assignee "human-user" \
  --reason "Needs stakeholder approval"
```

## Detection Keywords

### 🤖 Agent Keywords
```
implement, refactor, write test, build, develop, code,
automate, generate, update, script, format, lint
```

### 👤 Human Keywords
```
approve, decision, negotiate, prioritize, strategic,
legal, compliance, stakeholder, interview, sign off
```

### ⚠️ Review Keywords
```
security, authentication, payment, financial, critical,
production deploy, migration, audit, vulnerability
```

## Configuration

### Environment

```bash
# Set Linear API key
export LINEAR_API_KEY="lin_api_xxx"

# Set default agent user
export LINEAR_AGENT_USER="agent-bot-id"
```

### User Mapping File

Create `team-config.json`:
```json
{
  "agent_user": "agent-bot-id",
  "human_users": {
    "backend": "user-backend-id",
    "frontend": "user-frontend-id",
    "security": "user-security-id",
    "design": "user-design-id",
    "default": "user-manager-id"
  }
}
```

Use it:
```bash
--agent-user "$(jq -r .agent_user team-config.json)" \
--human-users "$(jq -r '.human_users | to_entries | map("\(.key):\(.value)") | join(",")' team-config.json)"
```

## Examples

### Example 1: Simple Feature

**Task:** "Add dark mode toggle"

**Assignment:**
- 🤖 Design theme colors → agent
- 🤖 Implement toggle component → agent
- 🤖 Update all components → agent
- 👤 UX review → human

### Example 2: Payment System

**Task:** "Build Stripe payment integration"

**Assignment:**
- 🤖 Implement Stripe API client → agent
- 🤖 Build checkout flow → agent
- 🤖⚠️ Implement payment security → agent + review
- 👤 Define refund policy → human
- 🤖⚠️ Security audit → agent + review
- 👤 Production approval → human

### Example 3: Database Migration

**Task:** "Migrate to PostgreSQL"

**Assignment:**
- 👤 Choose migration strategy → human
- 🤖 Write migration scripts → agent
- 🤖⚠️ Test migration on staging → agent + review
- 👤 Approve production migration → human
- 🤖⚠️ Execute migration → agent + review
- 👤 Verify and sign off → human

## Cheat Sheet

| If task involves... | Assign to | Review? |
|---------------------|-----------|---------|
| Writing code | 🤖 Agent | No |
| Writing tests | 🤖 Agent | No |
| Refactoring | 🤖 Agent | No |
| Code formatting | 🤖 Agent | No |
| Security code | 🤖 Agent | ✅ Yes |
| Authentication | 🤖 Agent | ✅ Yes |
| Payment processing | 🤖 Agent | ✅ Yes |
| Production deploy | 🤖 Agent | ✅ Yes |
| Database migration | 🤖 Agent | ✅ Yes |
| Architecture decision | 👤 Human | No |
| Business strategy | 👤 Human | No |
| Legal/compliance | 👤 Human | No |
| User research | 👤 Human | No |
| Final approval | 👤 Human | No |
| Stakeholder meeting | 👤 Human | No |

## Troubleshooting

### All tasks assigned to agent

**Problem:** Even decisions going to agent
**Solution:** Check keyword detection - add more human keywords

### Too many reviews required

**Problem:** Everything flagged for review
**Solution:** Adjust review threshold in code

### Wrong user assignments

**Problem:** Backend tasks going to frontend users
**Solution:** Check `--human-users` mapping matches labels

### Linear API errors

**Problem:** 401 Unauthorized
**Solution:** Verify LINEAR_API_KEY is correct

**Problem:** Can't find team
**Solution:** Use team ID not team name

## Tips

1. **Start with dry-run** - Always preview before creating issues
2. **Use labels** - Add labels to improve detection
3. **Review agents** - Check what agent created, even if automated
4. **Update keywords** - Customize for your team's vocabulary
5. **Track metrics** - Monitor agent vs human task completion

## Get User/Team IDs

```bash
# Run Linear integration to see your teams/users
python task-decomposer/scripts/linear_integration.py

# Output shows:
# Teams: ENG (id: team-abc-123)
# Users: Alice (id: user-def-456)
```

## Full Example Workflow

```bash
# 1. Set up environment
export LINEAR_API_KEY="lin_api_xxx"

# 2. Get team and user IDs
python task-decomposer/scripts/linear_integration.py

# 3. Decompose task (dry-run first)
python task-decomposer/scripts/analyze_task.py \
  "Implement user authentication system" \
  --project backend \
  --export-linear \
  --team-id "team-abc-123" \
  --agent-user "agent-bot-id" \
  --human-users "backend:user-alice,security:user-bob,default:user-charlie"

# 4. Review output
# Check assignment summary
# Verify agent/human split looks right

# 5. Actually create (when ready)
python task-decomposer/scripts/analyze_task.py \
  "Implement user authentication system" \
  --project backend \
  --export-linear \
  --team-id "team-abc-123" \
  --agent-user "agent-bot-id" \
  --human-users "backend:user-alice,security:user-bob,default:user-charlie" \
  --create-linear

# 6. Issues created in Linear with assignments!
```

## Learn More

- Full guide: [docs/ASSIGNMENT_RULES.md](ASSIGNMENT_RULES.md)
- Example: [examples/task-decomposer/example-assignment-strategy.md](../examples/task-decomposer/example-assignment-strategy.md)
- Integration: [task-decomposer/SKILL.md](../task-decomposer/SKILL.md)
