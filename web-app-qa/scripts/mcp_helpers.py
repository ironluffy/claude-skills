"""
MCP Helper Utilities - Wrappers for Playwright MCP tools
Part of web-app-qa skill for Claude Skills

This module provides Python wrappers for common Playwright MCP operations.
Note: These are reference implementations - actual MCP tools are called by Claude Code.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class MCPToolCall:
    """Represents a call to a Playwright MCP tool"""
    tool_name: str
    parameters: Dict[str, Any]
    description: str


class PlaywrightMCPHelper:
    """Helper class for generating MCP tool calls"""

    @staticmethod
    def navigate(url: str, timeout: int = 30000) -> MCPToolCall:
        """Generate browser_navigate tool call"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_navigate',
            parameters={'url': url, 'timeout': timeout},
            description=f'Navigate to {url}'
        )

    @staticmethod
    def click(selector: str) -> MCPToolCall:
        """Generate browser_click tool call"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_click',
            parameters={'selector': selector},
            description=f'Click element: {selector}'
        )

    @staticmethod
    def fill(selector: str, value: str) -> MCPToolCall:
        """Generate browser_type tool call"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_type',
            parameters={'selector': selector, 'text': value},
            description=f'Fill "{value}" into {selector}'
        )

    @staticmethod
    def snapshot(verbose: bool = False) -> MCPToolCall:
        """Generate browser_snapshot tool call"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_snapshot',
            parameters={'verbose': verbose},
            description='Capture accessibility tree snapshot'
        )

    @staticmethod
    def screenshot(full_page: bool = True, path: Optional[str] = None) -> MCPToolCall:
        """Generate browser_take_screenshot tool call"""
        params = {'full_page': full_page}
        if path:
            params['path'] = path

        return MCPToolCall(
            tool_name='mcp__playwright__browser_take_screenshot',
            parameters=params,
            description=f'Take {"full page" if full_page else "viewport"} screenshot'
        )

    @staticmethod
    def verify_element_visible(selector: str) -> MCPToolCall:
        """Generate browser_verify_element_visible tool call (requires testing capability)"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_verify_element_visible',
            parameters={'selector': selector},
            description=f'Verify element is visible: {selector}'
        )

    @staticmethod
    def verify_text_visible(text: str) -> MCPToolCall:
        """Generate browser_verify_text_visible tool call (requires testing capability)"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_verify_text_visible',
            parameters={'text': text},
            description=f'Verify text is visible: "{text}"'
        )

    @staticmethod
    def fill_form(fields: Dict[str, str]) -> List[MCPToolCall]:
        """Generate multiple browser_type calls for form filling"""
        return [
            PlaywrightMCPHelper.fill(selector, value)
            for selector, value in fields.items()
        ]

    @staticmethod
    def console_messages() -> MCPToolCall:
        """Generate browser_console_messages tool call"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_console_messages',
            parameters={},
            description='Get console messages'
        )

    @staticmethod
    def network_requests(filter_type: Optional[str] = None) -> MCPToolCall:
        """Generate browser_network_requests tool call"""
        params = {}
        if filter_type:
            params['type'] = filter_type

        return MCPToolCall(
            tool_name='mcp__playwright__browser_network_requests',
            parameters=params,
            description=f'Get network requests{f" (type: {filter_type})" if filter_type else ""}'
        )

    @staticmethod
    def evaluate(expression: str) -> MCPToolCall:
        """Generate browser_evaluate tool call"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_evaluate',
            parameters={'expression': expression},
            description=f'Evaluate JavaScript: {expression[:50]}...'
        )

    @staticmethod
    def resize_viewport(width: int, height: int) -> MCPToolCall:
        """Generate browser_resize tool call"""
        return MCPToolCall(
            tool_name='mcp__playwright__browser_resize',
            parameters={'width': width, 'height': height},
            description=f'Resize viewport to {width}x{height}'
        )


class TestGenerationHelper:
    """Helper for generating Playwright test code from MCP interactions"""

    @staticmethod
    def generate_test_template(
        test_name: str,
        url: str,
        steps: List[str],
        assertions: List[str]
    ) -> str:
        """Generate a Playwright test template"""

        # Sanitize test name
        safe_name = test_name.lower().replace(' ', '_').replace('-', '_')

        code = f"""import {{ test, expect }} from '@playwright/test';

