# Playwright MCP Tools Reference

Complete reference for Microsoft's Playwright MCP server tools.

**Source:** https://github.com/microsoft/playwright-mcp

## Tool Categories

- **Navigation** (2 tools): Page navigation
- **Interaction** (8 tools): User actions
- **Inspection** (4 tools): Page analysis
- **Testing** (5 tools): Assertions (requires `testing` capability)
- **Advanced** (8+ tools): JavaScript evaluation, file upload, etc.

---

## Navigation Tools

### `browser_navigate`
Navigate to a URL.

**Parameters:**
- `url` (string, required): Target URL
- `timeout` (number, optional): Max wait time in ms (default: 30000)

**Example:**
```json
{
  "url": "https://app.example.com",
  "timeout": 30000
}
```

**Use cases:**
- Start of test flows
- Navigate between pages
- Load specific page states

---

### `browser_navigate_back`
Go back in browser history (back button).

**Parameters:** None

**Use cases:**
- Test back button behavior
- Return to previous page
- Multi-page flows

---

## Interaction Tools

### `browser_click`
Click an element.

**Parameters:**
- `selector` (string, required): CSS selector or accessibility locator
- `timeout` (number, optional): Max wait time in ms

**Example:**
```json
{
  "selector": "button[type='submit']"
}
```

**Use cases:**
- Submit forms
- Navigate via links
- Trigger actions

---

### `browser_type`
Type text into an input field.

**Parameters:**
- `selector` (string, required): CSS selector for input element
- `text` (string, required): Text to type
- `delay` (number, optional): Delay between keystrokes in ms

**Example:**
```json
{
  "selector": "[name='email']",
  "text": "test@example.com"
}
```

**Use cases:**
- Fill form fields
- Search inputs
- Text areas

---

### `browser_fill_form`
Fill multiple form fields at once.

**Parameters:**
- `fields` (object, required): Map of selector → value pairs

**Example:**
```json
{
  "fields": {
    "[name='email']": "test@example.com",
    "[name='password']": "password123",
    "[name='remember']": "true"
  }
}
```

**Use cases:**
- Fill entire forms efficiently
- Login forms
- Multi-field inputs

---

### `browser_select_option`
Select option from dropdown.

**Parameters:**
- `selector` (string, required): CSS selector for `<select>` element
- `value` (string, required): Option value to select

**Example:**
```json
{
  "selector": "select[name='country']",
  "value": "US"
}
```

**Use cases:**
- Dropdown selections
- Filter controls
- Configuration forms

---

### `browser_press_key`
Press keyboard key or combination.

**Parameters:**
- `key` (string, required): Key name (e.g., "Enter", "Escape", "Control+A")

**Example:**
```json
{
  "key": "Enter"
}
```

**Key combinations:**
- `"Control+A"` - Select all
- `"Control+C"` - Copy
- `"Escape"` - Close modal
- `"Tab"` - Next field
- `"ArrowDown"` - Navigate down

**Use cases:**
- Submit forms via Enter
- Close modals via Escape
- Keyboard navigation
- Shortcuts testing

---

### `browser_hover`
Hover over an element.

**Parameters:**
- `selector` (string, required): CSS selector

**Example:**
```json
{
  "selector": ".dropdown-trigger"
}
```

**Use cases:**
- Trigger dropdown menus
- Show tooltips
- Test hover states

---

### `browser_drag`
Drag and drop an element.

**Parameters:**
- `source` (string, required): Selector for element to drag
- `target` (string, required): Selector for drop target

**Example:**
```json
{
  "source": ".draggable-item",
  "target": ".drop-zone"
}
```

**Use cases:**
- Reorder lists
- Kanban boards
- File uploads via drag-drop

---

## Inspection Tools

### `browser_snapshot`
Capture accessibility tree snapshot of the page.

**Parameters:**
- `verbose` (boolean, optional): Include detailed attributes (default: false)

**Returns:**
- Structured text representation of page elements with unique IDs
- Interactive elements with roles, labels, and states
- Hierarchical page structure

**Example output:**
```
[1] button "Submit Order"
[2] input "Email address" (value: "")
[3] link "Terms of Service"
[4] heading "Welcome to the Dashboard"
```

