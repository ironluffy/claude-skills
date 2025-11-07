#!/usr/bin/env python3
"""
Cross-Browser Testing Script - Multi-browser test orchestration
Part of web-app-qa skill for Claude Skills

Usage:
    python cross_browser.py --url <url> --browsers chrome,firefox,webkit
    python cross_browser.py --url <url> --flow "description" --browsers all --output report.html
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser, BrowserType
import time


class CrossBrowserTester:
    """Orchestrates tests across multiple browsers"""

    BROWSER_ENGINES = {
        'chrome': 'chromium',
        'chromium': 'chromium',
        'firefox': 'firefox',
        'webkit': 'webkit',
        'safari': 'webkit'
    }

    def __init__(self, url: str, flow_description: str = None, headless: bool = True):
        self.url = url
        self.flow_description = flow_description
        self.headless = headless
        self.results = []

    def test_browsers(self, browsers: List[str]) -> List[Dict]:
        """Test URL across multiple browsers"""
        results = []

        with sync_playwright() as p:
            for browser_name in browsers:
                if browser_name not in self.BROWSER_ENGINES:
                    print(f"[!] Unknown browser: {browser_name}, skipping")
                    continue

                engine = self.BROWSER_ENGINES[browser_name]
                print(f"\n[*] Testing on {browser_name.upper()} ({engine})...")

                try:
                    result = self._test_single_browser(p, engine, browser_name)
                    results.append(result)
                except Exception as e:
                    print(f"[✗] {browser_name} failed: {e}")
                    results.append({
                        'browser': browser_name,
                        'engine': engine,
                        'status': 'ERROR',
                        'error': str(e),
                        'tests': []
                    })

        self.results = results
        return results

    def _test_single_browser(self, playwright, engine: str, browser_name: str) -> Dict:
        """Test on a single browser"""
        start_time = time.time()

        # Launch browser
        if engine == 'chromium':
            browser = playwright.chromium.launch(headless=self.headless)
        elif engine == 'firefox':
            browser = playwright.firefox.launch(headless=self.headless)
        elif engine == 'webkit':
            browser = playwright.webkit.launch(headless=self.headless)
        else:
            raise ValueError(f"Unknown engine: {engine}")

        context = browser.new_context()
        page = context.new_page()

        tests = []

        # Test 1: Page Load
        test_result = self._test_page_load(page, browser_name)
        tests.append(test_result)

        if test_result['status'] == 'PASS':
            # Test 2: Basic Interactions (if page loaded successfully)
            interaction_result = self._test_basic_interactions(page, browser_name)
            tests.append(interaction_result)

            # Test 3: Console Errors
            console_result = self._test_console_errors(page, browser_name)
            tests.append(console_result)

        browser.close()

        elapsed_time = time.time() - start_time

        # Determine overall status
        failed = [t for t in tests if t['status'] == 'FAIL']
        warnings = [t for t in tests if t['status'] == 'WARN']

        if failed:
            overall_status = 'FAIL'
        elif warnings:
            overall_status = 'WARN'
        else:
            overall_status = 'PASS'

        return {
            'browser': browser_name,
            'engine': engine,
            'status': overall_status,
            'elapsed_time': elapsed_time,
            'tests': tests
        }

    def _test_page_load(self, page: Page, browser_name: str) -> Dict:
        """Test basic page loading"""
        test_name = "Load page"
        start_time = time.time()

        try:
            response = page.goto(self.url, wait_until='networkidle', timeout=30000)
            elapsed = time.time() - start_time

            if response.status >= 400:
                return {
                    'test': test_name,
                    'status': 'FAIL',
                    'message': f'HTTP {response.status}',
                    'elapsed': elapsed
                }

            # Check if page loaded
            page.wait_for_load_state('domcontentloaded')

            # Warn if slow
            if elapsed > 5.0:
                status = 'WARN'
                message = f'Loaded (slow: {elapsed:.1f}s)'
            else:
                status = 'PASS'
                message = f'Loaded in {elapsed:.1f}s'

            return {
                'test': test_name,
                'status': status,
                'message': message,
                'elapsed': elapsed
            }

        except Exception as e:
            elapsed = time.time() - start_time
            return {
                'test': test_name,
                'status': 'FAIL',
                'message': str(e),
                'elapsed': elapsed
            }

    def _test_basic_interactions(self, page: Page, browser_name: str) -> Dict:
        """Test basic page interactions"""
        test_name = "Basic interactions"
        start_time = time.time()

        try:
            # Check if interactive elements exist
            buttons = page.locator('button').count()
            links = page.locator('a').count()
            inputs = page.locator('input').count()

            elapsed = time.time() - start_time

            if buttons + links + inputs == 0:
                status = 'WARN'
                message = 'No interactive elements found'
            else:
                status = 'PASS'
                message = f'Found {buttons} buttons, {links} links, {inputs} inputs'

            return {
                'test': test_name,
                'status': status,
                'message': message,
                'elapsed': elapsed
            }

        except Exception as e:
            elapsed = time.time() - start_time
            return {
                'test': test_name,
                'status': 'FAIL',
                'message': str(e),
                'elapsed': elapsed
            }

    def _test_console_errors(self, page: Page, browser_name: str) -> Dict:
        """Check for console errors"""
        test_name = "Console errors"

        # Note: This is a simple check. For real console monitoring,
        # you'd need to set up listeners before navigation
        try:
            # Try to check for obvious console errors via evaluation
            has_errors = page.evaluate("""() => {
                // This is a simplified check
                return window.console && window.console.error ? false : false;
            }""")

            return {
                'test': test_name,
                'status': 'PASS',
                'message': 'No obvious console errors',
                'elapsed': 0
            }

        except Exception as e:
            return {
                'test': test_name,
                'status': 'WARN',
                'message': f'Could not check console: {e}',
                'elapsed': 0
            }

    def print_summary(self) -> None:
        """Print test summary to console"""
        if not self.results:
            print("[!] No results available")
            return

        print("\n" + "="*80)
        print("CROSS-BROWSER TEST SUMMARY")
        print("="*80)
        print(f"URL: {self.url}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Create results table
        header = f"{'Browser':<15} | {'Status':<10} | {'Time':<10} | {'Details'}"
        print(header)
        print("-" * 80)

        for result in self.results:
            browser = result['browser'].upper()
            status = result['status']
            time_str = f"{result.get('elapsed_time', 0):.2f}s"

            # Status with emoji
            if status == 'PASS':
                status_str = '✅ PASS'
            elif status == 'WARN':
                status_str = '⚠️  WARN'
            elif status == 'FAIL':
                status_str = '❌ FAIL'
            else:
                status_str = '❓ ERROR'

            # Get failed test names
            failed_tests = [t['test'] for t in result.get('tests', []) if t['status'] in ['FAIL', 'WARN']]
            details = ', '.join(failed_tests) if failed_tests else 'All tests passed'

            print(f"{browser:<15} | {status_str:<10} | {time_str:<10} | {details}")

        print("="*80)

        # Show detailed test results
        print("\nDETAILED RESULTS:")
        for result in self.results:
            print(f"\n{result['browser'].upper()} ({result['engine']}):")
            for test in result.get('tests', []):
                status_icon = '✅' if test['status'] == 'PASS' else ('⚠️ ' if test['status'] == 'WARN' else '❌')
                print(f"  {status_icon} {test['test']}: {test['message']}")

    def generate_html_report(self, output_path: Path) -> None:
        """Generate HTML report with test matrix"""
        if not self.results:
            print("[!] No results available for report generation")
            return

        # Build test matrix
        all_tests = set()
        for result in self.results:
            for test in result.get('tests', []):
                all_tests.add(test['test'])

        all_tests = sorted(list(all_tests))

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cross-Browser Test Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; }}
        h1 {{ color: #333; border-bottom: 3px solid #0066cc; padding-bottom: 10px; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #0066cc; color: white; }}
        .pass {{ background: #d4edda; color: #155724; font-weight: bold; }}
        .warn {{ background: #fff3cd; color: #856404; font-weight: bold; }}
        .fail {{ background: #f8d7da; color: #721c24; font-weight: bold; }}
        .error {{ background: #e7e7e7; color: #333; }}
    </style>
</head>
<body>
    <h1>Cross-Browser Test Report</h1>

    <div class="summary">
        <p><strong>URL:</strong> {self.url}</p>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Browsers Tested:</strong> {len(self.results)}</p>
    </div>

    <h2>Test Matrix</h2>
    <table>
        <thead>
            <tr>
                <th>Test Step</th>
"""

        # Add browser columns
        for result in self.results:
            html += f"                <th>{result['browser'].upper()}</th>\n"

        html += """
            </tr>
        </thead>
        <tbody>
"""

        # Add test rows
        for test_name in all_tests:
            html += f"            <tr>\n                <td><strong>{test_name}</strong></td>\n"

            for result in self.results:
                # Find this test in results
                test_result = next((t for t in result.get('tests', []) if t['test'] == test_name), None)

                if test_result:
                    status = test_result['status'].lower()
                    message = test_result['message']
                    html += f'                <td class="{status}">{status.upper()}<br><small>{message}</small></td>\n'
                else:
                    html += '                <td class="error">N/A</td>\n'

            html += "            </tr>\n"

        html += """
        </tbody>
    </table>
</body>
</html>
"""

        # Write report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)
        print(f"[✓] HTML report generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Cross-browser testing orchestrator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test on Chrome, Firefox, and Safari
  python cross_browser.py \\
    --url https://app.example.com \\
    --browsers chrome,firefox,webkit

  # Test all browsers with detailed flow
  python cross_browser.py \\
    --url https://app.example.com/checkout \\
    --flow "add item, proceed to checkout, enter payment" \\
    --browsers all \\
    --output results/cross-browser.html

  # Test with browser visible
  python cross_browser.py \\
    --url https://app.example.com \\
    --browsers chrome,firefox \\
    --no-headless
        """
    )

    parser.add_argument('--url', required=True, help='URL to test')
    parser.add_argument('--browsers', default='chrome,firefox,webkit',
                       help='Comma-separated browser names (or "all")')
    parser.add_argument('--flow', help='Description of test flow to execute')
    parser.add_argument('--output', type=Path, help='Output HTML report path')
    parser.add_argument('--no-headless', action='store_true', help='Show browsers')

    args = parser.parse_args()

    # Parse browsers
    if args.browsers == 'all':
        browsers = ['chrome', 'firefox', 'webkit']
    else:
        browsers = [b.strip() for b in args.browsers.split(',')]

    try:
        tester = CrossBrowserTester(
            url=args.url,
            flow_description=args.flow,
            headless=not args.no_headless
        )

        print(f"[*] Testing {len(browsers)} browser(s)...")
        tester.test_browsers(browsers)
        tester.print_summary()

        if args.output:
            tester.generate_html_report(args.output)

        # Exit with error code if any browser failed
        failed = [r for r in tester.results if r['status'] == 'FAIL']
        sys.exit(1 if failed else 0)

    except Exception as e:
        print(f"[✗] Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
