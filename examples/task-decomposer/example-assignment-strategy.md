# Example: Intelligent Agent/Human Assignment Strategy

## Task: Build E-commerce Payment Processing System

This example demonstrates how the task decomposer automatically assigns tasks to agents vs humans based on task characteristics.

## Original Task

```
Implement complete payment processing system with Stripe integration,
including checkout flow, payment handling, refunds, and security compliance
```

## Decomposition with Assignments

### 🤖 Subtask 1: Implement Stripe API Client (AGENT)

**Assignee:** agent-bot
**Type:** Agent (Automated)
**Priority:** P0
**Estimate:** 3 hours

**Why Agent:**
- Technical implementation following Stripe docs
- Clear API specifications
- Testable with mock data
- No business decisions required

**Acceptance Criteria:**
- [ ] Initialize Stripe client with API keys
- [ ] Implement createPaymentIntent()
- [ ] Implement confirmPayment()
- [ ] Implement refundPayment()
- [ ] Error handling for all API calls
- [ ] Unit tests with 90% coverage

**Testing:**
- [ ] Mock Stripe API responses
- [ ] Test success scenarios
- [ ] Test error scenarios (declined, insufficient funds)
- [ ] Test network failures

**Expected Outputs:**
- `src/services/stripe-client.ts`
- `tests/stripe-client.test.ts`
- API documentation

---

### 🤖 Subtask 2: Build Payment Database Schema (AGENT)

**Assignee:** agent-bot
**Type:** Agent (Automated)
**Priority:** P0
**Estimate:** 2 hours

**Why Agent:**
- Standard relational database design
- Clear requirements (payments, transactions, refunds)
- Follows established patterns

**Acceptance Criteria:**
- [ ] Create payments table (id, user_id, amount, currency, status)
- [ ] Create transactions table (id, payment_id, stripe_id, timestamp)
- [ ] Create refunds table (id, payment_id, amount, reason, status)
- [ ] Add indexes for performance
- [ ] Migration with rollback

**Testing:**
- [ ] Run migration on test database
- [ ] Verify foreign key constraints
- [ ] Test rollback functionality

**Expected Outputs:**
- `migrations/004_create_payment_schema.sql`
- Schema documentation

---

### 🤖 Subtask 3: Implement Checkout Flow API (AGENT)

**Assignee:** agent-bot
**Type:** Agent (Automated)
**Priority:** P0
**Estimate:** 4 hours

**Why Agent:**
- Standard REST API implementation
- Clear input/output specifications
- Testable endpoints

**Acceptance Criteria:**
- [ ] POST /checkout/create - Create payment session
- [ ] POST /checkout/confirm - Confirm payment
- [ ] GET /checkout/status/:id - Check status
- [ ] Input validation for all endpoints
- [ ] Rate limiting

**Testing:**
- [ ] Test successful checkout flow
- [ ] Test payment failures
- [ ] Test duplicate submissions
- [ ] Test rate limiting

**Expected Outputs:**
- `src/routes/checkout.ts`
- `tests/checkout.test.ts`
- OpenAPI spec

---

### 🤖⚠️ Subtask 4: Implement Payment Security (AGENT + REVIEW)

**Assignee:** agent-bot
**Requires Human Review:** ✅ (Security team)
**Priority:** P0
**Estimate:** 4 hours

**Why Agent with Review:**
- Agent can implement standard security practices
- But security is critical and needs expert validation
- Potential for vulnerabilities

**Acceptance Criteria:**
- [ ] Encrypt sensitive payment data at rest
- [ ] Implement PCI-DSS compliant logging
- [ ] Add CSRF protection
- [ ] Implement idempotency keys
- [ ] Add webhook signature verification
- [ ] Security headers on all endpoints

**Testing:**
- [ ] Test encryption/decryption
- [ ] Test CSRF protection
- [ ] Test webhook signature validation
- [ ] Security scan with OWASP ZAP

**Expected Outputs:**
- `src/middleware/payment-security.ts`
- Security documentation
- Threat model document

**Review Checklist:**
- [ ] No hardcoded secrets
- [ ] Proper key rotation strategy
- [ ] Secure random number generation
- [ ] No sensitive data in logs
- [ ] Webhook replay attack protection

---

### 🤖⚠️ Subtask 5: Build Refund Processing (AGENT + REVIEW)

**Assignee:** agent-bot
**Requires Human Review:** ✅ (Finance team)
**Priority:** P1
**Estimate:** 3 hours

**Why Agent with Review:**
- Agent can implement refund logic
- But financial operations need human oversight
- Business rules may need validation

**Acceptance Criteria:**
- [ ] Implement full refund
- [ ] Implement partial refund
- [ ] Validate refund amount ≤ original payment
- [ ] Update database atomically
- [ ] Send refund confirmation email

**Testing:**
- [ ] Test full refund flow
- [ ] Test partial refund
- [ ] Test duplicate refund prevention
- [ ] Test refund for already-refunded payment

