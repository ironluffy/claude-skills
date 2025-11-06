---
name: issue-manager
description: Manage GitHub and Linear issues - report blocks, modify metadata, split complex issues, create related issues with proper linking, and automate issue workflows
license: Apache-2.0
---

# Issue Manager

Comprehensive issue management for GitHub and Linear. Handle blocking issues, split complex tasks, modify metadata, create related issues, and streamline project workflows.

## Core Capabilities

### 1. Report Blocks and Blockers
- Document blocking issues with context
- Link to blocking dependencies
- Suggest unblocking strategies
- Notify stakeholders automatically

### 2. Split Complex Issues
- Break down large issues into manageable pieces
- Preserve relationships and context
- Maintain traceability
- Update parent/child links

### 3. Modify Issue Metadata
- Update labels, priorities, assignees
- Bulk operations on multiple issues
- Apply consistent taxonomy
- Enforce conventions

### 4. Create Related Issues
- Generate linked follow-up issues
- Create epic/story/task hierarchies
- Maintain relationship integrity
- Auto-populate metadata

## Quick Start

### Report a Blocker

```bash
python scripts/issue_operations.py report-blocker \
  --issue ISSUE-123 \
  --blocked-by "Waiting for API design approval" \
  --context "Backend team needs finalized endpoints" \
  --notify @backend-lead
```

Output:
- Updates issue with blocker label
- Adds comment with context
- Links to blocking issue (if exists)
- Notifies stakeholders

### Split Complex Issue

```bash
python scripts/issue_operations.py split-issue \
  --issue ISSUE-456 \
  --num-subtasks 4 \
  --preserve-labels \
  --link-parent
```

Output:
- Creates N sub-issues
- Links to original parent
- Distributes acceptance criteria
- Updates parent to track children

### Bulk Update Metadata

```bash
python scripts/issue_operations.py bulk-update \
  --filter "label:backend AND status:todo" \
  --add-label "needs-review" \
  --set-priority "p1"
```

Output:
- Finds matching issues
- Updates metadata consistently
- Logs changes
- Preserves audit trail

### Create Related Issues

```bash
python scripts/issue_operations.py create-related \
  --source ISSUE-789 \
  --type "follow-up" \
  --title "Add tests for feature X" \
  --inherit-labels
```

Output:
- Creates new issue
- Links to source issue
- Inherits relevant metadata
- Adds relationship context

## Workflows

### Workflow 1: Blocking Issue Management

**Scenario:** Your task is blocked by external dependency

**Steps:**
1. **Identify the blocker**
   ```bash
   python scripts/analyze_blocks.py --issue ISSUE-123
   ```

2. **Document the block**
   ```bash
   python scripts/issue_operations.py report-blocker \
     --issue ISSUE-123 \
     --reason "Waiting for design mockups" \
     --blocking-issue DESIGN-45 \
     --impact "Cannot start frontend work" \
     --eta "End of week"
   ```

3. **Track resolution**
   - Automatically checks if blocker is resolved
   - Updates issue status when unblocked
   - Notifies assignee to resume work

**Result:**
- Clear blocker documentation
- Stakeholder visibility
- Automatic unblock notifications
- Historical tracking

### Workflow 2: Issue Splitting

**Scenario:** Issue is too large and needs breakdown

**Steps:**
1. **Analyze complexity**
   ```bash
   python scripts/analyze_blocks.py --issue ISSUE-456 --suggest-split
   ```

2. **Review suggestions**
   - AI suggests logical split points
   - Shows proposed subtasks
   - Estimates per subtask

3. **Execute split**
   ```bash
   python scripts/issue_operations.py split-issue \
     --issue ISSUE-456 \
     --use-suggestions \
     --preserve-context
   ```

4. **Verify results**
   - Parent issue becomes epic/tracker
   - Sub-issues properly linked
   - Acceptance criteria distributed
   - Labels and metadata inherited

