---
name: web-app-qa
description: Interactive UI/visual QA workflows using Playwright MCP for test generation, accessibility audits, visual regression, and cross-browser testing
license: Apache-2.0
---

# Web App QA

Interactive UI/visual QA workflows powered by Playwright MCP. Perform comprehensive quality assurance through natural language, generate test code from exploration, audit accessibility, validate visual design, and verify cross-browser compatibility.

## Overview

This skill enables QA engineers to:
- 🤖 **Generate Tests** - Create Playwright tests from exploration or requirements
- ♿ **Accessibility Audits** - WCAG 2.1 AA/AAA compliance checking
- 👁️ **Visual Regression** - Screenshot comparison and diff visualization
- 🌐 **Cross-Browser Testing** - Verify behavior across Chrome, Firefox, WebKit
- 🔍 **Interactive Exploration** - Test apps via natural language commands

**Powered by:** [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) - 27+ browser automation tools

## Prerequisites

### MCP Server Setup

Add Playwright MCP to your Claude Code configuration:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--caps", "testing,vision",
        "--headless"
      ]
    }
  }
}
```

**Capabilities:**
- `testing` - Enable assertion tools (`browser_verify_*`)
- `vision` - Enable coordinate-based interactions
- `pdf` - Enable PDF generation

### System Requirements

- Node.js 18+ (`node --version`)
- Python 3.8+ for scripts (`python3 --version`)
- Browsers installed (run `npx playwright install`)

## Quick Start

### Test an App Interactively

```
"Navigate to https://example.com and test the login flow"
```

Claude will:
1. Open browser using `browser_navigate`
2. Capture page structure with `browser_snapshot`
3. Guide you through testing
4. Generate test code automatically

### Run Accessibility Audit

```bash
# Interactive
"Audit accessibility of https://example.com for WCAG AA compliance"

# Or via script
python scripts/accessibility_audit.py \
  --url https://example.com \
  --standard WCAG-AA \
  --output reports/a11y-report.html
```

### Capture Visual Baseline

```
"Take screenshots of https://example.com at mobile and desktop sizes"
```

### Cross-Browser Test

```
"Test the checkout flow on Chrome, Firefox, and Safari"
```

## Core Workflows

### 1. Test Generation from Exploration

**Scenario:** You need to create automated tests but don't want to write code from scratch.

**Workflow:**

1. **Explore the application**
   ```
   "Navigate to https://app.example.com/login and show me the page structure"
   ```

2. **Interact naturally**
   ```
   "Fill the email field with test@example.com"
   "Fill the password field with Test123!"
   "Click the login button"
   "Verify I'm on the dashboard"
   ```

3. **Generate test code**
   ```
   "Generate a Playwright test for what we just did"
   ```

**Output:**
```typescript
import { test, expect } from '@playwright/test';

