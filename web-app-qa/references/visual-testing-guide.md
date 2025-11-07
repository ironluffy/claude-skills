# Visual Regression Testing Guide

Comprehensive guide for visual regression testing with screenshot comparison.

## What is Visual Regression Testing?

Visual regression testing captures screenshots of your application and compares them against baseline images to detect unintended visual changes.

**Use Cases:**
- Detect CSS regressions after refactoring
- Verify responsive design across viewports
- Catch layout breaks from dependency updates
- Validate theme changes
- Ensure cross-browser rendering consistency

## Core Concepts

### 1. Baseline
The "golden" screenshot representing the expected appearance. Captured when visual design is correct.

### 2. Comparison
New screenshot captured during testing, compared pixel-by-pixel against baseline.

### 3. Diff
Visual representation of differences between baseline and comparison, highlighting changed pixels.

### 4. Threshold
Acceptable percentage of pixel differences before failing a test. Accounts for minor rendering variations.

## Workflow

### Step 1: Capture Baseline
```bash
# Capture baselines at multiple viewports
python visual_regression.py \
  --url https://app.example.com \
  --mode baseline \
  --output baselines/ \
  --viewports desktop,tablet,mobile
```

**When to capture baselines:**
- After completing new features
- Before major refactoring
- When designs are approved
- For stable release versions

### Step 2: Make Changes
- Refactor CSS
- Update dependencies
- Change themes
- Modify layouts

### Step 3: Compare
```bash
# Compare current state against baseline
python visual_regression.py \
  --url https://app.example.com \
  --mode compare \
  --baseline baselines/ \
  --output diffs/ \
  --viewports desktop,tablet,mobile \
  --threshold 0.05
```

### Step 4: Review Differences
- **Pass**: Differences below threshold → No visual regressions
- **Fail**: Differences above threshold → Review changes

**If changes are intentional:**
- Update baselines by re-capturing
- Document visual changes in changelog

**If changes are unintentional:**
- Fix CSS/layout issues
- Re-run comparison tests

## Viewport Strategies

### Standard Viewports
```javascript
{
  'mobile': { width: 375, height: 667 },      // iPhone SE
  'tablet': { width: 768, height: 1024 },     // iPad
  'desktop': { width: 1920, height: 1080 },   // Full HD
  'laptop': { width: 1366, height: 768 }      // Common laptop
}
```

### Custom Viewports
```python
# Define custom viewport for testing
custom_viewport = { 'width': 1440, 'height': 900 }  # MacBook Pro
```

### Responsive Breakpoints
Test at your CSS breakpoints:
```css
/* If your CSS has these breakpoints */
@media (max-width: 640px)  { /* mobile */ }
@media (max-width: 1024px) { /* tablet */ }
@media (min-width: 1025px) { /* desktop */ }

/* Test at: 640px, 1024px, 1025px */
```

## Threshold Guidelines

### Recommended Thresholds

| Scenario | Threshold | Reason |
|----------|-----------|---------|
| Static content | 0.01 (1%) | Mostly stable, minimal anti-aliasing differences |
| Dynamic content | 0.05 (5%) | Timestamps, user-generated content, ads |
| Animation frames | 0.10 (10%) | Animations may be at different frames |
| Font rendering | 0.03 (3%) | Cross-platform font rendering varies slightly |

### Setting Thresholds
```bash
# Strict (static pages)
--threshold 0.01

# Normal (typical web apps)
--threshold 0.05

# Lenient (highly dynamic)
--threshold 0.10
```

## Handling Dynamic Content

### Problem: Timestamps
```html
<!-- Changes every test run -->
<span>Last updated: 2024-01-15 14:32:18</span>
```

**Solution 1: Freeze time**
```javascript
// Mock Date in tests
beforeAll(() => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2024-01-15 12:00:00'));
});
```

**Solution 2: Hide dynamic elements**
```python
# Hide elements before screenshot
page.evaluate("""() => {
  document.querySelector('.timestamp').style.display = 'none';
}""")
```

**Solution 3: Ignore regions**
```python
# Take screenshot excluding regions
page.screenshot(
  path='screenshot.png',
  mask=[page.locator('.timestamp'), page.locator('.ad')]
)
```

### Problem: Animations
**Solution: Disable animations**
```python
# Disable CSS animations
page.add_style_tag(content="""
  *, *::before, *::after {
    animation-duration: 0s !important;
    transition-duration: 0s !important;
  }
""")
```

### Problem: External Resources (ads, images)
**Solution: Mock or block**
```python
# Block external resources
page.route('**/*.{png,jpg,jpeg}', lambda route: route.abort())
page.route('**/ads/**', lambda route: route.abort())
```