**Result:**
- Manageable subtasks
- Clear relationships
- Preserved context
- Better tracking

### Workflow 3: Bulk Operations

**Scenario:** Need to update many issues consistently

**Steps:**
1. **Define criteria**
   ```bash
   # Find all stale backend issues
   python scripts/issue_operations.py query \
     --filter "label:backend AND updated:<2weeks" \
     --save stale-issues.json
   ```

2. **Preview changes**
   ```bash
   python scripts/issue_operations.py bulk-update \
     --from stale-issues.json \
     --add-label "needs-triage" \
     --dry-run
   ```

3. **Apply updates**
   ```bash
   python scripts/issue_operations.py bulk-update \
     --from stale-issues.json \
     --add-label "needs-triage" \
     --comment "Triaging stale issues" \
     --execute
   ```

**Result:**
- Consistent metadata
- Bulk processing
- Audit trail
- Time saved

### Workflow 4: Creating Issue Hierarchies

**Scenario:** Build epic → story → task hierarchy

**Steps:**
1. **Create epic**
   ```bash
   python scripts/issue_operations.py create-issue \
     --type epic \
     --title "User Authentication System" \
     --labels "epic,auth,p0"
   ```

2. **Create stories under epic**
   ```bash
   python scripts/issue_operations.py create-related \
     --parent EPIC-100 \
     --type story \
     --titles "Backend API,Frontend UI,Security Audit" \
     --inherit-labels
   ```

3. **Create tasks under stories**
   ```bash
   python scripts/issue_operations.py create-related \
     --parent STORY-101 \
     --type task \
     --use-decomposition task-breakdown.json
   ```

**Result:**
- Proper hierarchy (epic → story → task)
- All relationships linked
- Consistent metadata
- Easy tracking

## Operations Reference

### Report Blocker

Document what's blocking progress:

```bash
python scripts/issue_operations.py report-blocker \
  --issue ISSUE-123 \
  --blocked-by "Description or ISSUE-ID" \
  --category "external|technical|resource" \
  --impact "high|medium|low" \
  --context "Additional details" \
  --notify "@user1,@user2"
```

**Adds to issue:**
- `blocked` label
- Blocker comment with context
- Link to blocking issue
- Impact assessment
- Notification to stakeholders

### Unblock Issue

Mark blocker as resolved:

```bash
python scripts/issue_operations.py unblock \
  --issue ISSUE-123 \
  --resolution "Design mockups completed" \
  --notify-assignee
```

**Updates issue:**
- Removes `blocked` label
- Adds resolution comment
- Notifies assignee to resume
- Logs unblock time

### Split Issue

Break large issue into smaller pieces:

```bash
python scripts/issue_operations.py split-issue \
  --issue ISSUE-456 \
  --num-subtasks 4 \
  --strategy "acceptance-criteria|functionality|layer" \
  --preserve-labels \
  --inherit-metadata \
  --link-parent
```

**Creates:**
- N sub-issues with descriptive titles
- Parent-child relationships
- Distributed acceptance criteria
- Inherited labels and metadata

### Merge Issues

Combine duplicate or related issues:

```bash
python scripts/issue_operations.py merge-issues \
  --issues "ISSUE-101,ISSUE-102,ISSUE-103" \
  --keep ISSUE-101 \
  --close-others \
  --preserve-comments
```

**Result:**
- Primary issue kept open
- Others closed as duplicates
- Comments merged
- Links updated

### Bulk Update

Update multiple issues at once:

```bash
python scripts/issue_operations.py bulk-update \
  --filter "label:needs-triage AND assignee:none" \
  --set-assignee "@triageteam" \
  --add-label "triaged" \
  --remove-label "needs-triage" \
  --dry-run  # Preview first
```

**Supports:**
- Label operations (add, remove, set)
- Assignee changes
- Priority updates
- Status transitions
- Custom field updates

### Create Related Issue

Generate linked follow-up issues:

