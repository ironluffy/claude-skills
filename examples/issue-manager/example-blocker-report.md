# Blocker Report Example

## Issue: TEAM-456 - Implement Payment Processing

### Blocker Details

**Reported**: 2025-11-06T14:30:00Z
**Status**: BLOCKED
**Category**: External Dependency
**Impact**: HIGH
**Blocked For**: 3 days

---

## What's Blocking

**Primary Blocker**: Waiting for Stripe API integration approval from Finance team

**Blocking Issue**: FINANCE-123

---

## Context

### Current Situation

Our team is ready to implement the payment processing feature using Stripe, but we need formal approval from the Finance team before we can:

1. Create the Stripe account under company credentials
2. Obtain API keys for development and production
3. Configure webhooks for payment events
4. Set up payment method capture

### Dependencies

- **Finance Team**: Must approve Stripe as payment processor
- **Legal Team**: Must review Stripe's terms of service
- **Security Team**: Must audit Stripe integration plan

### Impact Analysis

**Without Unblock:**
- Cannot complete sprint goal (payment feature is P0)
- 2 developers blocked (backend, frontend)
- Estimated revenue impact: $50K/month delayed
- Customer feature requests piling up (15+ requests)

**Work Affected:**
- TEAM-456: Payment processing (this issue)
- TEAM-457: Subscription management (depends on payment)
- TEAM-458: Invoice generation (depends on payment)
- TEAM-459: Refund workflow (depends on payment)

### Attempted Workarounds

1. ❌ **Use test mode without approval**
   - Rejected: Requires company Stripe account anyway

2. ❌ **Implement with different payment processor**
   - Rejected: Would need same approval process, plus Stripe already chosen

3. ✅ **Working on other features in parallel**
   - Currently implementing: User profile management
   - Buffer work remaining: ~2 days

---

## Timeline

### History

- **Day 0** (Nov 3): Submitted approval request to Finance
- **Day 1** (Nov 4): Finance requested additional documentation
- **Day 2** (Nov 5): Submitted additional docs, waiting for response
- **Day 3** (Nov 6 - Today): Still waiting, escalating to management

### Estimated Resolution

**Finance team ETA**: End of week (Nov 8)
**Our readiness**: Can start immediately after approval
**Implementation time**: 3 days after unblock

---

## Unblocking Strategy

### Immediate Actions (Today)

1. ✅ Escalate to Engineering Manager
2. ✅ CC'd Finance Director on approval request
3. ✅ Scheduled sync meeting with Finance for tomorrow
4. ⏳ Prepared all documentation Finance might need

### Short-term (This Week)

- Daily follow-ups with Finance team
- Prepare development environment to start immediately
- Document Stripe integration plan in detail
- Get Security team review scheduled

### Contingency Plans

**If still blocked Friday:**
- Escalate to VP level
- Consider interim solution (manual invoicing)
- Adjust sprint goals

**If blocked >1 week:**
- Reassess payment processor choice
- Consider alternative revenue model
- Notify customers of delay

---

## Notification Log

**Stakeholders Notified:**
- ✅ Engineering Manager (@eng-manager) - Nov 6, 10:00am
- ✅ Product Manager (@product-lead) - Nov 6, 10:15am
- ✅ Finance Director (@finance-director) - Nov 6, 2:30pm
- ⏳ Backend Team Lead (@backend-lead) - Automatically notified
- ⏳ Frontend Team Lead (@frontend-lead) - Automatically notified

**Escalation Chain:**
1. Engineering Manager (notified)
2. Finance Director (notified)
3. VP Engineering (if not resolved by Nov 8)

---

## Related Issues

**Blocked by this:**
- TEAM-456 (this issue)
- TEAM-457: Subscription management
- TEAM-458: Invoice generation
- TEAM-459: Refund workflow
- TEAM-460: Payment analytics dashboard

**Total team velocity impact**: 40% (5 issues blocked)

---

## Action Items

### For Our Team

- [ ] Complete Stripe integration documentation
- [ ] Prepare development environment
- [ ] Review Stripe API documentation
- [ ] Create implementation plan (ready to go)
- [ ] Work on buffer tasks until unblocked

### For Finance Team

- [ ] Review and approve Stripe usage
- [ ] Provide company credentials for Stripe account
- [ ] Approve budget for Stripe fees
- [ ] Complete any required legal review

### For Management

- [ ] Facilitate faster approval process
- [ ] Unblock Finance team if they're waiting on something
- [ ] Communicate timeline expectations to stakeholders

---

## Resolution Criteria

This blocker will be considered **RESOLVED** when:

1. ✅ Finance team provides written approval
2. ✅ Stripe account created under company credentials
3. ✅ API keys obtained (dev and prod environments)
4. ✅ Security review scheduled or completed
5. ✅ Issue status changed from BLOCKED to IN_PROGRESS

---

## Follow-up Actions After Unblock

Once unblocked, we will:

1. Create Stripe account and obtain keys (30 minutes)
2. Set up development environment (1 hour)
3. Begin implementation (3 days)
4. Daily standups to track progress
5. Close this blocker report

---

## Notes

- This is the **3rd day** blocked - threshold for escalation
- Similar approval took Finance team 4 days last quarter
- Payment feature is on critical path for Q4 goals
- Customer demand is high (15+ feature requests waiting)

---

## Automation Notes

- Auto-escalation triggered after 3 days blocked
- Daily status checks scheduled
- Notifications sent to relevant stakeholders
- Blocker visible on team dashboard

---

**Generated by**: issue-manager skill
**Platform**: Linear
**Blocker ID**: BLOCK-789
**Last Updated**: 2025-11-06T14:30:00Z
