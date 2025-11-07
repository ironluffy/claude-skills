# WCAG 2.1 AA Guidelines Reference

Quick reference for Web Content Accessibility Guidelines (WCAG) 2.1 Level AA compliance.

## Four Principles of WCAG

### 1. Perceivable
Information and user interface components must be presentable to users in ways they can perceive.

#### 1.1 Text Alternatives
- **1.1.1 (A)** Non-text Content: Provide text alternatives for non-text content
  - All images need alt text
  - Decorative images: `alt=""`
  - Functional images: Describe the function
  - Complex images: Provide detailed description

#### 1.2 Time-based Media
- **1.2.1 (A)** Audio-only and Video-only: Provide alternatives
- **1.2.2 (A)** Captions: Provide captions for videos
- **1.2.3 (A)** Audio Description or Media Alternative
- **1.2.4 (AA)** Captions (Live): Provide captions for live audio
- **1.2.5 (AA)** Audio Description: Provide audio descriptions for video

#### 1.3 Adaptable
- **1.3.1 (A)** Info and Relationships: Markup conveys meaning
  - Use semantic HTML (`<nav>`, `<main>`, `<article>`, etc.)
  - Proper heading hierarchy (h1 → h2 → h3)
  - Lists use `<ul>`, `<ol>`, `<li>`
  - Form labels associated with inputs
- **1.3.2 (A)** Meaningful Sequence: Logical reading order
- **1.3.3 (A)** Sensory Characteristics: Don't rely solely on shape, size, visual location, orientation, or sound
- **1.3.4 (AA)** Orientation: Content works in portrait and landscape
- **1.3.5 (AA)** Identify Input Purpose: Autocomplete attributes for user info

#### 1.4 Distinguishable
- **1.4.1 (A)** Use of Color: Don't use color alone to convey information
- **1.4.2 (A)** Audio Control: Provide controls for audio that plays > 3 seconds
- **1.4.3 (AA)** **Contrast (Minimum)**: 4.5:1 for normal text, 3:1 for large text
  - Normal text: < 18pt (or < 14pt bold)
  - Large text: ≥ 18pt (or ≥ 14pt bold)
  - UI components and graphics: 3:1
- **1.4.4 (AA)** Resize Text: Text can be resized up to 200% without loss of content or functionality
- **1.4.5 (AA)** Images of Text: Don't use images of text (unless customizable or essential)
- **1.4.10 (AA)** Reflow: Content reflows without horizontal scrolling at 320px width
- **1.4.11 (AA)** Non-text Contrast: 3:1 for UI components and graphical objects
- **1.4.12 (AA)** Text Spacing: Respect user text spacing preferences
- **1.4.13 (AA)** Content on Hover or Focus: Hoverable, dismissable, persistent

### 2. Operable
User interface components and navigation must be operable.

#### 2.1 Keyboard Accessible
- **2.1.1 (A)** Keyboard: All functionality via keyboard
- **2.1.2 (A)** No Keyboard Trap: Can navigate away from any component using keyboard
- **2.1.4 (A)** Character Key Shortcuts: Can be turned off, remapped, or only active on focus

#### 2.2 Enough Time
- **2.2.1 (A)** Timing Adjustable: Can adjust, extend, or disable time limits
- **2.2.2 (A)** Pause, Stop, Hide: Can control moving, blinking, or auto-updating content

#### 2.3 Seizures and Physical Reactions
- **2.3.1 (A)** Three Flashes or Below Threshold: No content flashes more than 3 times per second

#### 2.4 Navigable
- **2.4.1 (A)** Bypass Blocks: Skip navigation mechanism provided
- **2.4.2 (A)** Page Titled: Pages have descriptive titles
- **2.4.3 (A)** Focus Order: Logical focus order
- **2.4.4 (A)** Link Purpose (In Context): Link text describes destination
- **2.4.5 (AA)** Multiple Ways: More than one way to find pages (sitemap, search, nav)
- **2.4.6 (AA)** Headings and Labels: Headings and labels are descriptive
- **2.4.7 (AA)** Focus Visible: Keyboard focus is visible

#### 2.5 Input Modalities
- **2.5.1 (A)** Pointer Gestures: All functionality using multipoint or path-based gestures can be operated with single pointer
- **2.5.2 (A)** Pointer Cancellation: Cancel or undo actions triggered by pointer
- **2.5.3 (A)** Label in Name: Accessible name contains visible label text
- **2.5.4 (A)** Motion Actuation: Motion-based functionality has UI alternative

