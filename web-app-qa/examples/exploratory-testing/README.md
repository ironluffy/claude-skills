# Exploratory Testing Example

This example demonstrates interactive exploratory testing with automatic test generation.

## Scenario

Test a login flow by exploring the application, then generate Playwright test code automatically.

## Interactive Workflow

### Step 1: Start Exploration

**You say:**
```
"Navigate to https://demo.playwright.dev/todomvc and explore the page structure"
```

**Claude will:**
- Use `browser_navigate` to open the page
- Use `browser_snapshot` to capture accessibility tree
- Show you the page structure with element IDs

**Example output:**
```
[1] input "What needs to be done?" (placeholder)
[2] button "Toggle all"
[3] list "Todo list" (empty)
[4] footer "Filters: All, Active, Completed"
```

### Step 2: Interact Naturally

**You say:**
```
"Add a todo item 'Buy groceries' and another one 'Walk the dog'"
```

**Claude will:**
- Use `browser_fill` to type in the input
- Use `browser_press_key` to press Enter
- Repeat for second item
- Verify items were added

### Step 3: Test More Actions

**You say:**
```
"Mark the first todo as complete, then verify it shows as completed"
```

**Claude will:**
- Use `browser_click` on the checkbox
- Use `browser_verify_element_visible` to confirm completion
- Take screenshot if needed

### Step 4: Generate Test Code

**You say:**
```
"Generate a Playwright test for what we just did"
```

**Claude will generate:**
```typescript
import { test, expect } from '@playwright/test';

test('manage todo items', async ({ page }) => {
  // Navigate to app
  await page.goto('https://demo.playwright.dev/todomvc');

  // Add first todo
  await page.fill('.new-todo', 'Buy groceries');
  await page.keyboard.press('Enter');

  // Add second todo
  await page.fill('.new-todo', 'Walk the dog');
  await page.keyboard.press('Enter');

  // Verify todos are added
  await expect(page.locator('.todo-list li')).toHaveCount(2);
  await expect(page.locator('.todo-list li').first()).toContainText('Buy groceries');

  // Complete first todo
  await page.locator('.todo-list li').first().locator('.toggle').click();

  // Verify completion
  await expect(page.locator('.todo-list li').first()).toHaveClass(/completed/);
});
```

## Automated Script Usage

Instead of interactive mode, you can use the script:

```bash
python scripts/generate_tests.py \
  --url https://demo.playwright.dev/todomvc \
  --scenario "manage todo items" \
  --output tests/todo.spec.ts
```

## Tips for Exploration

### DO ✅

1. **Start with snapshot** to understand page structure
2. **Interact step-by-step** - don't rush through flows
3. **Verify each action** - use assertions to check outcomes
4. **Note edge cases** - try invalid inputs, empty states
5. **Document findings** - ask Claude to summarize issues found

### DON'T ❌

1. **Don't skip verification** - always check that actions worked
2. **Don't assume** - use snapshot to confirm element presence
3. **Don't rush** - exploratory testing finds more bugs when thorough
4. **Don't forget error states** - test unhappy paths too

## Example Conversations

### Exploring a Search Feature

**You:** "Navigate to https://www.example.com and test the search functionality"

**Claude:**
1. Opens page and shows structure
2. Finds search input and button
3. Enters search term
4. Clicks search button
5. Verifies results appear
6. Generates test code

### Testing Form Validation

**You:** "Test the signup form at https://app.example.com/signup - try valid and invalid inputs"

**Claude:**
1. Navigates and captures form structure
2. Tests empty submission (validation errors)
3. Tests invalid email format
4. Tests password requirements
5. Tests successful submission
6. Generates comprehensive test covering all cases

### Exploring Navigation

**You:** "Explore the navigation menu and test all links work"

**Claude:**
1. Captures nav structure with `browser_snapshot`
2. Clicks each link sequentially
3. Verifies each destination loads
4. Checks for 404s or errors
5. Generates navigation test suite

## Benefits of Exploratory Testing

1. **Find unexpected bugs** - Manual exploration often reveals issues missed by scripted tests
2. **Understand user experience** - See the app as users do
3. **Generate test coverage** - Convert exploration into automated tests
4. **Document workflows** - Create test artifacts from exploration
5. **Validate assumptions** - Confirm how features actually work

## Next Steps

After exploration:

1. **Save generated tests** to your test suite
2. **Refine selectors** - Replace brittle selectors with robust ones
3. **Add edge cases** - Expand tests with additional scenarios
4. **Run regularly** - Add to CI/CD pipeline
5. **Update as needed** - Maintain tests alongside feature changes

## Resources

- See `references/selector-strategies.md` for robust selector patterns
- See `references/playwright-mcp-tools.md` for all available MCP tools
- See `templates/test-template.spec.ts` for test code structure