**Expected Outputs:**
- `src/services/refund-processor.ts`
- Refund policy documentation

**Review Checklist:**
- [ ] Refund limits are appropriate
- [ ] Double refund prevention works
- [ ] Accounting records are correct
- [ ] Tax handling is correct

---

### 👤 Subtask 6: Define Refund Policy (HUMAN)

**Assignee:** Sarah (Product Manager)
**Type:** Human (Business Decision)
**Priority:** P1
**Estimate:** 2 hours

**Why Human:**
- Business policy decision
- Requires stakeholder input
- Legal implications
- Customer satisfaction trade-offs

**Acceptance Criteria:**
- [ ] Define full refund eligibility (time window, conditions)
- [ ] Define partial refund scenarios
- [ ] Define no-refund scenarios
- [ ] Get legal review
- [ ] Get executive approval

**Expected Outputs:**
- Refund policy document
- Customer-facing refund terms
- Support team guidelines

**Stakeholders:**
- Product team
- Legal team
- Customer support
- Finance team

---

### 🤖 Subtask 7: Create Payment Webhooks Handler (AGENT)

**Assignee:** agent-bot
**Type:** Agent (Automated)
**Priority:** P0
**Estimate:** 3 hours

**Why Agent:**
- Standard webhook handling pattern
- Clear Stripe webhook documentation
- Testable with mock events

**Acceptance Criteria:**
- [ ] Handle payment_intent.succeeded
- [ ] Handle payment_intent.payment_failed
- [ ] Handle charge.refunded
- [ ] Verify webhook signatures
- [ ] Implement idempotent processing
- [ ] Update database on events

**Testing:**
- [ ] Test all webhook events
- [ ] Test signature verification
- [ ] Test idempotency
- [ ] Test concurrent webhooks

**Expected Outputs:**
- `src/webhooks/stripe-handler.ts`
- Webhook documentation

---

### 🤖 Subtask 8: Build Payment Dashboard UI (AGENT)

**Assignee:** agent-bot
**Type:** Agent (Automated)
**Priority:** P2
**Estimate:** 5 hours

**Why Agent:**
- Standard React component development
- Clear UI requirements
- Follows existing design system

**Acceptance Criteria:**
- [ ] Payment history table
- [ ] Payment details view
- [ ] Refund UI with confirmation
- [ ] Loading states
- [ ] Error handling

**Testing:**
- [ ] Unit tests for components
- [ ] Integration tests
- [ ] Accessibility tests

**Expected Outputs:**
- `src/components/PaymentDashboard.tsx`
- Component tests

---

### 👤 Subtask 9: Review UI/UX Flow (HUMAN)

**Assignee:** Mike (UX Designer)
**Type:** Human (Design Review)
**Priority:** P1
**Estimate:** 2 hours

**Why Human:**
- Subjective user experience judgment
- Design consistency evaluation
- Accessibility considerations
- Brand alignment

**Acceptance Criteria:**
- [ ] Review checkout flow
- [ ] Test on mobile devices
- [ ] Check accessibility (WCAG)
- [ ] Verify brand consistency
- [ ] Conduct usability test

**Expected Outputs:**
- UX review document
- Design improvement recommendations
- Accessibility audit results

---

### 🤖⚠️ Subtask 10: Security Audit & Penetration Testing (AGENT + REVIEW)

**Assignee:** agent-bot
**Requires Human Review:** ✅ (Security team lead)
**Priority:** P0
**Estimate:** 4 hours

**Why Agent with Review:**
- Agent can run automated security scans
- But human expert must interpret results
- Critical security implications

**Acceptance Criteria:**
- [ ] Run OWASP ZAP automated scan
- [ ] Test SQL injection vectors
- [ ] Test XSS vulnerabilities
- [ ] Test authentication bypass attempts
- [ ] Test payment amount manipulation
- [ ] Document all findings

**Testing:**
- [ ] Automated security scanning
- [ ] Manual penetration testing
- [ ] Fix HIGH and MEDIUM issues
- [ ] Document LOW issues

**Expected Outputs:**
- Security audit report
- Vulnerability fixes
- Penetration test results

**Review Checklist:**
- [ ] All HIGH risks mitigated
- [ ] MEDIUM risks have mitigation plan
- [ ] PCI-DSS compliance verified

---

### 👤 Subtask 11: Final Production Approval (HUMAN)

**Assignee:** Jane (Engineering Manager)
**Type:** Human (Final Sign-off)
**Priority:** P0
**Estimate:** 1 hour

**Why Human:**
- Final production deployment decision
- Risk assessment and mitigation
- Rollback plan review
- Stakeholder alignment

**Acceptance Criteria:**
- [ ] All tests passing (unit, integration, E2E)
- [ ] Security audit complete with no HIGH issues
- [ ] Performance benchmarks met
- [ ] Rollback plan documented
- [ ] Monitoring/alerting configured
- [ ] On-call rotation assigned

