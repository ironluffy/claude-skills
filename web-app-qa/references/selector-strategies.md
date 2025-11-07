# Selector Strategies for Robust Tests

Guide to choosing selectors that create maintainable, reliable test automation.

## Selector Hierarchy (Best to Worst)

### 1. Test IDs (Best) 🥇
**Pattern:** `[data-testid="value"]`

```html
<button data-testid="submit-login">Login</button>
```

```typescript
// Playwright
await page.click('[data-testid="submit-login"]');
await page.getByTestId('submit-login').click();
```

**Pros:**
- ✅ Explicitly for testing - won't break with UI changes
- ✅ Unique and stable
- ✅ Clear intent to developers
- ✅ Works across frameworks

**Cons:**
- ❌ Requires adding attributes to markup
- ❌ Extra work for developers

**When to use:** Always, for critical user flows.

### 2. Accessibility Attributes 🥈
**Pattern:** `[aria-label]`, `[aria-labelledby]`, `role`

```html
<button aria-label="Close modal">×</button>
<input aria-label="Search products" type="search">
<nav role="navigation"></nav>
```

```typescript
// Playwright
await page.click('[aria-label="Close modal"]');
await page.getByRole('button', { name: 'Close modal' }).click();
await page.getByLabel('Search products').fill('laptop');
```

**Pros:**
- ✅ Semantic and accessible
- ✅ Mirrors how screen readers interact
- ✅ Encourages accessible design
- ✅ Relatively stable

**Cons:**
- ❌ May change with accessibility improvements
- ❌ Not always unique

**When to use:** Second choice when test IDs not available.

### 3. Semantic HTML 🥉
**Pattern:** `<button>`, `<nav>`, `<main>`, etc.

```html
<nav>
  <a href="/home">Home</a>
  <a href="/about">About</a>
</nav>
```

```typescript
// Playwright
await page.locator('nav >> a[href="/home"]').click();
await page.getByRole('navigation').getByText('Home').click();
```

**Pros:**
- ✅ Semantic and accessible
- ✅ No extra markup needed
- ✅ Encourages proper HTML structure

**Cons:**
- ❌ May not be unique enough
- ❌ Can change with refactoring

**When to use:** For general page structure navigation.

### 4. Name/ID Attributes
**Pattern:** `[name="value"]`, `#id`

```html
<input type="email" name="email" id="email-input">
<form name="login-form"></form>
```

```typescript
// Playwright
await page.fill('[name="email"]', 'test@example.com');
await page.fill('#email-input', 'test@example.com');
```

**Pros:**
- ✅ Usually stable for form fields
- ✅ Unique (IDs must be unique)
- ✅ Semantic purpose

**Cons:**
- ❌ IDs may be auto-generated (e.g., `input-1234`)
- ❌ Can change with refactoring

**When to use:** Form fields and unique page elements.

### 5. Visible Text
**Pattern:** `:has-text()`, `getByText()`

```html
<button>Submit Order</button>
<a href="/products">View Products</a>
```

```typescript
// Playwright
await page.click('button:has-text("Submit Order")');
await page.getByText('Submit Order').click();
await page.getByRole('button', { name: 'Submit Order' }).click();
```

**Pros:**
- ✅ Reads like natural language
- ✅ Easy to write
- ✅ No extra markup

**Cons:**
- ❌ Breaks with copy changes
- ❌ Breaks with i18n
- ❌ Not unique (multiple "Submit" buttons)

**When to use:** Quick tests, unique text, when combined with other selectors.

### 6. CSS Classes (Avoid) ⚠️
**Pattern:** `.class-name`

```html
<button class="btn btn-primary btn-large submit-button">Submit</button>
```

```typescript
// ❌ BAD: Brittle, can break with styling changes
await page.click('.btn-primary');
await page.click('.submit-button');

// ✅ BETTER: Use test ID or role
await page.click('[data-testid="submit-button"]');
```

**Pros:**
- ✅ Easy to select
- ✅ Often already in markup

**Cons:**
- ❌ Changes frequently with styling
- ❌ Not unique
- ❌ Couples tests to CSS implementation
- ❌ Utility classes change often (Tailwind, Bootstrap)

