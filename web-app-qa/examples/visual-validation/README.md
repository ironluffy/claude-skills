# Visual Validation Example

This example demonstrates visual regression testing with screenshot comparison and diff visualization.

## Scenario

Capture baseline screenshots of a web application, make CSS changes, then detect visual regressions.

## Interactive Workflow

### Step 1: Capture Baseline

**You say:**
```
"Capture baseline screenshots of https://www.example.com at desktop, tablet, and mobile sizes"
```

**Claude will:**
- Navigate to the page
- Resize viewport to each size
- Capture full-page screenshots
- Save to baselines/ directory

**Output:**
```
[✓] Captured desktop (1920x1080): baselines/desktop_1920x1080.png
[✓] Captured tablet (768x1024): baselines/tablet_768x1024.png
[✓] Captured mobile (375x667): baselines/mobile_375x667.png
```

### Step 2: Make Changes

**Developer makes CSS changes:**
```css
/* Changed button styling */
.btn-primary {
  background: #007bff; /* was #0056b3 */
  padding: 12px 24px;   /* was 10px 20px */
  border-radius: 8px;   /* was 4px */
}
```

### Step 3: Compare Against Baseline

**You say:**
```
"Compare current screenshots against the baseline with 5% threshold"
```

**Claude will:**
- Capture new screenshots at same viewports
- Compare pixel-by-pixel against baselines
- Generate diff images highlighting changes
- Report pass/fail for each viewport

**Example output:**
```
VISUAL REGRESSION COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Viewport: desktop
  Difference: 2.34%
  Status: ✅ PASSED (below 5% threshold)

Viewport: tablet
  Difference: 3.12%
  Status: ✅ PASSED (below 5% threshold)

Viewport: mobile
  Difference: 8.67%
  Status: ❌ FAILED (above 5% threshold)

SUMMARY: 2 passed, 1 failed

Diff images saved to: diffs/
```

### Step 4: Review Diffs

**You say:**
```
"Show me the visual diff for mobile"
```

**Claude will:**
- Display side-by-side comparison
- Highlight changed pixels in red
- Show percentage difference

**Comparison image shows:**
```
[Baseline] [Current] [Diff]
   ↓         ↓         ↓
  Old      New      Red highlights
  image    image    show changes
```

### Step 5: Decide on Action

**If changes are intentional:**
```
"The mobile changes look good, update the baseline"
```

**If changes are bugs:**
```
"The layout broke on mobile, this needs to be fixed"
```

## Automated Script Usage

### Capture Baseline
```bash
python scripts/visual_regression.py \
  --url https://www.example.com \
  --mode baseline \
  --output baselines/ \
  --viewports desktop,tablet,mobile
```

### Compare Against Baseline
```bash
python scripts/visual_regression.py \
  --url https://www.example.com \
  --mode compare \
  --baseline baselines/ \
  --output diffs/ \
  --viewports desktop,tablet,mobile \
  --threshold 0.05
```

**Output:**
- `diffs/current/` - New screenshots
- `diffs/desktop_diff.png` - Diff overlay
- `diffs/desktop_comparison.png` - Side-by-side view
- `diffs/comparison_report.html` - Interactive HTML report

## Real-World Example: CSS Refactoring

### Scenario
Refactoring CSS from custom styles to Tailwind CSS. Need to ensure no visual changes.

### Step 1: Capture Baseline (Before Refactoring)
```bash
python scripts/visual_regression.py \
  --url http://localhost:3000 \
  --mode baseline \
  --output baselines/pre-refactor/ \
  --viewports desktop,laptop,tablet,mobile
```

### Step 2: Refactor CSS
```diff
<!-- Before: Custom CSS -->
- <button class="btn btn-primary btn-large">
+ <button class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded">
    Submit
  </button>
```

### Step 3: Compare (After Refactoring)
```bash
python scripts/visual_regression.py \
  --url http://localhost:3000 \
  --mode compare \
  --baseline baselines/pre-refactor/ \
  --output diffs/post-refactor/ \
  --threshold 0.01  # Strict: expect < 1% difference
```

### Results
```
VISUAL REGRESSION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ desktop (1920x1080)
   Difference: 0.23%
   Status: PASSED

✅ laptop (1366x768)
   Difference: 0.18%
   Status: PASSED

⚠️  tablet (768x1024)
   Difference: 1.34%
   Status: FAILED
   Issue: Button padding differs by 2px

❌ mobile (375x667)
   Difference: 4.89%
   Status: FAILED
   Issue: Text wrapping changed, button shifted down
```