### 3. Understandable
Information and the operation of user interface must be understandable.

#### 3.1 Readable
- **3.1.1 (A)** Language of Page: Page language is declared (`<html lang="en">`)
- **3.1.2 (AA)** Language of Parts: Language changes are declared

#### 3.2 Predictable
- **3.2.1 (A)** On Focus: Focus doesn't trigger unexpected context changes
- **3.2.2 (A)** On Input: Input doesn't trigger unexpected context changes
- **3.2.3 (AA)** Consistent Navigation: Navigation is consistent across pages
- **3.2.4 (AA)** Consistent Identification: Components with same functionality labeled consistently

#### 3.3 Input Assistance
- **3.3.1 (A)** Error Identification: Errors are clearly identified
- **3.3.2 (A)** Labels or Instructions: Labels or instructions provided for user input
- **3.3.3 (AA)** Error Suggestion: Suggestions provided for fixing input errors
- **3.3.4 (AA)** Error Prevention (Legal, Financial, Data): Ability to review, confirm, and correct before submission

### 4. Robust
Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.

#### 4.1 Compatible
- **4.1.1 (A)** Parsing: HTML is valid (properly nested, unique IDs, etc.)
- **4.1.2 (A)** Name, Role, Value: All UI components have proper name, role, and state
- **4.1.3 (AA)** Status Messages: Status messages can be determined programmatically

## Quick Checks for QA

### Must-Have (Critical)
- [ ] All images have alt text
- [ ] Color contrast ≥ 4.5:1 for text
- [ ] All functionality works with keyboard only
- [ ] No keyboard traps
- [ ] Form inputs have associated labels
- [ ] Page has `<html lang>` attribute
- [ ] Headings follow logical hierarchy
- [ ] Links have descriptive text (not "click here")

### Important (AA Level)
- [ ] Videos have captions
- [ ] UI components have 3:1 contrast
- [ ] Focus indicator is visible
- [ ] Content works in portrait and landscape
- [ ] Can zoom to 200% without horizontal scroll
- [ ] Skip navigation link present
- [ ] Consistent navigation across site
- [ ] Error messages are clear and helpful

## Common Failures

### Color Contrast Issues
```html
<!-- ❌ BAD: Insufficient contrast -->
<button style="color: #999; background: #fff;">Submit</button>  <!-- 2.8:1 -->

<!-- ✅ GOOD: Sufficient contrast -->
<button style="color: #333; background: #fff;">Submit</button>  <!-- 12.6:1 -->
```

### Missing Alt Text
```html
<!-- ❌ BAD: No alt text -->
<img src="logo.png">

<!-- ❌ BAD: Redundant alt text -->
<img src="logo.png" alt="logo.png image">

<!-- ✅ GOOD: Descriptive alt text -->
<img src="logo.png" alt="Acme Corporation">
```

### Unlabeled Form Inputs
```html
<!-- ❌ BAD: No label -->
<input type="text" placeholder="Email">

<!-- ✅ GOOD: Explicit label -->
<label for="email">Email</label>
<input type="email" id="email" name="email" autocomplete="email">
```

### Keyboard Traps
```javascript
// ❌ BAD: Focus trap without escape
modal.addEventListener('keydown', (e) => {
  // Traps focus in modal with no way out
});

// ✅ GOOD: Escape key closes modal
modal.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});
```

### Non-semantic HTML
```html
<!-- ❌ BAD: Divs for everything -->
<div class="header">
  <div class="nav">...</div>
</div>

<!-- ✅ GOOD: Semantic HTML -->
<header>
  <nav>...</nav>
</header>
```

## Testing Tools

- **axe DevTools**: Browser extension for automated a11y testing
- **WAVE**: Web accessibility evaluation tool
- **Lighthouse**: Built into Chrome DevTools
- **NVDA/JAWS**: Screen readers for manual testing
- **Keyboard**: Test all functionality with Tab, Enter, Arrow keys, Escape

## Resources

- **Official WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/
- **WebAIM**: https://webaim.org/resources/contrastchecker/
- **a11y Project**: https://www.a11yproject.com/checklist/
- **MDN Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility
