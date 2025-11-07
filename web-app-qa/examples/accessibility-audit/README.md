# Accessibility Audit Example

This example demonstrates comprehensive WCAG 2.1 AA accessibility auditing.

## Scenario

Audit a web application for accessibility compliance and generate a detailed report with fix recommendations.

## Interactive Workflow

### Step 1: Start Audit

**You say:**
```
"Run a WCAG 2.1 AA accessibility audit on https://www.example.com"
```

**Claude will:**
- Navigate to the page
- Run axe-core accessibility scan
- Analyze violations across all WCAG principles
- Generate detailed report

### Step 2: Review Critical Issues

**Example output:**
```
🚨 CRITICAL ISSUES (5):

1. Color Contrast - 4.5:1 Required
   - 3 buttons have insufficient contrast (3.2:1)
   - Located: .btn-primary class
   - Fix: Change button color to #0056b3 or darker

2. Missing Alt Text
   - 8 images lack alt attributes
   - Located: .product-image elements
   - Fix: Add descriptive alt text for each product image

3. Form Labels Missing
   - 4 input fields have no associated label
   - Located: contact form inputs
   - Fix: Add <label> elements or aria-label attributes

4. Heading Hierarchy Skipped
   - h2 directly followed by h4 (skipped h3)
   - Located: sidebar content
   - Fix: Use proper heading sequence (h2 → h3 → h4)

5. Keyboard Trap
   - Modal dialog cannot be closed with keyboard
   - Located: #promo-modal
   - Fix: Add Escape key handler and visible close button
```

### Step 3: Get Fix Recommendations

**You say:**
```
"Show me how to fix the color contrast issues"
```

**Claude will provide:**
```css
/* ❌ Current (insufficient contrast 3.2:1) */
.btn-primary {
  color: #6c757d;
  background: #fff;
}

/* ✅ Fixed (sufficient contrast 4.6:1) */
.btn-primary {
  color: #333;
  background: #fff;
}

/* Or darker background with white text (7.0:1) */
.btn-primary {
  color: #fff;
  background: #0056b3;
}
```

### Step 4: Verify Fixes

After applying fixes:

**You say:**
```
"Re-run the accessibility audit to verify the fixes"
```

**Claude will:**
- Run audit again
- Compare with previous results
- Show which issues are resolved
- Highlight remaining issues

## Automated Script Usage

```bash
# Run full audit with HTML report
python scripts/accessibility_audit.py \
  --url https://www.example.com \
  --standard WCAG-AA \
  --output reports/accessibility-audit.html \
  --include-screenshots

# Run AAA audit (stricter)
python scripts/accessibility_audit.py \
  --url https://www.example.com \
  --standard WCAG-AAA \
  --output reports/audit-aaa.html
```

**Output:** Professional HTML report with:
- Executive summary
- Issue categorization (Critical/Serious/Moderate/Minor)
- Element-specific violations with screenshots
- Fix recommendations with code examples
- WCAG success criteria references

## Real-World Example: E-commerce Site

### Initial Audit Results

```
URL: https://shop.example.com
Standard: WCAG 2.1 AA
Date: 2024-01-15

SUMMARY:
- 🚨 Critical: 12
- ⚠️  Serious: 8
- ⚡ Moderate: 15
- ℹ️  Minor: 6
- ✅ Passed: 43 checks
```

### Critical Issues Found

#### 1. Product Images Missing Alt Text
```html
<!-- ❌ Current -->
<img src="product-123.jpg">

<!-- ✅ Fixed -->
<img src="product-123.jpg" alt="Blue wireless headphones with noise cancellation">
```

#### 2. Color-Only Price Indicators
```html
<!-- ❌ Current: Red color indicates sale price -->
<span class="price-sale" style="color: red;">$29.99</span>

<!-- ✅ Fixed: Text indicator + color -->
<span class="price-sale" style="color: red;">
  <span class="sr-only">Sale price: </span>
  <strong>$29.99</strong>
  <span class="badge">SALE</span>
</span>
```

#### 3. Filter Buttons Not Keyboard Accessible
```javascript
// ❌ Current: div with onClick
<div class="filter-btn" onclick="filter('category')">Filter</div>

// ✅ Fixed: Proper button element
<button
  type="button"
  class="filter-btn"
  aria-label="Filter by category"
  onclick="filter('category')"
>
  Filter
</button>
```