**When to use:** Last resort, prefer combining with context.

### 7. XPath (Avoid) 🚫
**Pattern:** `//div[@class="container"]//button[1]`

```typescript
// ❌ BAD: Hard to read, brittle, slow
await page.click('//div[@class="header"]//nav//a[contains(text(), "Home")]');

// ✅ BETTER: Use CSS or Playwright locators
await page.locator('header nav >> a:has-text("Home")').click();
```

**Pros:**
- ✅ Can traverse DOM in complex ways
- ✅ Powerful for XML

**Cons:**
- ❌ Hard to read and maintain
- ❌ Slower than CSS selectors
- ❌ Brittle (breaks with DOM structure changes)
- ❌ Less familiar to web developers

**When to use:** Almost never. Use CSS or Playwright locators instead.

## Combining Selectors (Chaining)

### Narrow by Context
```typescript
// ❌ BAD: Ambiguous
await page.click('button');  // Which button?

// ✅ GOOD: Specific context
await page.locator('form[name="login"] >> button[type="submit"]').click();
await page.locator('.modal-dialog >> [aria-label="Close"]').click();
```

### Playwright Chaining
```typescript
// Chain locators for specificity
await page
  .getByRole('navigation')
  .getByRole('link', { name: 'Products' })
  .click();

// Filter by text
await page
  .getByRole('listitem')
  .filter({ hasText: 'Premium' })
  .getByRole('button', { name: 'Subscribe' })
  .click();
```

## Framework-Specific Patterns

### React Testing Library
```javascript
// Follows accessibility-first approach
import { render, screen } from '@testing-library/react';

// ✅ By role (best)
screen.getByRole('button', { name: /submit/i });

// ✅ By label text
screen.getByLabelText('Email address');

// ✅ By text content
screen.getByText('Welcome back!');

// ❌ Avoid test IDs in React Testing Library (use roles instead)
screen.getByTestId('submit-button');  // Last resort
```

### Playwright
```typescript
// Playwright locators (recommended)
page.getByRole('button', { name: 'Submit' });
page.getByText('Welcome back!');
page.getByLabel('Email address');
page.getByPlaceholder('Enter email');
page.getByTestId('submit-button');

// CSS selectors (fallback)
page.locator('button[type="submit"]');
page.locator('[data-testid="submit-button"]');
```

### Cypress
```javascript
// Cypress commands
cy.get('[data-testid="submit-button"]').click();
cy.get('button').contains('Submit').click();
cy.get('input[name="email"]').type('test@example.com');
```

## Real-World Examples

### Example 1: Login Form

```html
<form name="login-form" aria-label="User login">
  <label for="email">Email</label>
  <input
    type="email"
    id="email"
    name="email"
    data-testid="login-email"
    aria-label="Email address"
  >

  <label for="password">Password</label>
  <input
    type="password"
    id="password"
    name="password"
    data-testid="login-password"
    aria-label="Password"
  >

  <button
    type="submit"
    data-testid="login-submit"
    aria-label="Login to your account"
  >
    Login
  </button>
</form>
```

**Selector choices (best to worst):**
```typescript
// 🥇 Best: Test IDs
await page.fill('[data-testid="login-email"]', 'test@example.com');
await page.fill('[data-testid="login-password"]', 'password123');
await page.click('[data-testid="login-submit"]');

// 🥈 Good: Accessibility attributes
await page.getByLabel('Email address').fill('test@example.com');
await page.getByLabel('Password').fill('password123');
await page.getByRole('button', { name: 'Login to your account' }).click();

// 🥉 Okay: Name attributes with context
await page.locator('form[name="login-form"] >> [name="email"]').fill('test@example.com');
await page.locator('form[name="login-form"] >> [name="password"]').fill('password123');
await page.locator('form[name="login-form"] >> button[type="submit"]').click();

// ⚠️ Avoid: IDs (might be auto-generated in frameworks)
await page.fill('#email', 'test@example.com');

// 🚫 Bad: Text content (breaks with copy changes)
await page.getByText('Login').click();  // Ambiguous if "Login" appears multiple times
```