```bash
python scripts/issue_operations.py create-related \
  --source ISSUE-789 \
  --type "follow-up|prerequisite|related" \
  --title "Issue title" \
  --description "Description" \
  --relationship "blocks|blocked-by|relates-to" \
  --inherit-labels
```

**Relationships:**
- `follow-up` - Work after source completes
- `prerequisite` - Must complete before source
- `related` - Connected but independent
- `duplicate` - Same as source
- `subtask` - Part of source

### Query Issues

Find issues matching criteria:

```bash
python scripts/issue_operations.py query \
  --filter "label:backend AND status:in-progress" \
  --sort "updated:desc" \
  --limit 50 \
  --output issues.json
```

**Filter syntax:**
```
label:NAME              Has label
status:STATE            In state (todo, in-progress, done, etc.)
assignee:USER           Assigned to user
priority:LEVEL          Has priority (p0, p1, p2)
updated:<TIMEFRAME      Updated before timeframe (1d, 1w, 1m)
updated:>TIMEFRAME      Updated after timeframe
created:<TIMEFRAME      Created before
created:>TIMEFRAME      Created after
has:comments            Has comments
has:subtasks            Has subtasks
is:blocked              Is blocked
is:blocking             Is blocking others
```

## Block Analysis

### Identify Blockers

Analyze blocking issues:

```bash
python scripts/analyze_blocks.py --issue ISSUE-123
```

**Reports:**
- Direct blockers
- Transitive dependencies
- Critical path
- Unblocking suggestions

### Blocker Categories

**External Blockers:**
- Waiting for design
- Waiting for stakeholder decision
- Third-party dependency
- Infrastructure not ready

**Technical Blockers:**
- API not implemented
- Database migration pending
- Security review needed
- Performance bottleneck

**Resource Blockers:**
- Waiting for assignment
- Missing expertise
- Competing priorities
- Capacity constraints

### Unblocking Strategies

For each blocker type, suggest:

**External → Escalate**
```bash
# Notify stakeholders
python scripts/issue_operations.py escalate-blocker \
  --issue ISSUE-123 \
  --to "@manager" \
  --reason "Blocked for 3 days"
```

**Technical → Create Prerequisite**
```bash
# Create blocking issue
python scripts/issue_operations.py create-related \
  --source ISSUE-123 \
  --type prerequisite \
  --title "Implement required API" \
  --priority p0
```

**Resource → Reassign**
```bash
# Find alternative assignee
python scripts/issue_operations.py suggest-assignee \
  --issue ISSUE-123 \
  --skill-required "backend,python"
```

## Splitting Strategies

### Strategy 1: By Acceptance Criteria

Split based on acceptance criteria:

```bash
python scripts/issue_operations.py split-issue \
  --issue ISSUE-456 \
  --strategy acceptance-criteria
```

**Example:**
```
Original: "Implement user authentication"
Criteria:
- [ ] User can register
- [ ] User can login
- [ ] User can reset password
- [ ] Session management

Subtasks:
→ ISSUE-457: Implement user registration
→ ISSUE-458: Implement user login
→ ISSUE-459: Implement password reset
→ ISSUE-460: Implement session management
```

### Strategy 2: By Functionality

Split by distinct features:

```bash
python scripts/issue_operations.py split-issue \
  --issue ISSUE-456 \
  --strategy functionality
```

**Example:**
```
Original: "Build dashboard"

Subtasks:
→ ISSUE-461: Dashboard data aggregation
→ ISSUE-462: Dashboard UI components
→ ISSUE-463: Dashboard charts and visualization
→ ISSUE-464: Dashboard filtering and search
```

### Strategy 3: By Layer/Component

Split by technical layer:

```bash
python scripts/issue_operations.py split-issue \
  --issue ISSUE-456 \
  --strategy layer
```

**Example:**
```
Original: "Add export feature"

Subtasks:
→ ISSUE-465: Backend export API
→ ISSUE-466: Frontend export UI
→ ISSUE-467: Export file generation
→ ISSUE-468: Export integration tests
```

