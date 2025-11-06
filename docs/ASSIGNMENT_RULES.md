# Agent vs Human Assignment Rules

## Overview

The Claude Skills repository includes intelligent assignment logic that automatically determines whether tasks should be assigned to AI agents or humans based on task characteristics.

## Assignment Types

### 🤖 Agent Tasks (Fully Automated)

Tasks that can be completed autonomously by AI agents:

**Characteristics:**
- Clearly defined technical specifications
- Deterministic outcomes
- Testable with automated checks
- No human judgment required
- Repeatable patterns

**Examples:**
- Implementing functions from specifications
- Writing unit tests
- Refactoring code
- Generating documentation
- Running linters/formatters
- Creating boilerplate code
- Database migrations
- API endpoint implementation
- Test coverage improvements

**Keywords Detected:**
```
implement, write test, create unit test, refactor, update,
build, develop, code, script, automate, generate,
format, lint, type check, documentation code
```

### 👤 Human Tasks (Requires Human Intervention)

Tasks requiring human judgment, decision-making, or stakeholder interaction:

**Characteristics:**
- Subjective decisions
- Business strategy
- Stakeholder management
- Legal/compliance considerations
- User research insights
- Final approvals

**Examples:**
- Architecture decisions
- Prioritizing features
- Stakeholder negotiations
- Legal compliance review
- User research interpretation
- Strategic planning
- Budget allocation
- Final production sign-offs

**Keywords Detected:**
```
approve, decision, review stakeholder, negotiate,
business decision, prioritize, strategic, legal,
compliance, privacy policy, user research, interview,
stakeholder, sign off, final approval
```

### 🤖⚠️ Agent Tasks Requiring Human Review

Tasks agents can complete but need human validation:

**Characteristics:**
- High-risk areas
- Security-sensitive
- Financial systems
- Critical infrastructure
- Potential for significant impact

**Examples:**
- Authentication systems
- Payment processing
- Security audits
- Production deployments
- Database migrations
- API key management
- User data handling

**Keywords Detected:**
```
security, audit, penetration test, vulnerability,
authentication, payment, financial, billing,
critical, production deploy, migration
```

### 🔄 Either Agent or Human

Tasks that can be done by either:

**Characteristics:**
- Flexible approach
- Multiple valid solutions
- Context-dependent

**Examples:**
- Research tasks
- Design explorations
- Planning phases
- Documentation review

**Labels Detected:**
```
planning, research, design
```

## Detection Algorithm

The system uses a multi-layered detection approach:

```python
def detect_assignee_type(title, description, labels):
    # 1. Check for human-required keywords
    if contains(human_keywords):
        return HUMAN

    # 2. Check for security/critical keywords
    if contains(review_keywords):
        if contains(agent_keywords):
            return AGENT + REQUIRES_REVIEW
        else:
            return HUMAN

    # 3. Check for agent-friendly keywords
    if contains(agent_keywords):
        return AGENT

    # 4. Check labels
    if "security" in labels:
        return AGENT + REQUIRES_REVIEW
    if "planning" in labels:
        return EITHER

    # 5. Default to agent
    return AGENT
```

## Usage Examples

### Task Decomposition with Auto-Assignment

```bash
# Basic task decomposition with assignment detection
python task-decomposer/scripts/analyze_task.py \
  "Implement user authentication system"

# Output shows:
# 🤖 Subtask 1: Implement password hashing (agent)
# 🤖⚠️ Subtask 2: Security audit (agent, needs review)
# 👤 Subtask 3: Approve deployment (human)
```

### Export to Linear with Assignments

```bash
# Export with agent and human user mappings
python task-decomposer/scripts/analyze_task.py \
  "Build payment processing" \
  --export-linear \
  --team-id TEAM123 \
  --agent-user "agent-bot" \
  --human-users "backend:user-abc123,security:user-def456,default:user-xyz789"

# Result:
# - Agent tasks assigned to: agent-bot
# - Backend tasks needing human → user-abc123
# - Security tasks → user-def456
# - Other human tasks → user-xyz789
```

### Issue Management with Auto-Assignment

```bash
# Manually assign to agent
python issue-manager/scripts/issue_operations.py assign \
  --issue ISSUE-123 \
  --assignee "agent-bot" \
  --assignee-type agent

# Auto-detect and assign
python issue-manager/scripts/issue_operations.py auto-assign \
  --issue ISSUE-456 \
  --agent-user "agent-bot" \
  --human-users "default:user-xyz789"

# Reassign from agent to human
python issue-manager/scripts/issue_operations.py reassign \
  --issue ISSUE-789 \
  --from-assignee "agent-bot" \
  --to-assignee "user-xyz789" \
  --reason "Requires stakeholder approval"
```

## Configuration

### Setting Up Agent User

