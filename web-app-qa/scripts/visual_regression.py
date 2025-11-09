#!/usr/bin/env python3
"""
Visual Regression Testing Script - Screenshot comparison and diff visualization
Part of web-app-qa skill for Claude Skills

Usage:
    # Capture baseline
    python visual_regression.py --url <url> --mode baseline --output baselines/

    # Compare against baseline
    python visual_regression.py --url <url> --mode compare --baseline baselines/ --output diffs/

    # Multi-viewport capture
    python visual_regression.py --url <url> --mode baseline --viewports desktop,tablet,mobile
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from playwright.sync_api import sync_playwright, Page
from PIL import Image, ImageChops, ImageDraw, ImageFont
import numpy as np


class VisualTester:
    """Captures screenshots and performs visual regression testing"""

    VIEWPORTS = {
        'desktop': {'width': 1920, 'height': 1080},
        'tablet': {'width': 768, 'height': 1024},
        'mobile': {'width': 375, 'height': 667},
        'laptop': {'width': 1366, 'height': 768},
    }

    def __init__(self, url: str, headless: bool = True):
        self.url = url
        self.headless = headless

    def capture_baseline(self, output_dir: Path, viewports: List[str]) -> List[Path]:
        """Capture baseline screenshots at multiple viewport sizes"""
        output_dir.mkdir(parents=True, exist_ok=True)
        captured_files = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)

            for viewport_name in viewports:
                if viewport_name not in self.VIEWPORTS:
                    print(f"[!] Unknown viewport: {viewport_name}, skipping")
                    continue

                viewport = self.VIEWPORTS[viewport_name]
                print(f"[*] Capturing {viewport_name} ({viewport['width']}x{viewport['height']})...")

                context = browser.new_context(viewport=viewport)
                page = context.new_page()
                page.goto(self.url)
                page.wait_for_load_state('networkidle')

                # Generate filename
                filename = f"{viewport_name}_{viewport['width']}x{viewport['height']}.png"
                filepath = output_dir / filename

                # Capture screenshot
                page.screenshot(path=str(filepath), full_page=True)
                captured_files.append(filepath)
                print(f"[✓] Saved: {filepath}")

                context.close()

            browser.close()

        return captured_files

    def compare_screenshots(
        self,
        baseline_dir: Path,
        current_url: str,
        output_dir: Path,
        viewports: List[str],
        threshold: float = 0.05
    ) -> Dict:
        """Compare current screenshots against baseline"""
        output_dir.mkdir(parents=True, exist_ok=True)
        results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'threshold': threshold,
            'comparisons': []
        }

        # Capture current screenshots
        current_dir = output_dir / 'current'
        current_dir.mkdir(exist_ok=True)

        print(f"[*] Capturing current screenshots...")
        current_files = self.capture_baseline(current_dir, viewports)

        # Compare each viewport
        for viewport_name in viewports:
            if viewport_name not in self.VIEWPORTS:
                continue

            viewport = self.VIEWPORTS[viewport_name]
            filename = f"{viewport_name}_{viewport['width']}x{viewport['height']}.png"

            baseline_path = baseline_dir / filename
            current_path = current_dir / filename

            if not baseline_path.exists():
                print(f"[!] No baseline found for {viewport_name}, skipping comparison")
                continue

            print(f"[*] Comparing {viewport_name}...")

            # Perform comparison
            diff_result = self._compare_images(baseline_path, current_path, output_dir, viewport_name, threshold)
            results['comparisons'].append(diff_result)
            results['total'] += 1

            if diff_result['passed']:
                results['passed'] += 1
                print(f"[✓] {viewport_name}: PASSED (diff: {diff_result['diff_percentage']:.2f}%)")
            else:
                results['failed'] += 1
                print(f"[✗] {viewport_name}: FAILED (diff: {diff_result['diff_percentage']:.2f}% > threshold: {threshold*100}%)")

        # Save comparison report
        self._save_comparison_report(results, output_dir)

        return results

    def _compare_images(
        self,
        baseline_path: Path,
        current_path: Path,
        output_dir: Path,
        viewport_name: str,
        threshold: float
    ) -> Dict:
        """Compare two images and generate diff visualization"""
        # Load images
        baseline_img = Image.open(baseline_path).convert('RGB')
        current_img = Image.open(current_path).convert('RGB')

        # Ensure same size (handle full-page differences)
        if baseline_img.size != current_img.size:
            # Resize to match baseline
            current_img = current_img.resize(baseline_img.size, Image.LANCZOS)

        # Calculate pixel difference
        diff = ImageChops.difference(baseline_img, current_img)

        # Convert to numpy for percentage calculation
        diff_array = np.array(diff)
        total_pixels = diff_array.size
        changed_pixels = np.count_nonzero(diff_array)
        diff_percentage = (changed_pixels / total_pixels) * 100

        # Enhance diff for visualization
        diff_enhanced = diff.point(lambda x: x * 10)

        # Create side-by-side comparison
        comparison = self._create_comparison_image(baseline_img, current_img, diff_enhanced, viewport_name, diff_percentage)

        # Save diff images
        diff_path = output_dir / f"{viewport_name}_diff.png"
        comparison_path = output_dir / f"{viewport_name}_comparison.png"

        diff_enhanced.save(diff_path)
        comparison.save(comparison_path)

        # Convert to Python bool for JSON serialization (numpy bool_ is not JSON serializable)
        passed = bool((diff_percentage / 100) <= threshold)

        return {
            'viewport': viewport_name,
            'baseline': str(baseline_path),
            'current': str(current_path),
            'diff': str(diff_path),
            'comparison': str(comparison_path),
            'diff_percentage': float(diff_percentage / 100),  # Ensure Python float
            'threshold': float(threshold),
            'passed': passed
        }

    def _create_comparison_image(
        self,
        baseline: Image.Image,
        current: Image.Image,
        diff: Image.Image,
        viewport_name: str,
        diff_percentage: float
    ) -> Image.Image:
        """Create side-by-side comparison with labels"""
        width, height = baseline.size
        label_height = 40

        # Create new image with 3 columns
        comparison = Image.new('RGB', (width * 3, height + label_height), 'white')

        # Add labels
        draw = ImageDraw.Draw(comparison)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        except:
            font = ImageFont.load_default()

        # Paste images
        comparison.paste(baseline, (0, label_height))
        comparison.paste(current, (width, label_height))
        comparison.paste(diff, (width * 2, label_height))

        # Draw labels
        draw.text((width // 2 - 40, 10), "BASELINE", fill='black', font=font)
        draw.text((width + width // 2 - 40, 10), "CURRENT", fill='black', font=font)
        draw.text((width * 2 + width // 2 - 40, 10), f"DIFF ({diff_percentage:.2f}%)", fill='red', font=font)

        return comparison

    def _save_comparison_report(self, results: Dict, output_dir: Path) -> None:
        """Save comparison results to JSON and HTML"""
        # Save JSON
        json_path = output_dir / 'comparison_report.json'
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"[✓] JSON report saved: {json_path}")

        # Generate HTML report
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Regression Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; }}
        h1 {{ color: #333; border-bottom: 3px solid #0066cc; padding-bottom: 10px; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .comparison {{ margin: 30px 0; border: 1px solid #ddd; padding: 20px; border-radius: 8px; }}
        .comparison img {{ max-width: 100%; height: auto; }}
        .passed {{ color: #0a0; font-weight: bold; }}
        .failed {{ color: #d00; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Visual Regression Test Report</h1>
    <div class="summary">
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Total Tests:</strong> {results['total']}</p>
        <p><strong>Passed:</strong> <span class="passed">{results['passed']}</span></p>
        <p><strong>Failed:</strong> <span class="failed">{results['failed']}</span></p>
        <p><strong>Threshold:</strong> {results['threshold'] * 100}%</p>
    </div>
"""

        for comp in results['comparisons']:
            status = 'passed' if comp['passed'] else 'failed'
            html += f"""
    <div class="comparison">
        <h2>{comp['viewport']} - <span class="{status}">{status.upper()}</span></h2>
        <p><strong>Difference:</strong> {comp['diff_percentage'] * 100:.2f}%</p>
        <img src="file://{comp['comparison']}" alt="{comp['viewport']} comparison">
    </div>
"""

        html += """
</body>
</html>
"""

        html_path = output_dir / 'comparison_report.html'
        html_path.write_text(html)
        print(f"[✓] HTML report saved: {html_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Visual regression testing with screenshot comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture baseline screenshots
  python visual_regression.py \\
    --url https://app.example.com \\
    --mode baseline \\
    --output baselines/ \\
    --viewports desktop,tablet,mobile

  # Compare against baseline
  python visual_regression.py \\
    --url https://app.example.com \\
    --mode compare \\
    --baseline baselines/ \\
    --output diffs/ \\
    --viewports desktop,tablet,mobile \\
    --threshold 0.05

  # Capture with browser visible
  python visual_regression.py \\
    --url https://app.example.com \\
    --mode baseline \\
    --output baselines/ \\
    --no-headless
        """
    )

    parser.add_argument('--url', required=True, help='URL to test')
    parser.add_argument('--mode', required=True, choices=['baseline', 'compare'],
                       help='Mode: baseline (capture) or compare (diff)')
    parser.add_argument('--output', required=True, type=Path, help='Output directory')
    parser.add_argument('--baseline', type=Path, help='Baseline directory (required for compare mode)')
    parser.add_argument('--viewports', default='desktop,tablet,mobile',
                       help='Comma-separated viewport names (default: desktop,tablet,mobile)')
    parser.add_argument('--threshold', type=float, default=0.05,
                       help='Difference threshold for pass/fail (default: 0.05 = 5%%)')
    parser.add_argument('--no-headless', action='store_true', help='Show browser')

    args = parser.parse_args()

    # Parse viewports
    viewports = [v.strip() for v in args.viewports.split(',')]

    # Validate compare mode requirements
    if args.mode == 'compare' and not args.baseline:
        parser.error("--baseline is required for compare mode")

    try:
        tester = VisualTester(args.url, headless=not args.no_headless)

        if args.mode == 'baseline':
            print(f"[*] Capturing baseline screenshots...")
            captured = tester.capture_baseline(args.output, viewports)
            print(f"[✓] Captured {len(captured)} baseline screenshots")

        elif args.mode == 'compare':
            print(f"[*] Running visual regression comparison...")
            results = tester.compare_screenshots(
                baseline_dir=args.baseline,
                current_url=args.url,
                output_dir=args.output,
                viewports=viewports,
                threshold=args.threshold
            )

            print("\n" + "="*60)
            print(f"VISUAL REGRESSION SUMMARY")
            print("="*60)
            print(f"Total: {results['total']} | Passed: {results['passed']} | Failed: {results['failed']}")
            print("="*60)

            sys.exit(0 if results['failed'] == 0 else 1)

    except Exception as e:
        print(f"[✗] Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
