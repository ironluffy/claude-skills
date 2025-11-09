#!/usr/bin/env python3
"""
Accessibility Audit Script - WCAG 2.1 AA/AAA compliance checking
Part of web-app-qa skill for Claude Skills

Usage:
    python accessibility_audit.py --url <url> --standard WCAG-AA --output report.html
    python accessibility_audit.py --url <url> --standard WCAG-AAA --include-screenshots
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page
from axe_core_python.sync_playwright import Axe
from report_generator import HTMLReportGenerator, ReportSection


class AccessibilityAuditor:
    """Performs comprehensive accessibility audits using axe-core"""

    WCAG_LEVELS = {
        'WCAG-A': ['wcag2a', 'wcag21a'],
        'WCAG-AA': ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'],
        'WCAG-AAA': ['wcag2a', 'wcag2aa', 'wcag2aaa', 'wcag21a', 'wcag21aa', 'wcag21aaa']
    }

    def __init__(self, url: str, standard: str = 'WCAG-AA', headless: bool = True):
        self.url = url
        self.standard = standard
        self.headless = headless
        self.results = None
        self.screenshot_path = None

    def run_audit(self, include_screenshots: bool = False) -> Dict:
        """Run accessibility audit on the page"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()

            print(f"[*] Navigating to {self.url}")
            page.goto(self.url)
            page.wait_for_load_state('networkidle')

            # Take screenshot if requested
            if include_screenshots:
                screenshot_dir = Path('screenshots')
                screenshot_dir.mkdir(exist_ok=True)
                self.screenshot_path = screenshot_dir / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(self.screenshot_path), full_page=True)
                print(f"[*] Screenshot saved: {self.screenshot_path}")

            # Run axe-core accessibility checks
            print(f"[*] Running {self.standard} accessibility audit...")
            axe = Axe()

            # Get tags for WCAG level
            tags = self.WCAG_LEVELS.get(self.standard, self.WCAG_LEVELS['WCAG-AA'])

            # Run scan with axe-core
            results = axe.run(page, {'runOnly': tags})

            browser.close()

        self.results = results
        return results

    def categorize_issues(self) -> Dict[str, List]:
        """Categorize issues by severity"""
        if not self.results:
            return {'critical': [], 'serious': [], 'moderate': [], 'minor': []}

        violations = self.results.get('violations', [])

        categorized = {
            'critical': [],
            'serious': [],
            'moderate': [],
            'minor': []
        }

        for violation in violations:
            impact = violation.get('impact', 'moderate')
            if impact == 'critical':
                categorized['critical'].append(violation)
            elif impact == 'serious':
                categorized['serious'].append(violation)
            elif impact == 'moderate':
                categorized['moderate'].append(violation)
            else:
                categorized['minor'].append(violation)

        return categorized

    def print_summary(self) -> None:
        """Print audit summary to console"""
        if not self.results:
            print("[!] No results available")
            return

        violations = self.results.get('violations', [])
        passes = self.results.get('passes', [])
        incomplete = self.results.get('incomplete', [])

        categorized = self.categorize_issues()

        print("\n" + "="*60)
        print(f"ACCESSIBILITY AUDIT SUMMARY - {self.standard}")
        print("="*60)
        print(f"URL: {self.url}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Critical issues
        if categorized['critical']:
            print(f"🚨 CRITICAL ISSUES ({len(categorized['critical'])}):")
            for issue in categorized['critical']:
                print(f"  - {issue['description']}")
                print(f"    Impact: {issue['impact']} | Affects {len(issue['nodes'])} element(s)")
            print()

        # Serious issues
        if categorized['serious']:
            print(f"⚠️  SERIOUS ISSUES ({len(categorized['serious'])}):")
            for issue in categorized['serious']:
                print(f"  - {issue['description']}")
                print(f"    Impact: {issue['impact']} | Affects {len(issue['nodes'])} element(s)")
            print()

        # Moderate/Minor warnings
        warning_count = len(categorized['moderate']) + len(categorized['minor'])
        if warning_count > 0:
            print(f"⚡ WARNINGS ({warning_count}):")
            for issue in categorized['moderate'][:3]:  # Show first 3
                print(f"  - {issue['description']}")
            if warning_count > 3:
                print(f"  ... and {warning_count - 3} more")
            print()

        # Passes
        print(f"✅ PASSED CHECKS: {len(passes)}")

        # Incomplete
        if incomplete:
            print(f"⏳ INCOMPLETE/MANUAL REVIEW NEEDED: {len(incomplete)}")

        print("="*60)

    def generate_html_report(self, output_path: Path) -> None:
        """Generate detailed HTML report using professional report generator"""
        if not self.results:
            print("[!] No results available for report generation")
            return

        violations = self.results.get('violations', [])
        passes = self.results.get('passes', [])
        incomplete = self.results.get('incomplete', [])
        categorized = self.categorize_issues()

        # Create report
        report = HTMLReportGenerator(
            title="Accessibility Audit Report",
            description=f"WCAG compliance analysis for {self.url}"
        )

        # Add metadata
        report.add_metadata('URL', self.url)
        report.add_metadata('Standard', self.standard)
        report.add_metadata('Test Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # Add summary statistics
        summary_stats = {
            '🚨 Critical': len(categorized['critical']),
            '⚠️  Serious': len(categorized['serious']),
            '⚡ Moderate': len(categorized['moderate']),
            'ℹ️  Minor': len(categorized['minor']),
            '✅ Passed': len(passes),
        }

        summary_html = report.generate_summary_stats(summary_stats)
        report.add_section(ReportSection(
            title="Summary",
            content=summary_html
        ))

        # Add Critical Issues
        if categorized['critical']:
            for issue in categorized['critical']:
                content = self._format_issue_content(issue)
                report.add_section(ReportSection(
                    title=issue['description'],
                    content=content,
                    severity='critical'
                ))

        # Add Serious Issues
        if categorized['serious']:
            for issue in categorized['serious']:
                content = self._format_issue_content(issue)
                report.add_section(ReportSection(
                    title=issue['description'],
                    content=content,
                    severity='warning'
                ))

        # Add Moderate Issues
        if categorized['moderate']:
            for issue in categorized['moderate']:
                content = self._format_issue_content(issue)
                report.add_section(ReportSection(
                    title=issue['description'],
                    content=content,
                    severity='info'
                ))

        # Save report
        report.save(output_path)
        print(f"[✓] HTML report generated: {output_path}")

    def _format_issue_content(self, issue: Dict) -> str:
        """Format issue content for report generator"""
        tags = ', '.join(issue.get('tags', []))
        node_count = len(issue.get('nodes', []))

        html = f"""
        <div class="metadata">
            <div class="metadata-item"><span class="metadata-label">Impact:</span> {issue['impact'].upper()}</div>
            <div class="metadata-item"><span class="metadata-label">Affects:</span> {node_count} element(s)</div>
            <div class="metadata-item"><span class="metadata-label">WCAG Tags:</span> {tags}</div>
        </div>

        <h3>How to Fix</h3>
        <p>{issue['help']}</p>
        <p><a href="{issue['helpUrl']}" target="_blank">📖 Learn more about this issue</a></p>
        """

        # Add affected elements (first 3)
        if issue.get('nodes'):
            html += "<details><summary><strong>Affected Elements</strong></summary><ul>"
            for node in issue['nodes'][:3]:
                target = node.get('target', [''])[0]
                html_snippet = node.get('html', 'N/A')
                html += f"<li><code>{target}</code><br><pre><code>{html_snippet}</code></pre></li>"
            if len(issue['nodes']) > 3:
                html += f"<li><em>... and {len(issue['nodes']) - 3} more element(s)</em></li>"
            html += "</ul></details>"

        return html


def main():
    parser = argparse.ArgumentParser(
        description='WCAG 2.1 AA/AAA accessibility compliance checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run WCAG 2.1 AA audit with HTML report
  python accessibility_audit.py \\
    --url https://app.example.com \\
    --standard WCAG-AA \\
    --output reports/a11y-report.html

  # Run AAA audit with screenshots
  python accessibility_audit.py \\
    --url https://app.example.com \\
    --standard WCAG-AAA \\
    --output reports/audit.html \\
    --include-screenshots

  # Run with browser visible
  python accessibility_audit.py \\
    --url https://app.example.com \\
    --no-headless
        """
    )

    parser.add_argument('--url', required=True, help='URL to audit')
    parser.add_argument('--standard', choices=['WCAG-A', 'WCAG-AA', 'WCAG-AAA'],
                       default='WCAG-AA', help='WCAG compliance level (default: WCAG-AA)')
    parser.add_argument('--output', type=Path, help='Output HTML report path')
    parser.add_argument('--include-screenshots', action='store_true',
                       help='Capture screenshots of issues')
    parser.add_argument('--no-headless', action='store_true', help='Show browser')

    args = parser.parse_args()

    try:
        auditor = AccessibilityAuditor(
            url=args.url,
            standard=args.standard,
            headless=not args.no_headless
        )

        auditor.run_audit(include_screenshots=args.include_screenshots)
        auditor.print_summary()

        if args.output:
            auditor.generate_html_report(args.output)

    except Exception as e:
        print(f"[✗] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