```bash
# Linear
export LINEAR_AGENT_USER="agent-bot-id"

# GitHub
export GITHUB_AGENT_USER="agent-bot"
```

### Mapping Human Users

Create a mapping file `team-config.json`:

```json
{
  "agent_user": "agent-bot",
  "human_users": {
    "backend": "user-backend-lead",
    "frontend": "user-frontend-lead",
    "security": "user-security-lead",
    "devops": "user-devops-lead",
    "default": "user-project-manager"
  }
}
```

Use in scripts:
```bash
--agent-user "$(jq -r .agent_user team-config.json)" \
--human-users "$(jq -r '.human_users | to_entries | map("\(.key):\(.value)") | join(",")' team-config.json)"
```

## Best Practices

### 1. Always Review Agent Assignments

Even automated tasks should be reviewed, especially:
- First-time implementations
- Complex algorithms
- Security-related code

### 2. Set Clear Human Ownership

Ensure human tasks have specific owners:
```bash
--human-users "security:alice@company.com,compliance:bob@company.com"
```

### 3. Use Labels Effectively

Add labels to improve detection:
- `security` → triggers review requirement
- `planning` → allows either agent or human
- `critical` → may trigger human assignment

### 4. Review Auto-Assignments

Check the assignment summary before creating issues:
```
Task Assignment Summary:
  🤖 Agent-assigned tasks: 8
  🤖⚠️  Agent tasks requiring human review: 3
  👤 Human-assigned tasks: 2
  🔄 Either agent or human: 1
```

### 5. Customize Detection Keywords

Modify `detect_assignee_type()` for your team's vocabulary:
```python
# Add custom keywords
human_keywords.extend(["customer-facing", "ux-decision"])
agent_keywords.extend(["data-pipeline", "etl"])
```

## Integration with Linear

### Linear API Configuration

```bash
# Set up Linear MCP
export LINEAR_API_KEY="lin_api_xxx"

# Or use Linear MCP server
claude mcp add linear npx @linear/mcp
```

### Creating Issues with Assignments

```python
import requests

def create_linear_issue_with_assignment(issue_data):
    headers = {
        "Authorization": f"Bearer {LINEAR_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "title": issue_data["title"],
        "description": issue_data["description"],
        "teamId": issue_data["team_id"],
        "assigneeId": issue_data["assignee_id"],
        "priority": issue_data["priority"],
        "labels": issue_data["labels"]
    }

    # Add custom field for assignment type
    if issue_data.get("assignee_type") == "agent":
        payload["customFields"] = {
            "assignee_type": "agent"
        }

    response = requests.post(
        "https://api.linear.app/graphql",
        json={"query": CREATE_ISSUE_MUTATION, "variables": payload},
        headers=headers
    )

    return response.json()
```

## Monitoring and Analytics

### Track Assignment Effectiveness

```bash
# Query agent-assigned issues
python issue-manager/scripts/issue_operations.py query \
  --filter "assignee:agent-bot status:done"

# Measure completion rates
python issue-manager/scripts/issue_operations.py query \
  --filter "label:agent-task" \
  --output agent-metrics.json

# Compare agent vs human velocity
```

### Review Patterns

Periodically review:
- Which tasks agents complete successfully
- Which tasks require human intervention
- False positives (agent assigned but needed human)
- False negatives (human assigned but agent could do)

## Customization

### Override Auto-Detection

```python
# In task decomposition
subtask.assignee_type = AssigneeType.HUMAN  # Force human
subtask.assignee = "specific-user-id"       # Explicit assignment
subtask.requires_human_review = True        # Add review requirement
```

### Custom Detection Logic

Create custom detection for your domain:

```python
def detect_ml_task_assignee(title, description):
    """Custom detection for ML tasks."""
    ml_human_tasks = [
        "model selection", "hyperparameter tuning",
        "feature engineering strategy", "dataset curation"
    ]

    ml_agent_tasks = [
        "data preprocessing", "train model",
        "run experiments", "generate metrics"
    ]

    # Your custom logic
    pass
```

## Troubleshooting

### Issue: All tasks assigned to agent

**Solution:** Check keyword detection is working:
```bash
# Add more human keywords or adjust thresholds
# Review task titles for clarity
```

### Issue: Too many human assignments

**Solution:** Be more specific about agent capabilities:
```bash
# Expand agent_keywords list
# Use explicit assignee when possible
```

### Issue: Review requirements too aggressive

**Solution:** Adjust review detection:
```python
# Only trigger review for HIGH risk
if risk_level == "HIGH":
    requires_human_review = True
```

## Resources

- Detection algorithm: `task-decomposer/scripts/analyze_task.py:231`
- Issue assignment: `issue-manager/scripts/issue_operations.py:83`
- Examples: `examples/task-decomposer/example-assignment-strategy.md`
- Tests: `tests/test_assignment_detection.py`
