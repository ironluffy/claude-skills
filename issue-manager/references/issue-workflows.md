# Issue Management Workflows

Comprehensive workflows for managing issues effectively across GitHub, Linear, and Jira.

## Common Workflows

### Workflow 1: Blocked Issue Management

**Scenario:** Your work is blocked by an external dependency

**Steps:**

1. **Identify and document the blocker**
   ```bash
   python scripts/issue_operations.py report-blocker \
     --issue MYTEAM-123 \
     --blocked-by "Waiting for API design approval from Platform team" \
     --category external \
     --impact high \
     --context "Cannot implement frontend until endpoints are finalized" \
     --blocking-issue PLATFORM-456 \
     --notify "@platform-lead,@project-manager"
   ```

2. **Track blocker status**
   - Daily automated checks on blocking issue
   - Receive notifications when blocker status changes
   - Escalate if blocker remains open too long

3. **Auto-escalate if stuck**
   ```bash
   # Run daily via cron
   python scripts/analyze_blocks.py --auto-escalate --threshold 3d
   ```

4. **Unblock when resolved**
   ```bash
   python scripts/issue_operations.py unblock \
     --issue MYTEAM-123 \
     --resolution "API design approved, endpoints documented" \
     --notify-assignee
   ```

**Outcome:**
- Clear visibility into what's blocking work
- Automatic escalation prevents issues from stalling
- Team stays informed of blocker status

---

### Workflow 2: Complex Issue Decomposition

**Scenario:** Issue is too large and needs to be split

**Steps:**

1. **Analyze complexity**
   ```bash
   python scripts/analyze_blocks.py \
     --issue MYTEAM-456 \
     --suggest-split
   ```

   Output:
   ```
   Complexity: HIGH
   Estimated total time: 16 hours
   Recommended split: YES
   Suggested strategy: acceptance-criteria

   Suggested breakdown into 4 subtasks:
   1. Backend API implementation (4h)
   2. Frontend UI components (4h)
   3. Database schema changes (3h)
   4. Testing and documentation (5h)
   ```

2. **Review and approve split**
   - Review suggested subtasks
   - Adjust estimates if needed
   - Confirm split strategy

3. **Execute the split**
   ```bash
   python scripts/issue_operations.py split-issue \
     --issue MYTEAM-456 \
     --num-subtasks 4 \
     --strategy acceptance-criteria \
     --preserve-labels \
     --link-parent
   ```

4. **Verify results**
   - Check that parent issue is updated
   - Verify all subtasks are created
   - Confirm relationships are correct
   - Validate metadata inheritance

**Outcome:**
- Manageable, focused subtasks
- Clear parent-child relationships
- Preserved context and metadata
- Better progress tracking

---

### Workflow 3: Bulk Triage

**Scenario:** Backlog has many untriaged issues

**Steps:**

1. **Query untriaged issues**
   ```bash
   python scripts/issue_operations.py query \
     --filter "label:needs-triage AND assignee:none" \
     --sort "created:desc" \
     --output untriaged.json
   ```

2. **Preview bulk operation**
   ```bash
   python scripts/issue_operations.py bulk-update \
     --filter "label:needs-triage" \
     --add-label "triaged" \
     --remove-label "needs-triage" \
     --set-assignee "@triage-team" \
     --dry-run
   ```

   Review output:
   ```
   [DRY RUN] Would update 23 issues
   Filter: label:needs-triage
   Add labels: triaged
   Remove labels: needs-triage
   Set assignee: @triage-team

   Matching issues: MYTEAM-101, MYTEAM-105, ...
   ```

3. **Execute if correct**
   ```bash
   python scripts/issue_operations.py bulk-update \
     --filter "label:needs-triage" \
     --add-label "triaged" \
     --remove-label "needs-triage" \
     --set-assignee "@triage-team" \
     --comment "Auto-triaged, please review and assign" \
     --execute
   ```

4. **Verify changes**
   - Spot-check a few updated issues
   - Confirm label changes
   - Verify assignees set correctly

**Outcome:**
- Backlog is organized
- Issues properly labeled
- Team can focus on triaged work

---

### Workflow 4: Sprint Planning

**Scenario:** Planning next sprint, need to organize issues