## Best Practices

### DO ✅

#### Capture Full Page Screenshots
```python
page.screenshot(path='screenshot.png', full_page=True)
```
**Why:** Ensures entire page is tested, not just viewport.

#### Test Multiple Viewports
```python
viewports = ['mobile', 'tablet', 'desktop']
for vp in viewports:
    # Capture each viewport
```
**Why:** Responsive design bugs often appear at specific breakpoints.

#### Wait for Page Stability
```python
page.goto(url)
page.wait_for_load_state('networkidle')  # Wait for all requests
page.wait_for_selector('.content')       # Wait for key content
```
**Why:** Prevents flaky tests from content loading at different times.

#### Version Control Baselines
```bash
# Commit baselines to git
git add baselines/
git commit -m "Update visual baselines for v2.0"
```
**Why:** Track visual changes alongside code changes.

#### Name Files Descriptively
```
baselines/
  homepage_desktop_1920x1080.png
  homepage_mobile_375x667.png
  login_desktop_1920x1080.png
```
**Why:** Easy to identify which page and viewport failed.

### DON'T ❌

#### Don't Use 0% Threshold
```python
threshold = 0.0  # ❌ Too brittle
```
**Why:** Minor anti-aliasing differences will cause false failures.

#### Don't Compare Across Different Browsers
```python
# ❌ BAD: Baseline in Chrome, compare in Firefox
baseline_browser = 'chrome'
comparison_browser = 'firefox'
```
**Why:** Font rendering and anti-aliasing differ across browsers.

#### Don't Capture Too Frequently
```python
# ❌ BAD: Capture baseline on every test run
if not baseline_exists:
    capture_baseline()
```
**Why:** Baselines should be intentional snapshots of correct state.

#### Don't Ignore All Failures
```python
# ❌ BAD: Always pass
if diff_percentage > threshold:
    pass  # Whatever, probably fine
```
**Why:** Visual regressions are real bugs that affect users.

## Debugging Failures

### Step 1: Review Diff Image
Open `{viewport}_diff.png` to see highlighted changes.

### Step 2: Check Comparison Image
Open `{viewport}_comparison.png` for side-by-side view:
- Left: Baseline
- Middle: Current
- Right: Diff (changes highlighted in red)

### Step 3: Identify Root Cause

**Common causes:**

1. **CSS Changes**
   - Check recent CSS commits
   - Look for specificity conflicts
   - Verify media queries

2. **Dependency Updates**
   - Check package.json changes
   - Review UI library updates
   - Test with previous version

3. **Dynamic Content**
   - Timestamps not mocked
   - User data varies
   - External resources loading differently

4. **Environment Differences**
   - Font rendering (OS differences)
   - Screen density
   - Browser version

### Step 4: Fix or Update
- **If bug**: Fix CSS/layout, re-test
- **If intentional**: Update baseline
- **If environment**: Adjust threshold or mock

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

      - name: Run visual tests
        run: |
          python visual_regression.py \
            --url https://staging.example.com \
            --mode compare \
            --baseline baselines/ \
            --output diffs/ \
            --threshold 0.05

      - name: Upload diffs
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: visual-diffs
          path: diffs/
```

## Advanced Techniques

### Ignore Regions
```python
# Screenshot with masked regions
page.screenshot(
    path='screenshot.png',
    mask=[
        page.locator('.timestamp'),
        page.locator('.random-ad'),
        page.locator('.user-avatar')
    ]
)
```

### Component-Level Screenshots
```python
# Screenshot specific component
component = page.locator('.modal')
component.screenshot(path='modal.png')
```

### Multi-Page Flows
```python
# Test entire user flow
pages = [
    'https://app.example.com/',
    'https://app.example.com/login',
    'https://app.example.com/dashboard'
]

for url in pages:
    page.goto(url)
    page.screenshot(path=f'baseline_{url.split("/")[-1]}.png')
```

### Diff Sensitivity
```python
# Adjust diff sensitivity
from PIL import ImageChops

# More sensitive (smaller diff is flagged)
diff = ImageChops.difference(baseline, current)
diff_enhanced = diff.point(lambda x: x * 50)  # Amplify differences

# Less sensitive (only larger diffs flagged)
diff_reduced = diff.point(lambda x: x * 5)
```

## Resources

- **Playwright Screenshots**: https://playwright.dev/docs/screenshots
- **Percy (Visual Testing SaaS)**: https://percy.io/
- **BackstopJS**: https://github.com/garris/BackstopJS
- **Pixelmatch**: https://github.com/mapbox/pixelmatch
- **Looks Same**: https://github.com/gemini-testing/looks-same