### Example 2: Modal Dialog

```html
<div
  role="dialog"
  aria-labelledby="modal-title"
  data-testid="confirmation-modal"
>
  <h2 id="modal-title">Confirm Delete</h2>
  <p>Are you sure you want to delete this item?</p>

  <button
    data-testid="modal-cancel"
    aria-label="Cancel deletion"
  >
    Cancel
  </button>

  <button
    data-testid="modal-confirm"
    aria-label="Confirm deletion"
    class="btn btn-danger"
  >
    Delete
  </button>

  <button
    data-testid="modal-close"
    aria-label="Close dialog"
    class="close-button"
  >
    ×
  </button>
</div>
```

**Selector choices:**
```typescript
// 🥇 Best: Test IDs with context
await page.locator('[data-testid="confirmation-modal"] >> [data-testid="modal-confirm"]').click();

// 🥈 Good: Role + accessible name
await page
  .getByRole('dialog', { name: 'Confirm Delete' })
  .getByRole('button', { name: 'Confirm deletion' })
  .click();

// 🥉 Okay: Chaining with aria-label
await page.locator('div[role="dialog"] >> [aria-label="Confirm deletion"]').click();

// ⚠️ Avoid: CSS classes
await page.locator('.btn-danger').click();  // What if there are multiple?

// 🚫 Bad: Text only
await page.click('text=Delete');  // Could match anything with "Delete" text
```

### Example 3: Navigation Menu

```html
<nav aria-label="Main navigation" data-testid="main-nav">
  <a href="/" data-testid="nav-home">Home</a>
  <a href="/products" data-testid="nav-products">Products</a>
  <a href="/about" data-testid="nav-about">About</a>
  <a href="/contact" data-testid="nav-contact">Contact</a>
</nav>
```

**Selector choices:**
```typescript
// 🥇 Best: Test IDs with context
await page.locator('[data-testid="main-nav"] >> [data-testid="nav-products"]').click();

// 🥈 Good: Role + context + text
await page
  .getByRole('navigation', { name: 'Main navigation' })
  .getByRole('link', { name: 'Products' })
  .click();

// 🥉 Okay: Semantic HTML + href
await page.locator('nav >> a[href="/products"]').click();

// ⚠️ Risky: Text only
await page.getByText('Products').click();  // What if "Products" appears elsewhere?
```

## Best Practices Summary

### DO ✅

1. **Use test IDs for critical paths**
   ```html
   <button data-testid="checkout-submit">Proceed to Checkout</button>
   ```

2. **Prefer accessibility attributes**
   ```html
   <button aria-label="Add to cart">+</button>
   ```

3. **Chain selectors for specificity**
   ```typescript
   page.locator('.modal >> [data-testid="confirm-button"]')
   ```

4. **Wait for elements properly**
   ```typescript
   await page.waitForSelector('[data-testid="results"]');
   ```

5. **Use Playwright's built-in locators**
   ```typescript
   page.getByRole(), page.getByLabel(), page.getByText()
   ```

### DON'T ❌

1. **Don't rely on CSS classes**
   ```typescript
   // ❌ Brittle
   page.click('.btn-primary-large-blue');
   ```

2. **Don't use complex XPath**
   ```typescript
   // ❌ Hard to maintain
   page.click('//div[@class="container"]//button[contains(@class, "submit")]');
   ```

3. **Don't depend on DOM structure**
   ```typescript
   // ❌ Breaks with layout changes
   page.click('div > div > ul > li:nth-child(3) > a');
   ```

4. **Don't use generated IDs**
   ```typescript
   // ❌ Changes on every build
   page.click('#react-component-1234');
   ```

5. **Don't couple to implementation details**
   ```typescript
   // ❌ Tied to React internals
   page.click('[data-reactid=".0.1.2"]');
   ```

## Resources

- **Playwright Locators**: https://playwright.dev/docs/locators
- **Testing Library**: https://testing-library.com/docs/queries/about
- **W3C Selectors**: https://www.w3.org/TR/selectors-4/
- **ARIA Roles**: https://www.w3.org/TR/wai-aria-1.2/#role_definitions