### Fix Issues
```html
<!-- Fix tablet button padding -->
<button class="... py-3 px-6">  <!-- was py-2 px-4 -->

<!-- Fix mobile text wrapping -->
<button class="... text-sm sm:text-base">  <!-- Responsive text size -->
```

### Re-test
```bash
# After fixes
python scripts/visual_regression.py \
  --url http://localhost:3000 \
  --mode compare \
  --baseline baselines/pre-refactor/ \
  --output diffs/fixed/
```

```
✅ ALL VIEWPORTS PASSED
   Max difference: 0.31%
   Refactoring successful!
```

## Handling Dynamic Content

### Problem: Timestamps Change Every Run

**Page contains:**
```html
<span class="timestamp">Last updated: 2024-01-15 14:32:18</span>
```

**Solution 1: Freeze time in tests**
```javascript
// In your test setup
await page.addInitScript(() => {
  const now = new Date('2024-01-15T12:00:00Z');
  Date = class extends Date {
    constructor() { return now; }
    static now() { return now.getTime(); }
  };
});
```

**Solution 2: Hide dynamic elements**
```python
# Before screenshot
page.evaluate("""() => {
  document.querySelectorAll('.timestamp').forEach(el => {
    el.style.display = 'none';
  });
}""")
```

### Problem: Animations in Progress

**Solution: Disable animations**
```python
# Add style to disable all animations
page.add_style_tag(content="""
  *, *::before, *::after {
    animation-duration: 0s !important;
    animation-delay: 0s !important;
    transition-duration: 0s !important;
    transition-delay: 0s !important;
  }
""")
```

### Problem: External Images Load at Different Times

**Solution: Wait for all images**
```python
# Wait for all images to load
page.wait_for_function("""() => {
  const images = Array.from(document.querySelectorAll('img'));
  return images.every(img => img.complete && img.naturalHeight > 0);
}""")
```

## Best Practices

### DO ✅

1. **Capture baselines from stable releases**
   ```bash
   # Capture from production
   python visual_regression.py --url https://production.example.com --mode baseline
   ```

2. **Test multiple viewports**
   ```bash
   --viewports desktop,laptop,tablet,mobile
   ```

3. **Use appropriate thresholds**
   - Static pages: 0.01 (1%)
   - Dynamic content: 0.05 (5%)
   - Heavy animations: 0.10 (10%)

4. **Version control baselines**
   ```bash
   git add baselines/
   git commit -m "Update visual baselines for v2.0"
   ```

5. **Disable animations before capture**
   ```python
   page.add_style_tag(content="* { animation: none !important; }")
   ```

### DON'T ❌

1. **Don't use 0% threshold** - Too strict, fails on minor rendering differences
2. **Don't compare across browsers** - Font rendering differs
3. **Don't ignore all failures** - Visual regressions are real bugs
4. **Don't capture too frequently** - Baselines should be intentional

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Visual Regression Tests

on: [pull_request]

jobs:
  visual-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m playwright install chromium

      - name: Download baselines
        run: |
          # Download from artifact storage or git
          git checkout main -- baselines/

      - name: Run visual regression tests
        run: |
          python scripts/visual_regression.py \
            --url https://staging.example.com \
            --mode compare \
            --baseline baselines/ \
            --output diffs/ \
            --threshold 0.05

      - name: Upload diffs on failure
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: visual-diffs
          path: diffs/
          retention-days: 7
```

## Troubleshooting

### Issue: High False Positive Rate

**Symptoms:** Tests fail frequently with small differences

**Solutions:**
- Increase threshold: `--threshold 0.10`
- Disable animations
- Hide dynamic content (timestamps, user avatars)
- Use same browser/OS for baseline and comparison

### Issue: Different Results on Different Machines

**Cause:** Font rendering varies across OS

**Solutions:**
- Use Docker containers for consistent environment
- Run tests in CI/CD with fixed OS
- Use web fonts, not system fonts

### Issue: Flaky Tests

**Causes:**
- Images not loaded
- Animations running
- Async content loading

**Solutions:**
- Wait for `networkidle` state
- Wait for specific elements
- Add delays before screenshot

## Resources

- See `references/visual-testing-guide.md` for comprehensive guide
- See `scripts/visual_regression.py` for script documentation
- Playwright Screenshots: https://playwright.dev/docs/screenshots
- Percy Visual Testing: https://percy.io/
