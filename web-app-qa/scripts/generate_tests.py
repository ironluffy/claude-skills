#!/usr/bin/env python3
"""
Test Generation Script - Generate Playwright tests from exploration or requirements
Part of web-app-qa skill for Claude Skills

Usage:
    python generate_tests.py --url <url> --scenario "description" --output tests/test.spec.ts
    python generate_tests.py --url <url> --interactive --output tests/test.spec.ts
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext


class TestRecorder:
    """Records browser interactions and generates Playwright test code"""

    def __init__(self, url: str, scenario: str, headless: bool = False):
        self.url = url
        self.scenario = scenario
        self.headless = headless
        self.actions: List[Dict] = []
        self.assertions: List[Dict] = []

    def explore_page(self) -> None:
        """Explore the page and capture structure"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                try:
                    context = browser.new_context()
                    page = context.new_page()

                    # Navigate to URL
                    print(f"[*] Navigating to {self.url}")
                    page.goto(self.url, wait_until='domcontentloaded', timeout=30000)
                    self.actions.append({
                        'type': 'goto',
                        'url': self.url
                    })

                    # Wait for page to load
                    page.wait_for_load_state('networkidle', timeout=10000)

                    # Capture page structure
                    print(f"[*] Analyzing page structure...")
                    self._analyze_page_structure(page)

                    # Generate test code
                    print(f"[*] Generating test code for scenario: {self.scenario}")

                finally:
                    # Ensure browser closes properly
                    context.close()
                    browser.close()
        except Exception as e:
            print(f"[✗] Error during page exploration: {e}")
            raise

    def _analyze_page_structure(self, page: Page) -> None:
        """Analyze page structure to identify testable elements"""
        try:
            # Get counts of interactive elements
            structure = {
                'title': page.title(),
                'url': page.url,
                'interactive_elements': page.locator('button, a, input, select, textarea').count(),
                'forms': page.locator('form').count(),
                'buttons': page.locator('button').count(),
                'links': page.locator('a').count(),
                'inputs': page.locator('input').count()
            }

            print(f"[*] Page Analysis:")
            print(f"    Title: {structure['title']}")
            print(f"    Interactive elements: {structure['interactive_elements']}")
            print(f"    Forms: {structure['forms']}")
            print(f"    Buttons: {structure['buttons']}")
            print(f"    Links: {structure['links']}")
            print(f"    Inputs: {structure['inputs']}")
        except Exception as e:
            print(f"[!] Warning: Could not fully analyze page structure: {e}")

    def generate_test_code(self, output_path: Path) -> str:
        """Generate Playwright test code from recorded actions"""

        # Sanitize scenario name for test function
        test_name = self.scenario.lower().replace(' ', '_').replace('-', '_')

        # Build test code
        code = f"""import {{ test, expect }} from '@playwright/test';

test.describe('{self.scenario}', () => {{
  test('{test_name}', async ({{ page }}) => {{
"""

        # Add navigation
        code += f"    // Navigate to page\n"
        code += f"    await page.goto('{self.url}');\n\n"

        # Add scenario-specific interactions (placeholder for AI to fill)
        code += f"    // TODO: Add test steps for: {self.scenario}\n"
        code += f"    // Example interactions:\n"
        code += f"    // await page.fill('[name=\"email\"]', 'test@example.com');\n"
        code += f"    // await page.click('button[type=\"submit\"]');\n\n"

        # Add assertions (placeholder for AI to fill)
        code += f"    // TODO: Add assertions\n"
        code += f"    // Example assertions:\n"
        code += f"    // await expect(page).toHaveURL(/.*dashboard/);\n"
        code += f"    // await expect(page.locator('h1')).toContainText('Welcome');\n"

        code += f"  }});\n"
        code += f"}});\n"

        return code

    def save_test(self, output_path: Path) -> None:
        """Save generated test to file"""
        test_code = self.generate_test_code(output_path)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write test file
        output_path.write_text(test_code)
        print(f"[✓] Test generated: {output_path}")
        print(f"[!] Note: Test contains placeholders - use with Claude Code to fill in specific interactions")


def generate_from_scenario(url: str, scenario: str, output: Path, headless: bool = False) -> None:
    """Generate test from URL and scenario description"""
    recorder = TestRecorder(url, scenario, headless)
    recorder.explore_page()
    recorder.save_test(output)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Playwright tests from exploration or requirements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate test template for login flow
  python generate_tests.py \\
    --url https://app.example.com/login \\
    --scenario "user login flow" \\
    --output tests/login.spec.ts

  # Generate with browser visible (non-headless)
  python generate_tests.py \\
    --url https://app.example.com \\
    --scenario "homepage navigation" \\
    --output tests/nav.spec.ts \\
    --no-headless

Note: This script generates test templates. For AI-powered test generation
with specific interactions, use this script with Claude Code + Playwright MCP.
        """
    )

    parser.add_argument('--url', required=True, help='URL to test')
    parser.add_argument('--scenario', required=True, help='Test scenario description')
    parser.add_argument('--output', required=True, type=Path, help='Output test file path (.spec.ts)')
    parser.add_argument('--no-headless', action='store_true', help='Show browser during exploration')

    args = parser.parse_args()

    # Validate output file extension
    if not args.output.suffix == '.ts':
        print(f"[!] Warning: Output file should have .spec.ts extension", file=sys.stderr)

    try:
        generate_from_scenario(
            url=args.url,
            scenario=args.scenario,
            output=args.output,
            headless=not args.no_headless
        )
    except Exception as e:
        print(f"[✗] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