**Use cases:**
- Understand page structure
- Find selectors
- Debug element visibility
- Accessibility analysis

**Why use this:**
- More reliable than screenshots for automation
- Works with dynamic content
- Provides semantic information

---

### `browser_take_screenshot`
Capture a screenshot of the page.

**Parameters:**
- `full_page` (boolean, optional): Capture full scrollable page (default: true)
- `path` (string, optional): File path to save screenshot

**Example:**
```json
{
  "full_page": true,
  "path": "screenshots/homepage.png"
}
```

**Use cases:**
- Visual documentation
- Bug reports
- Visual regression testing
- Baseline captures

---

### `browser_console_messages`
Get console logs from the page.

**Parameters:**
- `types` (array, optional): Filter by message types (log, error, warn, info, debug)

**Returns:**
- List of console messages with types and text

**Example:**
```json
{
  "types": ["error", "warn"]
}
```

**Use cases:**
- Debug JavaScript errors
- Check for warnings
- Validate logging
- Monitor client-side issues

---

### `browser_network_requests`
Get network requests made by the page.

**Parameters:**
- `type` (string, optional): Filter by resource type (document, xhr, fetch, image, script, stylesheet)

**Returns:**
- List of network requests with URL, status, method, and response

**Example:**
```json
{
  "type": "xhr"
}
```

**Use cases:**
- Verify API calls
- Check resource loading
- Debug failed requests
- Performance analysis

---

## Testing Tools (Require `testing` capability)

### `browser_verify_element_visible`
Assert that an element is visible.

**Parameters:**
- `selector` (string, required): CSS selector
- `timeout` (number, optional): Max wait time in ms

**Example:**
```json
{
  "selector": ".success-message"
}
```

**Use cases:**
- Verify UI elements appear
- Check form validation
- Confirm navigation success

---

### `browser_verify_text_visible`
Assert that specific text is visible on the page.

**Parameters:**
- `text` (string, required): Text to find
- `timeout` (number, optional): Max wait time in ms

**Example:**
```json
{
  "text": "Order Confirmed"
}
```

**Use cases:**
- Verify success messages
- Check page content
- Validate labels

---

### `browser_verify_value`
Assert that an input field has a specific value.

**Parameters:**
- `selector` (string, required): CSS selector for input
- `value` (string, required): Expected value

**Example:**
```json
{
  "selector": "[name='email']",
  "value": "test@example.com"
}
```

**Use cases:**
- Verify form pre-fill
- Check field persistence
- Validate input after changes

---

### `browser_verify_list_visible`
Assert that specific items are visible in a list.

**Parameters:**
- `selector` (string, required): Selector for list container
- `items` (array, required): Array of expected text items

**Example:**
```json
{
  "selector": ".search-results",
  "items": ["Product A", "Product B", "Product C"]
}
```

**Use cases:**
- Verify search results
- Check filtered lists
- Validate navigation menus

---

### `browser_generate_locator`
Generate a robust selector for an element.

**Parameters:**
- `description` (string, required): Description of element to find

**Returns:**
- Recommended CSS selector or accessible locator

**Example:**
```json
{
  "description": "The submit button in the login form"
}
```

**Use cases:**
- Find best selector for automation
- Generate test code
- Learn selector strategies

---

## Advanced Tools

### `browser_evaluate`
Execute JavaScript in the page context.

**Parameters:**
- `expression` (string, required): JavaScript code to execute

**Returns:**
- Result of the JavaScript expression (must be JSON-serializable)

**Example:**
```json
{
  "expression": "document.title"
}
```

**Use cases:**
- Get computed values
- Manipulate DOM
- Query page state
- Mock data

---

### `browser_wait_for`
Wait for a condition to be true.

**Parameters:**
- `condition` (string, required): One of: `networkidle`, `load`, `domcontentloaded`
- `timeout` (number, optional): Max wait time in ms

**Example:**
```json
{
  "condition": "networkidle",
  "timeout": 30000
}
```

**Use cases:**
- Wait for AJAX requests
- Ensure page fully loaded
- Synchronize with animations

---

### `browser_handle_dialog`
Accept or dismiss browser dialogs (alert, confirm, prompt).