**Steps:**

1. **Identify candidates**
   ```bash
   # Find ready-to-work issues
   python scripts/issue_operations.py query \
     --filter "label:ready AND status:todo AND priority:p0,p1" \
     --sort "priority:asc,created:asc" \
     --output sprint-candidates.json
   ```

2. **Add sprint label**
   ```bash
   python scripts/issue_operations.py bulk-update \
     --filter "label:ready AND priority:p0,p1" \
     --add-label "sprint-12" \
     --execute
   ```

3. **Assign to team members**
   ```bash
   # Distribute evenly
   python scripts/issue_operations.py bulk-update \
     --filter "label:sprint-12 AND label:backend" \
     --set-assignee "@backend-team" \
     --execute

   python scripts/issue_operations.py bulk-update \
     --filter "label:sprint-12 AND label:frontend" \
     --set-assignee "@frontend-team" \
     --execute
   ```

4. **Identify dependencies**
   ```bash
   python scripts/analyze_blocks.py --critical-path --project my-project
   ```

**Outcome:**
- Sprint is organized
- Issues are assigned
- Dependencies are clear
- Team can start work

---

### Workflow 5: Release Planning

**Scenario:** Preparing for release, need to track completion

**Steps:**

1. **Create release epic**
   ```bash
   python scripts/issue_operations.py create-issue \
     --type epic \
     --title "Q1 2025 Release" \
     --labels "epic,release,p0"
   ```

2. **Link related issues to epic**
   ```bash
   # Find issues for this release
   python scripts/issue_operations.py query \
     --filter "label:release-q1-2025" \
     --output release-issues.json

   # Link each to epic (would be automated)
   for issue in $(cat release-issues.json | jq -r '.[].id'); do
     python scripts/issue_operations.py create-related \
       --source EPIC-100 \
       --type subtask \
       --existing $issue
   done
   ```

3. **Track completion**
   ```bash
   # Check status
   python scripts/issue_operations.py query \
     --filter "parent:EPIC-100 AND status:done" \
     --output completed.json

   # Calculate progress
   # Total: 20 issues
   # Done: 15 issues
   # Progress: 75%
   ```

4. **Create follow-ups**
   ```bash
   # For each completed feature, create docs task
   python scripts/issue_operations.py create-related \
     --source MYTEAM-123 \
     --type follow-up \
     --title "Documentation for feature X" \
     --labels "docs,release-notes"
   ```

**Outcome:**
- Release scope is tracked
- Progress is visible
- Follow-up work is captured

---

### Workflow 6: Handling Duplicates

**Scenario:** Multiple issues filed for same bug

**Steps:**

1. **Identify duplicates**
   ```bash
   # Search for similar issues
   python scripts/issue_operations.py query \
     --filter "text:\"login page error\" AND status:open"
   ```

2. **Review potential duplicates**
   - Check issue descriptions
   - Compare symptoms
   - Verify same root cause

3. **Merge duplicates**
   ```bash
   python scripts/issue_operations.py merge-issues \
     --issues "MYTEAM-101,MYTEAM-105,MYTEAM-108" \
     --keep MYTEAM-101 \
     --preserve-comments
   ```

4. **Notify reporters**
   - Automatic notification sent to reporters of closed issues
   - Point them to the canonical issue

**Outcome:**
- Reduced duplicate work
- Single source of truth
- All context preserved

---

### Workflow 7: Stale Issue Cleanup

**Scenario:** Old, inactive issues cluttering backlog

**Steps:**

1. **Find stale issues**
   ```bash
   python scripts/issue_operations.py query \
     --filter "updated:<30d AND status:open" \
     --output stale-issues.json
   ```

2. **Label as stale**
   ```bash
   python scripts/issue_operations.py bulk-update \
     --filter "updated:<30d AND status:open" \
     --add-label "stale" \
     --comment "This issue appears stale. Please update or it will be closed." \
     --execute
   ```

3. **Close after grace period**
   ```bash
   # After 7 more days
   python scripts/issue_operations.py bulk-update \
     --filter "label:stale AND updated:<7d" \
     --set-status "closed" \
     --add-label "auto-closed" \
     --comment "Auto-closed due to inactivity. Reopen if still relevant." \
     --execute
   ```