## Best Practices

### Blocker Documentation

✅ **DO**: Be specific
```
Blocked by: Waiting for API design approval
Context: Backend team needs final endpoint specifications
Impact: Cannot start implementation until endpoints are defined
ETA: Design review scheduled for Friday
```

❌ **DON'T**: Be vague
```
Blocked by: stuff
Context: waiting
```

### Issue Splitting

✅ **DO**: Preserve context
```
Parent: "Implement authentication system"
Child 1: "Implement backend JWT service"
  - Links to parent
  - Inherits labels (auth, backend, p0)
  - References parent acceptance criteria
```

❌ **DON'T**: Lose connections
```
Child 1: "Do some auth stuff"
  - No parent link
  - No context
  - Lost metadata
```

### Bulk Operations

✅ **DO**: Preview first
```bash
# Always use --dry-run first
python scripts/issue_operations.py bulk-update \
  --filter "..." \
  --add-label "new-label" \
  --dry-run

# Review output, then execute
python scripts/issue_operations.py bulk-update \
  --filter "..." \
  --add-label "new-label" \
  --execute
```

❌ **DON'T**: Execute blindly
```bash
# Risky - no preview
python scripts/issue_operations.py bulk-update \
  --filter "..." \
  --execute
```

## Integration

### Linear Integration

Authenticate with Linear:
```bash
export LINEAR_API_KEY="your-api-key"
python scripts/issue_operations.py --platform linear report-blocker ...
```

### GitHub Integration

Authenticate with GitHub:
```bash
export GITHUB_TOKEN="your-token"
python scripts/issue_operations.py --platform github report-blocker ...
```

### Jira Integration

Authenticate with Jira:
```bash
export JIRA_API_TOKEN="your-token"
export JIRA_DOMAIN="your-domain.atlassian.net"
python scripts/issue_operations.py --platform jira report-blocker ...
```

## Automation Examples

### Auto-label Stale Issues

```bash
# Daily cron job
0 9 * * * python scripts/issue_operations.py bulk-update \
  --filter "updated:<7d AND is:open" \
  --add-label "stale" \
  --comment "Issue appears stale. Please update or close."
```

### Auto-escalate Blocked Issues

```bash
# Daily cron job
0 10 * * * python scripts/analyze_blocks.py --auto-escalate \
  --threshold "3d" \
  --notify "@managers"
```

### Auto-create Follow-ups

```bash
# When issue is closed, create documentation task
python scripts/issue_operations.py create-related \
  --source ISSUE-123 \
  --type follow-up \
  --template documentation \
  --auto-assign "@docs-team"
```

## Resources

- Issue workflows guide: `references/issue-workflows.md`
- Platform API reference: `references/platform-apis.md`
- Automation examples: `references/automation-examples.md`
- Scripts: `scripts/issue_operations.py`, `scripts/analyze_blocks.py`

## Quality Checklist

Before bulk operations:

- [ ] Verified filter matches intended issues
- [ ] Ran with `--dry-run` to preview
- [ ] Reviewed preview output
- [ ] Confirmed changes are correct
- [ ] Have backup/undo plan
- [ ] Notified team if large-scale change
- [ ] Documented reason for bulk change
- [ ] Tested on small subset first

Before splitting issues:

- [ ] Confirmed issue is too large
- [ ] Chose appropriate split strategy
- [ ] Reviewed suggested subtasks
- [ ] Verified relationships will be preserved
- [ ] Confirmed metadata inheritance
- [ ] Checked assignee assignments
- [ ] Validated acceptance criteria distribution

Before reporting blockers:

- [ ] Clearly identified what's blocking
- [ ] Provided relevant context
- [ ] Assessed impact accurately
- [ ] Linked to blocking issue if exists
- [ ] Notified appropriate stakeholders
- [ ] Documented expected resolution time