#### 4. Search Form Missing Label
```html
<!-- ❌ Current -->
<input type="search" placeholder="Search products">

<!-- ✅ Fixed -->
<label for="product-search">Search products</label>
<input
  type="search"
  id="product-search"
  name="search"
  placeholder="Search products"
  aria-label="Search products"
>
```

### After Fixes - Second Audit

```
SUMMARY:
- 🚨 Critical: 0 ✅
- ⚠️  Serious: 2 (down from 8)
- ⚡ Moderate: 5 (down from 15)
- ℹ️  Minor: 3 (down from 6)
- ✅ Passed: 68 checks (up from 43)

IMPROVEMENT: 83% reduction in critical/serious issues
```

## WCAG 2.1 AA Checklist

Use this checklist during audits:

### Perceivable ♿

- [ ] All images have alt text
- [ ] Color contrast ≥ 4.5:1 for text
- [ ] Color contrast ≥ 3:1 for UI components
- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] Content can be resized to 200%
- [ ] Heading hierarchy is logical

### Operable 🎯

- [ ] All functionality via keyboard
- [ ] No keyboard traps
- [ ] Skip navigation link present
- [ ] Page has descriptive title
- [ ] Focus indicator is visible
- [ ] Links have descriptive text
- [ ] No content flashes > 3 times/second

### Understandable 🧠

- [ ] Page language declared (`<html lang="en">`)
- [ ] Navigation is consistent
- [ ] Form inputs have labels
- [ ] Error messages are clear
- [ ] Error suggestions provided

### Robust 💪

- [ ] HTML is valid
- [ ] ARIA roles are proper
- [ ] Status messages announced
- [ ] Compatible with screen readers

## Common Failures and Fixes

### Failure: Insufficient Color Contrast

**Issue:** Text/background combination doesn't meet 4.5:1 ratio

**Fix:**
```css
/* Use a contrast checker tool */
/* https://webaim.org/resources/contrastchecker/ */

/* ❌ Fails: 2.8:1 ratio */
color: #999;
background: #fff;

/* ✅ Passes: 4.6:1 ratio */
color: #595959;
background: #fff;
```

### Failure: Empty Links

**Issue:** Links with no text content

**Fix:**
```html
<!-- ❌ Fails -->
<a href="/cart">
  <i class="icon-cart"></i>
</a>

<!-- ✅ Passes -->
<a href="/cart" aria-label="Shopping cart">
  <i class="icon-cart" aria-hidden="true"></i>
  <span class="sr-only">Shopping cart</span>
</a>
```

### Failure: Form Without Fieldset

**Issue:** Related form inputs not grouped

**Fix:**
```html
<!-- ❌ Fails -->
<form>
  <input type="radio" name="shipping" value="standard"> Standard
  <input type="radio" name="shipping" value="express"> Express
</form>

<!-- ✅ Passes -->
<form>
  <fieldset>
    <legend>Shipping method</legend>
    <label>
      <input type="radio" name="shipping" value="standard">
      Standard shipping
    </label>
    <label>
      <input type="radio" name="shipping" value="express">
      Express shipping
    </label>
  </fieldset>
</form>
```

## Testing with Screen Readers

### NVDA (Windows - Free)

1. Download from https://www.nvaccess.org/
2. Navigate to your site
3. Use Tab to navigate interactive elements
4. Listen for announcements
5. Verify all content is accessible

### VoiceOver (Mac - Built-in)

1. Enable: Cmd + F5
2. Navigate: VO + Arrow keys
3. Interact: VO + Space
4. Verify all elements announced correctly

### Common Screen Reader Issues

- **Not announced:** Element missing ARIA label or role
- **Wrong announcement:** Incorrect ARIA role (e.g., div with role="button" instead of <button>)
- **Missing context:** Buttons announce "button" but not their purpose

## Resources

- WCAG 2.1 Quick Reference: https://www.w3.org/WAI/WCAG21/quickref/
- axe DevTools Extension: https://www.deque.com/axe/devtools/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- See `references/wcag-aa-guidelines.md` for detailed guidelines