test.describe('{test_name}', () => {{
  test('{safe_name}', async ({{ page }}) => {{
    // Navigate to page
    await page.goto('{url}');

"""

        # Add steps
        if steps:
            code += "    // Test steps\n"
            for step in steps:
                code += f"    {step}\n"
            code += "\n"

        # Add assertions
        if assertions:
            code += "    // Assertions\n"
            for assertion in assertions:
                code += f"    {assertion}\n"

        code += "  });\n});\n"

        return code

    @staticmethod
    def selector_to_playwright(selector: str, selector_type: str = 'css') -> str:
        """Convert various selector formats to Playwright locator"""
        if selector_type == 'css':
            return f"page.locator('{selector}')"
        elif selector_type == 'text':
            return f"page.getByText('{selector}')"
        elif selector_type == 'role':
            return f"page.getByRole('{selector}')"
        elif selector_type == 'testid':
            return f"page.getByTestId('{selector}')"
        elif selector_type == 'label':
            return f"page.getByLabel('{selector}')"
        else:
            return f"page.locator('{selector}')"


class SelectorStrategyHelper:
    """Helper for choosing robust selectors"""

    SELECTOR_PRIORITY = [
        'data-testid',
        'aria-label',
        'aria-labelledby',
        'role',
        'name',
        'placeholder',
        'text',
        'type',
        'class'
    ]

    @staticmethod
    def analyze_element(element_attrs: Dict[str, str]) -> Dict[str, Any]:
        """Analyze element attributes and recommend best selector strategy"""
        recommendations = []

        # Check for test IDs (highest priority)
        if 'data-testid' in element_attrs:
            recommendations.append({
                'strategy': 'testid',
                'selector': f"[data-testid='{element_attrs['data-testid']}']",
                'priority': 1,
                'reason': 'Test ID - most stable'
            })

        # Check for ARIA labels (semantic)
        if 'aria-label' in element_attrs:
            recommendations.append({
                'strategy': 'aria-label',
                'selector': f"[aria-label='{element_attrs['aria-label']}']",
                'priority': 2,
                'reason': 'ARIA label - semantic and stable'
            })

        # Check for role (semantic)
        if 'role' in element_attrs:
            recommendations.append({
                'strategy': 'role',
                'selector': f"[role='{element_attrs['role']}']",
                'priority': 3,
                'reason': 'ARIA role - semantic'
            })

        # Check for name attribute
        if 'name' in element_attrs:
            recommendations.append({
                'strategy': 'name',
                'selector': f"[name='{element_attrs['name']}']",
                'priority': 4,
                'reason': 'Name attribute - fairly stable'
            })

        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'])

        return {
            'best_selector': recommendations[0] if recommendations else None,
            'alternatives': recommendations[1:] if len(recommendations) > 1 else [],
            'element_attrs': element_attrs
        }


def export_mcp_workflow(steps: List[MCPToolCall], output_path: str) -> None:
    """Export MCP workflow to JSON for documentation"""
    workflow = {
        'steps': [
            {
                'tool': step.tool_name,
                'parameters': step.parameters,
                'description': step.description
            }
            for step in steps
        ]
    }

    with open(output_path, 'w') as f:
        json.dump(workflow, f, indent=2)

    print(f"[✓] Workflow exported to {output_path}")


# Example usage
if __name__ == '__main__':
    # Example: Generate a login test workflow
    mcp = PlaywrightMCPHelper()

    workflow = [
        mcp.navigate('https://app.example.com/login'),
        mcp.snapshot(),
        mcp.fill('[name="email"]', 'test@example.com'),
        mcp.fill('[name="password"]', 'Test123!'),
        mcp.click('button[type="submit"]'),
        mcp.verify_text_visible('Dashboard'),
    ]

    print("Example MCP Workflow:")
    for i, step in enumerate(workflow, 1):
        print(f"{i}. {step.description}")
        print(f"   Tool: {step.tool_name}")
        print(f"   Params: {step.parameters}\n")