**Expected Outputs:**
- Production readiness checklist
- Go/no-go decision
- Deployment plan approval

**Stakeholders:**
- Engineering team
- Product team
- Security team
- Customer support team

---

## Assignment Summary

### By Type:
- 🤖 **Agent-only tasks:** 6 (55%)
- 🤖⚠️ **Agent with review:** 3 (27%)
- 👤 **Human-only tasks:** 2 (18%)

### By Domain:
- **Technical Implementation:** Mostly agent
- **Security:** Agent + human review
- **Business Decisions:** Human
- **Final Approvals:** Human

### Timeline Optimization:

**Parallel Track 1 (Agent):**
```
Subtasks 1, 2 → 3 → 7 → 8
Total: 17 hours agent work
```

**Parallel Track 2 (Human):**
```
Subtask 6 (2h) can start immediately
Subtasks 4, 5, 10 reviews happen after agent completion
Subtask 9 happens after subtask 8
Subtask 11 happens last
```

**Critical Path:**
```
1, 2 → 3 → 4 (review) → 7 → 5 (review) → 10 (review) → 11 (approval)
Estimated: 22 hours elapsed (with parallelization)
```

## Command to Generate This

```bash
python task-decomposer/scripts/analyze_task.py \
  "Implement complete payment processing system with Stripe integration" \
  --project backend \
  --complexity high \
  --export-linear \
  --team-id TEAM-PAYMENTS \
  --agent-user "agent-bot" \
  --human-users "backend:user-sarah,security:user-james,design:user-mike,manager:user-jane,default:user-sarah"
```

## Expected Output from CLI:

```
Analyzing task: Implement complete payment processing system with Stripe integration

Task Assignment Summary:
  🤖 Agent-assigned tasks: 6
  🤖⚠️  Agent tasks requiring human review: 3
  👤 Human-assigned tasks: 2
  🔄 Either agent or human: 0

📤 Exporting to Linear team: TEAM-PAYMENTS

Would create Linear issues with assignments:
  🤖 #1: Implement Stripe API Client
      Assignee: agent-bot
      Estimate: 3h | Priority: P0

  🤖 #2: Build Payment Database Schema
      Assignee: agent-bot
      Estimate: 2h | Priority: P0

  🤖 #3: Implement Checkout Flow API
      Assignee: agent-bot
      Estimate: 4h | Priority: P0
      Depends on: #1, #2

  🤖 #4: Implement Payment Security ⚠️ [NEEDS REVIEW]
      Assignee: agent-bot
      Estimate: 4h | Priority: P0
      Depends on: #3

  🤖 #5: Build Refund Processing ⚠️ [NEEDS REVIEW]
      Assignee: agent-bot
      Estimate: 3h | Priority: P1
      Depends on: #1

  👤 #6: Define Refund Policy
      Assignee: user-sarah
      Estimate: 2h | Priority: P1

  🤖 #7: Create Payment Webhooks Handler
      Assignee: agent-bot
      Estimate: 3h | Priority: P0
      Depends on: #3

  🤖 #8: Build Payment Dashboard UI
      Assignee: agent-bot
      Estimate: 5h | Priority: P2
      Depends on: #3

  👤 #9: Review UI/UX Flow
      Assignee: user-mike
      Estimate: 2h | Priority: P1
      Depends on: #8

  🤖 #10: Security Audit & Penetration Testing ⚠️ [NEEDS REVIEW]
      Assignee: agent-bot
      Estimate: 4h | Priority: P0
      Depends on: #4, #5, #7

  👤 #11: Final Production Approval
      Assignee: user-jane
      Estimate: 1h | Priority: P0
      Depends on: #10

💡 Assignment Rules Applied:
  • Agent tasks: Fully automated work (code, tests, refactoring)
  • Human tasks: Decisions, approvals, stakeholder work
  • Review required: Security, payments, critical systems
```

## Benefits of This Approach

### 1. **Parallel Execution**
- Agents work on multiple tasks simultaneously
- Humans focus on high-value decisions
- 2-3x faster completion vs sequential

### 2. **Clear Ownership**
- No ambiguity about who does what
- Agents know their scope
- Humans know when input needed

### 3. **Quality Assurance**
- Critical tasks get human review
- Agent work is validated
- Security is never compromised

### 4. **Scalability**
- Add more agent capacity easily
- Human bandwidth focused on decisions
- Bottlenecks clearly identified

### 5. **Audit Trail**
- Every decision tracked
- Assignment rationale documented
- Easy to review process

## Customization for Your Team

Edit detection keywords in `analyze_task.py`:

```python
# Add your team's vocabulary
human_keywords.extend([
    "customer-facing-decision",
    "pricing-strategy",
    "marketing-approval"
])

agent_keywords.extend([
    "etl-pipeline",
    "cron-job",
    "data-sync"
])

review_keywords.extend([
    "gdpr-related",
    "pii-handling",
    "audit-log"
])
```