4. **Track metrics**
   - How many issues auto-closed
   - How many reopened
   - Adjust policy if needed

**Outcome:**
- Clean backlog
- Focus on active work
- Automated maintenance

---

## Platform-Specific Workflows

### GitHub Workflows

**Project Board Automation:**
```bash
# Move issues to "In Progress" when assigned
# (Use GitHub Actions or webhooks for real automation)

# Simulated manual version:
python scripts/issue_operations.py bulk-update \
  --filter "assignee:@me AND status:todo" \
  --set-status "in-progress"
```

**PR-Related Issue Management:**
```bash
# When PR is opened, create review follow-up
python scripts/issue_operations.py create-related \
  --source MYTEAM-123 \
  --type follow-up \
  --title "Code review for PR #456" \
  --labels "code-review"
```

### Linear Workflows

**Cycle Planning:**
```bash
# Assign issues to current cycle
python scripts/issue_operations.py bulk-update \
  --filter "label:ready AND priority:p0" \
  --set-cycle "current" \
  --execute
```

**Initiative Tracking:**
```bash
# Link issues to initiative
python scripts/issue_operations.py bulk-update \
  --filter "label:auth-revamp" \
  --set-initiative "Q1-Security" \
  --execute
```

### Jira Workflows

**Sprint Management:**
```bash
# Add issues to sprint
python scripts/issue_operations.py bulk-update \
  --filter "label:ready" \
  --set-sprint "Sprint 42" \
  --execute
```

**Epic Rollup:**
```bash
# Track epic completion
python scripts/issue_operations.py query \
  --filter "parent:EPIC-100" \
  --output epic-subtasks.json

# Calculate story points, etc.
```

---

## Best Practices

### Before Bulk Operations

1. **Always preview first**
   - Use `--dry-run` to preview changes
   - Review the list of affected issues
   - Confirm the changes are correct

2. **Test on a subset**
   - Try on 2-3 issues first
   - Verify results
   - Then scale to full set

3. **Document the reason**
   - Add `--comment` explaining bulk change
   - Helps team understand context
   - Useful for audit trail

4. **Notify affected parties**
   - Use `--notify` for stakeholders
   - Explain the change
   - Provide point of contact

### When Splitting Issues

1. **Preserve context**
   - Link to parent issue
   - Reference original requirements
   - Maintain acceptance criteria

2. **Logical boundaries**
   - Split by deliverables
   - Each subtask should be independently valuable
   - Avoid creating dependencies unnecessarily

3. **Consistent metadata**
   - Inherit relevant labels
   - Set appropriate priorities
   - Assign to right team/person

### When Reporting Blockers

1. **Be specific**
   - Clear description of what's blocking
   - Link to blocking issue if exists
   - Explain the impact

2. **Provide context**
   - Why is this blocking
   - What work is waiting
   - When do you need it resolved

3. **Suggest solutions**
   - How can we unblock
   - Alternative approaches
   - Who can help

### Automation Guidelines

1. **Monitor automation**
   - Check results regularly
   - Adjust rules as needed
   - Don't "set and forget"

2. **Escape hatches**
   - Allow manual override
   - Provide way to opt-out
   - Handle edge cases

3. **Gradual rollout**
   - Start with low-risk operations
   - Expand carefully
   - Get team buy-in

---

## Troubleshooting

### Bulk Update Affects Wrong Issues

**Problem:** Filter matched more issues than intended

**Solution:**
1. Always use `--dry-run` first
2. Refine filter query
3. Test on small subset
4. Use more specific criteria

### Split Created Too Many Subtasks

**Problem:** Issue split into too many pieces

**Solution:**
1. Review split strategy
2. Use `--num-subtasks` to limit
3. Manually merge some subtasks
4. Adjust estimation

### Blocker Not Properly Linked

**Problem:** Blocking relationship not created

**Solution:**
1. Verify blocking issue ID
2. Check permissions
3. Use platform-specific relationship syntax
4. Create manual link if needed

### Duplicate Issues Not Detected

**Problem:** Duplicates slipping through

**Solution:**
1. Improve search keywords
2. Use fuzzy matching
3. Regular manual reviews
4. Better initial triage process
