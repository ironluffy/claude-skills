import { test, expect } from '@playwright/test';

/**
 * Test Template for web-app-qa skill
 *
 * This template demonstrates:
 * - Test organization and structure
 * - Page navigation and interaction
 * - Assertions and expectations
 * - Best practices for selector strategies
 */

// Test suite (describe block)
test.describe('Feature Name', () => {
  // Runs before each test in this describe block
  test.beforeEach(async ({ page }) => {
    // Navigate to the page under test
    await page.goto('/');

    // Wait for page to be ready (if needed)
    await page.waitForLoadState('networkidle');
  });

  // Individual test case
  test('should perform a specific action successfully', async ({ page }) => {
    // ARRANGE: Set up test data and initial state
    // (Optional: Fill forms, navigate to specific state, etc.)

    // ACT: Perform the action you're testing
    await page.click('[data-testid="action-button"]');

    // ASSERT: Verify expected outcomes
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page).toHaveURL(/.*success/);
  });

  test('should display validation error for invalid input', async ({ page }) => {
    // Test error states
    await page.fill('[data-testid="email-input"]', 'invalid-email');
    await page.click('[data-testid="submit-button"]');

    // Verify error message
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="error-message"]')).toContainText(
      'Please enter a valid email address'
    );
  });
});

// Example: Login flow test
test.describe('User Login', () => {
  test('should login with valid credentials', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login');

    // Fill login form using test IDs
    await page.fill('[data-testid="login-email"]', 'test@example.com');
    await page.fill('[data-testid="login-password"]', 'SecurePassword123!');

    // Submit form
    await page.click('[data-testid="login-submit"]');

    // Verify successful login
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator('h1')).toContainText('Dashboard');

    // Verify user is logged in
    const userMenu = page.locator('[data-testid="user-menu"]');
    await expect(userMenu).toBeVisible();
    await expect(userMenu).toContainText('test@example.com');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');

    // Attempt login with invalid credentials
    await page.fill('[data-testid="login-email"]', 'wrong@example.com');
    await page.fill('[data-testid="login-password"]', 'WrongPassword');
    await page.click('[data-testid="login-submit"]');

    // Verify error message
    await expect(page.locator('[data-testid="error-alert"]')).toBeVisible();
    await expect(page.locator('[data-testid="error-alert"]')).toContainText(
      'Invalid email or password'
    );

    // Verify still on login page
    await expect(page).toHaveURL(/.*login/);
  });

  test('should validate required fields', async ({ page }) => {
    await page.goto('/login');

    // Try to submit without filling fields
    await page.click('[data-testid="login-submit"]');

    // Verify validation messages
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
  });
});

// Example: Accessibility-focused test
test.describe('Accessibility', () => {
  test('should be keyboard navigable', async ({ page }) => {
    await page.goto('/');

    // Test keyboard navigation
    await page.keyboard.press('Tab');  // Focus first element
    await page.keyboard.press('Tab');  // Focus second element
    await page.keyboard.press('Enter');  // Activate element

    // Verify focus is visible
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
  });

  test('should have proper ARIA labels', async ({ page }) => {
    await page.goto('/');

    // Verify ARIA attributes
    const submitButton = page.getByRole('button', { name: 'Submit form' });
    await expect(submitButton).toBeVisible();

    const emailInput = page.getByLabel('Email address');
    await expect(emailInput).toBeVisible();
  });
});

// Example: Visual regression test
test.describe('Visual Regression', () => {
  test('homepage should match baseline', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Take screenshot for visual comparison
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      maxDiffPixels: 100,  // Allow small differences
    });
  });
});

// Example: API testing with Playwright
test.describe('API Integration', () => {
  test('should fetch data successfully', async ({ request }) => {
    const response = await request.get('/api/users');

    // Verify response
    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('users');
    expect(Array.isArray(data.users)).toBeTruthy();
  });
});

// Example: Mobile-specific test
test.describe('Mobile Viewport', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('should display mobile navigation', async ({ page }) => {
    await page.goto('/');

    // Verify mobile menu is visible
    const mobileMenu = page.locator('[data-testid="mobile-menu-button"]');
    await expect(mobileMenu).toBeVisible();

    // Open mobile menu
    await mobileMenu.click();

    // Verify menu items
    const menuDrawer = page.locator('[data-testid="mobile-menu-drawer"]');
    await expect(menuDrawer).toBeVisible();
  });
});

// Example: Test with custom fixtures
test.describe('Custom Fixtures', () => {
  test('should use authenticated user', async ({ page }) => {
    // Set up authenticated state
    await page.context().addCookies([
      {
        name: 'auth_token',
        value: 'test_token_123',
        domain: 'localhost',
        path: '/',
      },
    ]);

    await page.goto('/dashboard');

    // Verify authenticated access
    await expect(page.locator('[data-testid="user-profile"]')).toBeVisible();
  });
});

/**
 * Selector Strategy Examples:
 *
 * BEST PRACTICES:
 * ✅ Use test IDs:
 *    page.locator('[data-testid="submit-button"]')
 *
 * ✅ Use accessibility attributes:
 *    page.getByRole('button', { name: 'Submit' })
 *    page.getByLabel('Email address')
 *
 * ✅ Use semantic HTML:
 *    page.locator('nav >> a')
 *    page.locator('main >> h1')
 *
 * AVOID:
 * ❌ CSS classes:
 *    page.locator('.btn-primary-large')
 *
 * ❌ Complex XPath:
 *    page.locator('//div[@class="container"]//button')
 *
 * ❌ DOM structure:
 *    page.locator('div > div > ul > li:nth-child(3)')
 */