test('user login flow', async ({ page }) => {
  // Navigate to login page
  await page.goto('https://app.example.com/login');

  // Fill credentials
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'Test123!');

  // Submit login
  await page.click('button[type="submit"]');

  // Verify dashboard reached
  await expect(page).toHaveURL(/.*dashboard/);
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

**Using Script:**
```bash
python scripts/generate_tests.py \
  --url https://app.example.com/login \
  --scenario "user login flow" \
  --output tests/login.spec.ts
```

### 2. Accessibility Auditing

**Scenario:** Ensure your application meets WCAG 2.1 AA standards.

**Interactive Workflow:**

```
"Audit the accessibility of https://app.example.com/dashboard"
```

**What it checks:**
- ♿ **Perceivable**
  - Images have alt text
  - Color contrast meets 4.5:1 ratio
  - Text is resizable

- 🎯 **Operable**
  - All functionality via keyboard
  - No keyboard traps
  - Sufficient time limits

- 🧠 **Understandable**
  - Language declared
  - Consistent navigation
  - Input errors identified

- 💪 **Robust**
  - Valid HTML
  - Proper ARIA usage
  - Compatible with assistive tech

**Example Output:**
```
🚨 Critical Issues (3):
  - Color contrast 3.2:1 (needs 4.5:1) on .button-primary
  - Missing alt text on 5 images
  - Form inputs missing labels

⚠️ Warnings (7):
  - Heading levels skipped (h2 → h4)
  - Link text not descriptive ("click here")
  - ARIA role="button" on <div> (use <button> instead)

✅ Passed (24 checks)
```

**Detailed Script:**
```bash
python scripts/accessibility_audit.py \
  --url https://app.example.com \
  --standard WCAG-AA \
  --output reports/accessibility.html \
  --include-screenshots
```

**Output:** HTML report with:
- Executive summary
- Issue categorization (Critical/Warning/Pass)
- Element-specific violations with screenshots
- Fix recommendations with code examples
- WCAG success criteria reference

### 3. Visual Regression Testing

**Scenario:** Detect unintended UI changes between releases.

**Workflow:**

**Step 1: Capture Baseline**
```
"Take screenshots of https://app.example.com at these sizes:
 - Desktop: 1920x1080
 - Tablet: 768x1024
 - Mobile: 375x667"
```

**Step 2: After Changes**
```
"Compare current screenshots against baseline"
```

**Step 3: Review Differences**
```
"Show me the visual diff for the homepage"
```

**Using Script:**
```bash
# Capture baseline
python scripts/visual_regression.py \
  --url https://app.example.com \
  --mode baseline \
  --output baselines/

# After changes, compare
python scripts/visual_regression.py \
  --url https://app.example.com \
  --mode compare \
  --baseline baselines/ \
  --output diffs/ \
  --threshold 0.05
```

**Output:**
- Side-by-side comparison images
- Diff overlay (changed pixels highlighted)
- Pixel difference percentage
- Pass/fail based on threshold
- Change regions annotated

**DO:**
✅ Capture baselines of stable releases
✅ Set appropriate thresholds (5% for dynamic content)
✅ Test multiple viewport sizes
✅ Exclude dynamic elements (timestamps, ads)

**DON'T:**
❌ Use pixel-perfect thresholds (0%) - too brittle
❌ Compare across different browsers (font rendering varies)
❌ Forget to update baselines after intentional changes

### 4. Cross-Browser Testing

**Scenario:** Ensure consistent behavior across browsers.

**Interactive Workflow:**

```
"Test the checkout flow on Chrome, Firefox, and Safari"
```

Claude will:
1. Run test in Chrome (Chromium)
2. Repeat in Firefox
3. Repeat in WebKit (Safari engine)
4. Compare results and highlight differences

**Using Script:**
```bash
python scripts/cross_browser.py \
  --url https://app.example.com/checkout \
  --flow "add item, proceed to checkout, enter payment" \
  --browsers chrome,firefox,webkit \
  --output results/cross-browser.html
```

**Output Matrix:**

| Test Step              | Chrome | Firefox | WebKit |
|------------------------|--------|---------|--------|
| Load checkout page     | ✅ PASS | ✅ PASS  | ✅ PASS |
| Add item to cart       | ✅ PASS | ✅ PASS  | ✅ PASS |
| Enter payment info     | ✅ PASS | ⚠️ SLOW  | ✅ PASS |
| Submit order           | ✅ PASS | ✅ PASS  | ❌ FAIL |

**Browser-Specific Issues:**
- Firefox: Payment form slow to respond (2.5s vs 0.8s)
- WebKit: Order submission fails with "Network error"

## MCP Tools Reference

### Navigation
- `browser_navigate` - Go to URL
- `browser_navigate_back` - Browser back button

### Interaction
- `browser_click` - Click element by selector
- `browser_type` - Type text into field
- `browser_fill_form` - Fill multiple form fields
- `browser_select_option` - Choose dropdown option
- `browser_press_key` - Keyboard shortcuts
- `browser_hover` - Hover over element
- `browser_drag` - Drag and drop

### Inspection
- `browser_snapshot` - Get accessibility tree (recommended)
- `browser_take_screenshot` - Capture screenshot
- `browser_console_messages` - View console logs
- `browser_network_requests` - Inspect network activity

### Testing Assertions (requires `--caps testing`)
- `browser_verify_element_visible` - Assert element exists
- `browser_verify_text_visible` - Assert text present
- `browser_verify_value` - Assert field value
- `browser_verify_list_visible` - Assert list items
- `browser_generate_locator` - Get robust selector

### Advanced
- `browser_evaluate` - Run JavaScript
- `browser_wait_for` - Wait for condition
- `browser_handle_dialog` - Handle alerts/confirms
- `browser_file_upload` - Upload files
- `browser_resize` - Change viewport size

## Best Practices

### Selector Strategies

**DO:**
✅ Use accessibility tree attributes
```typescript
page.locator('[aria-label="Search"]')
page.locator('button:has-text("Submit")')
page.locator('[data-testid="login-button"]')
```

✅ Prefer semantic HTML
```typescript
page.locator('nav >> a')  // Navigation links
page.locator('main >> h1')  // Main heading
```

**DON'T:**
❌ Use brittle CSS classes
```typescript
page.locator('.btn-v2-primary-large-blue')  // Too specific, breaks often
```

❌ Use XPath for simple selectors
```typescript
page.locator('//div[@class="container"]/button[1]')  // Hard to read
```

### Test Organization

**DO:**
✅ One user flow per test
```typescript
test('complete checkout flow', async () => {
  // Single happy path
});
```

✅ Test error states separately
```typescript
test('shows error on invalid email', async () => {
  // Edge case
});
```

**DON'T:**
❌ Test everything in one giant test
```typescript
test('entire application', async () => {
  // 500 lines of test code
});
```

## Quality Checklist

Before shipping a feature:

**Functional Testing:**
- [ ] All user flows work end-to-end
- [ ] Error states handled gracefully
- [ ] Edge cases tested
- [ ] Cross-browser verified

**Accessibility:**
- [ ] WCAG 2.1 AA compliant
- [ ] Keyboard navigable
- [ ] Screen reader friendly
- [ ] Color contrast passes
- [ ] Form labels present

**Visual:**
- [ ] No unintended layout shifts
- [ ] Responsive across viewports
- [ ] Visual regression tests pass
- [ ] Loading states implemented

**Performance:**
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] No console errors

## Resources

- **MCP Tools Reference:** `references/playwright-mcp-tools.md`
- **WCAG Guidelines:** `references/wcag-aa-guidelines.md`
- **Visual Testing Guide:** `references/visual-testing-guide.md`
- **Selector Strategies:** `references/selector-strategies.md`
- **Scripts:** `scripts/generate_tests.py`, `scripts/accessibility_audit.py`, `scripts/visual_regression.py`, `scripts/cross_browser.py`
- **Examples:** `examples/exploratory-testing/`, `examples/accessibility-audit/`, `examples/visual-validation/`
- **Playwright Docs:** https://playwright.dev/docs/intro
- **Microsoft Playwright MCP:** https://github.com/microsoft/playwright-mcp
