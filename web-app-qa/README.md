# Web App QA Skill

Interactive UI/visual QA workflows powered by Playwright MCP. Perform comprehensive quality assurance through natural language, generate test code from exploration, audit accessibility, validate visual design, and verify cross-browser compatibility.

## Features

- 🤖 **Test Generation** - Create Playwright tests from interactive exploration or requirements
- ♿ **Accessibility Audits** - WCAG 2.1 AA/AAA compliance checking with detailed reports
- 👁️ **Visual Regression** - Screenshot comparison with diff visualization and threshold-based validation
- 🌐 **Cross-Browser Testing** - Verify behavior across Chrome, Firefox, and WebKit (Safari)
- 🔍 **Interactive Exploration** - Test applications via natural language commands through Claude Code

## Prerequisites

### 1. System Requirements

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.8+ ([Download](https://www.python.org/downloads/))
- **Claude Code** ([Get started](https://claude.com/claude-code))

Verify installations:
```bash
node --version   # Should be v18.0.0 or higher
python3 --version  # Should be 3.8.0 or higher
```

### 2. Microsoft Playwright MCP Server

This skill requires the Playwright MCP server to be configured in Claude Code.

#### Installation

Add to your Claude Code MCP configuration file:

**Location:**
- **Mac/Linux:** `~/.config/claude-code/mcp_settings.json`
- **Windows:** `%APPDATA%/claude-code/mcp_settings.json`

**Configuration:**
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

**Capabilities explained:**
- `testing` - Enables assertion tools (`browser_verify_*`)
- `vision` - Enables coordinate-based interactions
- `pdf` - Enables PDF generation (optional)

**Headless mode:**
- `--headless` - Run browser without visible window (recommended for automation)
- Remove flag to see browser during testing (useful for debugging)

#### Verify Installation

After adding the configuration:

1. Restart Claude Code
2. In Claude Code, say: *"List available MCP tools"*
3. Verify you see tools starting with `mcp__playwright__`

Expected tools:
- `browser_navigate`
- `browser_click`
- `browser_snapshot`
- `browser_take_screenshot`
- And 20+ more...

### 3. Python Dependencies

For running standalone Python scripts:

```bash
# Navigate to skill directory
cd claude-skills/web-app-qa

# Install dependencies
pip3 install -r scripts/requirements.txt

# Install Playwright browsers
python3 -m playwright install
```

**Dependencies installed:**
- `playwright` - Browser automation
- `axe-core-python` - Accessibility testing
- `Pillow` - Image processing for visual regression
- `numpy` - Array operations for image comparison

## Quick Start

### Interactive QA with Claude Code

Just start a conversation in Claude Code with this skill enabled:

**Example 1: Exploratory Testing**
```
You: Navigate to https://demo.playwright.dev/todomvc and test the todo functionality

Claude will:
1. Open the page and analyze structure
2. Add todo items interactively
3. Test marking items as complete
4. Generate Playwright test code automatically
```

**Example 2: Accessibility Audit**
```
You: Run a WCAG 2.1 AA accessibility audit on https://www.example.com

Claude will:
1. Navigate and scan the page
2. Identify critical accessibility issues
3. Provide fix recommendations with code examples
4. Generate detailed HTML report
```

**Example 3: Visual Regression**
```
You: Capture baseline screenshots of https://www.example.com at desktop, tablet, and mobile sizes

Claude will:
1. Navigate to the page
2. Capture screenshots at each viewport size
3. Save baselines for future comparison
```

### Standalone Script Usage

Run QA tasks directly from the command line:

#### Test Generation
```bash
python3 scripts/generate_tests.py \
  --url https://app.example.com/login \
  --scenario "user login flow" \
  --output tests/login.spec.ts
```

#### Accessibility Audit
```bash
python3 scripts/accessibility_audit.py \
  --url https://app.example.com \
  --standard WCAG-AA \
  --output reports/accessibility.html \
  --include-screenshots
```

#### Visual Regression
```bash
# Capture baseline
python3 scripts/visual_regression.py \
  --url https://app.example.com \
  --mode baseline \
  --output baselines/ \
  --viewports desktop,tablet,mobile

# Compare against baseline
python3 scripts/visual_regression.py \
  --url https://app.example.com \
  --mode compare \
  --baseline baselines/ \
  --output diffs/ \
  --threshold 0.05
```

#### Cross-Browser Testing
```bash
python3 scripts/cross_browser.py \
  --url https://app.example.com \
  --browsers chrome,firefox,webkit \
  --output results/cross-browser.html
```

## Core Workflows

### 1. Generate Tests from Exploration

**Interactive approach:**
```
You: Navigate to https://app.example.com and explore the checkout flow

Claude will guide you through:
1. Filling form fields
2. Selecting options
3. Submitting orders
4. Generating complete test code

Output: Playwright test file (.spec.ts)
```

**Result:** Production-ready Playwright tests with proper selectors and assertions.

### 2. Accessibility Compliance

**Interactive approach:**
```
You: Audit accessibility of https://app.example.com for WCAG AA compliance

Claude will:
1. Scan for violations across 4 WCAG principles
2. Categorize by severity (Critical/Serious/Moderate/Minor)
3. Provide fix recommendations with code
4. Generate HTML report

Output: Detailed compliance report with actionable fixes
```

**Result:** Comprehensive accessibility audit identifying all WCAG violations.

### 3. Visual Regression Detection

**Interactive approach:**
```
You: Compare current screenshots of https://app.example.com against baseline

Claude will:
1. Capture new screenshots at all viewports
2. Compare pixel-by-pixel against baselines
3. Generate diff overlays highlighting changes
4. Report pass/fail for each viewport

Output: Visual diff report with comparison images
```

**Result:** Automated detection of unintended visual changes.

### 4. Cross-Browser Verification

**Interactive approach:**
```
You: Test https://app.example.com on Chrome, Firefox, and Safari

Claude will:
1. Run tests in Chromium (Chrome)
2. Run tests in Firefox
3. Run tests in WebKit (Safari)
4. Compare results and identify browser-specific issues

Output: Cross-browser compatibility matrix
```

**Result:** Verification that application works consistently across browsers.

## Directory Structure

```
web-app-qa/
├── SKILL.md                          # Main skill instructions
├── README.md                         # This file
│
├── scripts/                          # Automation scripts
│   ├── generate_tests.py            # Test code generation
│   ├── accessibility_audit.py       # WCAG compliance checker
│   ├── visual_regression.py         # Screenshot comparison
│   ├── cross_browser.py             # Multi-browser testing
│   ├── mcp_helpers.py               # MCP tool wrappers
│   ├── report_generator.py          # HTML report utilities
│   └── requirements.txt             # Python dependencies
│
├── references/                       # Documentation
│   ├── wcag-aa-guidelines.md        # WCAG 2.1 AA reference
│   ├── visual-testing-guide.md      # Visual regression guide
│   ├── selector-strategies.md       # Robust selector patterns
│   └── playwright-mcp-tools.md      # MCP tools reference (27+ tools)
│
├── templates/                        # Starter files
│   ├── playwright.config.ts         # Playwright configuration
│   ├── test-template.spec.ts        # Test boilerplate
│   ├── mcp-config.json              # MCP server config
│   ├── package.json                 # Node.js dependencies
│   └── .gitignore                   # Git ignore patterns
│
└── examples/                         # Real-world examples
    ├── exploratory-testing/         # Interactive exploration example
    ├── accessibility-audit/         # Accessibility audit example
    └── visual-validation/           # Visual regression example
```

## MCP Tools Reference

This skill uses 27+ browser automation tools provided by Microsoft's Playwright MCP server:

### Navigation
- `browser_navigate` - Navigate to URL
- `browser_navigate_back` - Go back in history

### Interaction
- `browser_click` - Click elements
- `browser_type` - Type text
- `browser_fill_form` - Fill multiple fields
- `browser_select_option` - Select dropdown options
- `browser_press_key` - Keyboard inputs
- `browser_hover` - Hover over elements
- `browser_drag` - Drag and drop

### Inspection
- `browser_snapshot` - Get accessibility tree (recommended)
- `browser_take_screenshot` - Capture screenshots
- `browser_console_messages` - View console logs
- `browser_network_requests` - Inspect network activity

### Testing (requires `testing` capability)
- `browser_verify_element_visible` - Assert element exists
- `browser_verify_text_visible` - Assert text present
- `browser_verify_value` - Assert field value
- `browser_verify_list_visible` - Assert list items
- `browser_generate_locator` - Get robust selector

**Full reference:** See `references/playwright-mcp-tools.md`

## Best Practices

### Selector Strategies

✅ **DO: Use test IDs**
```typescript
page.locator('[data-testid="submit-button"]')
```

✅ **DO: Use accessibility attributes**
```typescript
page.getByRole('button', { name: 'Submit' })
page.getByLabel('Email address')
```

❌ **DON'T: Use CSS classes**
```typescript
page.locator('.btn-primary-large-blue')  // Too brittle
```

**Full guide:** See `references/selector-strategies.md`

### Visual Testing

✅ **DO: Set appropriate thresholds**
- Static pages: 1% (0.01)
- Dynamic content: 5% (0.05)
- Heavy animations: 10% (0.10)

✅ **DO: Disable animations before capture**
```python
page.add_style_tag(content="* { animation: none !important; }")
```

❌ **DON'T: Use 0% threshold** (too strict, minor rendering differences fail)

**Full guide:** See `references/visual-testing-guide.md`

### Accessibility

✅ **DO: Check these critical items**
- [ ] All images have alt text
- [ ] Color contrast ≥ 4.5:1 for text
- [ ] All functionality works with keyboard
- [ ] Form inputs have labels
- [ ] Page has `<html lang>` attribute

**Full checklist:** See `references/wcag-aa-guidelines.md`

## Troubleshooting

### Issue: MCP tools not available

**Solution:**
1. Verify MCP configuration in `mcp_settings.json`
2. Restart Claude Code
3. Check Node.js version: `node --version` (must be 18+)

### Issue: Python scripts fail with import errors

**Solution:**
```bash
pip3 install -r scripts/requirements.txt
python3 -m playwright install
```

### Issue: Browser fails to launch

**Solution:**
```bash
# Reinstall Playwright browsers
python3 -m playwright install --force chromium firefox webkit
```

### Issue: Visual regression tests are flaky

**Solution:**
- Disable animations
- Wait for `networkidle` state
- Hide dynamic content (timestamps, avatars)
- Increase threshold

## Development

### Validating the Skill

Before distributing:

```bash
cd ../skill-creator/scripts
python3 package_skill.py ../../web-app-qa
```

### Testing the Skill

1. **Interactive testing:** Use Claude Code with the skill enabled
2. **Script testing:** Run individual Python scripts
3. **Integration testing:** Test with real applications

### Contributing

To improve this skill:

1. **Add new workflows** to `SKILL.md`
2. **Enhance scripts** in `scripts/` directory
3. **Expand documentation** in `references/`
4. **Create examples** in `examples/`
5. **Update templates** in `templates/`

## Resources

### Documentation
- **SKILL.md** - Full skill instructions and workflows
- **references/** - Comprehensive guides and references
- **examples/** - Real-world usage examples

### External Resources
- **Playwright MCP:** https://github.com/microsoft/playwright-mcp
- **Playwright Docs:** https://playwright.dev/docs/intro
- **WCAG 2.1:** https://www.w3.org/WAI/WCAG21/quickref/
- **axe DevTools:** https://www.deque.com/axe/devtools/
- **WebAIM Contrast Checker:** https://webaim.org/resources/contrastchecker/

## License

Apache-2.0

---

**Need help?** See `examples/` directory for complete workflow demonstrations.

**Want to contribute?** Open an issue or pull request in the parent repository.

**Using this skill?** Share your experience and help improve QA workflows!