**Parameters:**
- `action` (string, required): "accept" or "dismiss"
- `text` (string, optional): Text to enter for prompt dialogs

**Example:**
```json
{
  "action": "accept",
  "text": "Test input"
}
```

**Use cases:**
- Handle confirmation dialogs
- Test alert behavior
- Input into prompts

---

### `browser_file_upload`
Upload a file through file input.

**Parameters:**
- `selector` (string, required): Selector for file input
- `file_path` (string, required): Path to file to upload

**Example:**
```json
{
  "selector": "input[type='file']",
  "file_path": "/path/to/file.pdf"
}
```

**Use cases:**
- Test file upload forms
- Profile picture uploads
- Document attachments

---

### `browser_resize`
Resize browser viewport.

**Parameters:**
- `width` (number, required): Viewport width in pixels
- `height` (number, required): Viewport height in pixels

**Example:**
```json
{
  "width": 375,
  "height": 667
}
```

**Use cases:**
- Test responsive design
- Simulate mobile devices
- Capture different viewport sizes

---

## Capability Flags

Add to `--caps` argument when starting MCP server:

### `testing`
Enables assertion tools:
- `browser_verify_element_visible`
- `browser_verify_text_visible`
- `browser_verify_value`
- `browser_verify_list_visible`
- `browser_generate_locator`

**Enable:**
```bash
npx @playwright/mcp@latest --caps testing
```

### `vision`
Enables coordinate-based interactions (click by pixel coordinates).

**Enable:**
```bash
npx @playwright/mcp@latest --caps vision
```

### `pdf`
Enables PDF generation from pages.

**Enable:**
```bash
npx @playwright/mcp@latest --caps pdf
```

### Multiple capabilities
```bash
npx @playwright/mcp@latest --caps testing,vision,pdf
```

---

## Common Patterns

### Login Flow
```typescript
// 1. Navigate
browser_navigate({ url: "https://app.example.com/login" })

// 2. Take snapshot to see structure
browser_snapshot({ verbose: false })

// 3. Fill credentials
browser_fill_form({
  fields: {
    "[name='email']": "test@example.com",
    "[name='password']": "password123"
  }
})

// 4. Submit
browser_click({ selector: "button[type='submit']" })

// 5. Verify success
browser_verify_text_visible({ text: "Dashboard" })
```

### Accessibility Audit
```typescript
// 1. Navigate to page
browser_navigate({ url: "https://app.example.com" })

// 2. Get accessibility tree
browser_snapshot({ verbose: true })

// 3. Check console for a11y errors
browser_console_messages({ types: ["error"] })

// 4. Verify critical elements
browser_verify_element_visible({ selector: "main" })
browser_verify_element_visible({ selector: "nav" })
```

### Visual Regression
```typescript
// 1. Navigate
browser_navigate({ url: "https://app.example.com" })

// 2. Wait for stable state
browser_wait_for({ condition: "networkidle" })

// 3. Resize to target viewport
browser_resize({ width: 1920, height: 1080 })

// 4. Capture screenshot
browser_take_screenshot({
  full_page: true,
  path: "baselines/homepage_desktop.png"
})
```

### Cross-Browser Workflow
```typescript
// Same commands work across Chromium, Firefox, WebKit
// Just launch different browser when starting MCP server

// Test in all browsers:
for browser in ['chromium', 'firefox', 'webkit']:
  # Launch MCP with browser
  # Run same test commands
  # Compare results
```

---

## Best Practices

1. **Always use `browser_snapshot` first** to understand page structure
2. **Prefer accessibility locators** (role, label) over CSS classes
3. **Use `browser_wait_for`** before taking screenshots
4. **Enable `testing` capability** for assertions
5. **Check console errors** with `browser_console_messages`
6. **Verify network requests** for API testing
7. **Use `browser_fill_form`** instead of multiple `browser_type` calls
8. **Resize viewport** before visual regression tests

---

## Resources

- **GitHub Repository**: https://github.com/microsoft/playwright-mcp
- **Playwright Docs**: https://playwright.dev/docs/intro
- **MCP Specification**: https://github.com/modelcontextprotocol/specification
