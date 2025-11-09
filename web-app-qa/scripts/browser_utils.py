"""
Browser Utilities - Reusable browser lifecycle management
Part of web-app-qa skill for Claude Skills

Provides context managers and utilities for managing Playwright browser instances.
"""

from typing import Optional, Dict, Literal
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, PlaywrightContextManager


class BrowserManager:
    """Context manager for Playwright browser lifecycle management

    Handles browser launch, context creation, and cleanup automatically.
    Supports all three browser engines (chromium, firefox, webkit) with
    configurable viewport and headless settings.

    Example:
        ```python
        with BrowserManager('chromium', headless=True) as page:
            page.goto('https://example.com')
            # ... do work ...
        # Browser automatically closed
        ```
    """

    def __init__(
        self,
        browser_type: Literal['chromium', 'firefox', 'webkit'] = 'chromium',
        headless: bool = True,
        viewport: Optional[Dict[str, int]] = None,
        timeout: int = 30000
    ):
        """Initialize browser manager

        Args:
            browser_type: Browser engine to use ('chromium', 'firefox', 'webkit')
            headless: Run browser in headless mode (default: True)
            viewport: Optional viewport size dict with 'width' and 'height' keys
            timeout: Default navigation timeout in milliseconds (default: 30000)
        """
        self.browser_type = browser_type
        self.headless = headless
        self.viewport = viewport
        self.timeout = timeout

        # Will be populated in __enter__
        self.playwright: Optional[PlaywrightContextManager] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def __enter__(self) -> Page:
        """Enter context manager - launch browser and return page

        Returns:
            Page: Playwright page object ready for use

        Raises:
            ValueError: If browser_type is invalid
        """
        # Start Playwright
        self.playwright = sync_playwright().start()

        # Get browser launcher
        if self.browser_type == 'chromium':
            browser_launcher = self.playwright.chromium
        elif self.browser_type == 'firefox':
            browser_launcher = self.playwright.firefox
        elif self.browser_type == 'webkit':
            browser_launcher = self.playwright.webkit
        else:
            raise ValueError(f"Invalid browser type: {self.browser_type}. "
                           f"Must be one of: chromium, firefox, webkit")

        # Launch browser
        self.browser = browser_launcher.launch(headless=self.headless)

        # Create context with optional viewport
        context_kwargs = {}
        if self.viewport:
            context_kwargs['viewport'] = self.viewport

        self.context = self.browser.new_context(**context_kwargs)

        # Set default timeout
        self.context.set_default_navigation_timeout(self.timeout)
        self.context.set_default_timeout(self.timeout)

        # Create page
        self.page = self.context.new_page()

        return self.page

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager - cleanup browser resources

        Ensures proper cleanup even if exceptions occurred.
        """
        try:
            if self.context:
                self.context.close()
        except Exception:
            pass  # Ignore errors during cleanup

        try:
            if self.browser:
                self.browser.close()
        except Exception:
            pass  # Ignore errors during cleanup

        try:
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass  # Ignore errors during cleanup

        # Don't suppress exceptions from the with block
        return False


class MultiBrowserManager:
    """Context manager for running operations across multiple browsers

    Launches multiple browser instances sequentially and provides
    an iterator over (browser_name, page) tuples.

    Example:
        ```python
        with MultiBrowserManager(['chromium', 'firefox'], headless=True) as browsers:
            for browser_name, page in browsers:
                page.goto('https://example.com')
                # Test on this browser
        # All browsers automatically closed
        ```
    """

    def __init__(
        self,
        browser_types: list[Literal['chromium', 'firefox', 'webkit']],
        headless: bool = True,
        viewport: Optional[Dict[str, int]] = None
    ):
        """Initialize multi-browser manager

        Args:
            browser_types: List of browser engines to use
            headless: Run browsers in headless mode (default: True)
            viewport: Optional viewport size for all browsers
        """
        self.browser_types = browser_types
        self.headless = headless
        self.viewport = viewport
        self.managers: list[BrowserManager] = []

    def __enter__(self):
        """Enter context manager - return self for iteration"""
        return self

    def __iter__(self):
        """Iterate over browsers, yielding (browser_name, page) tuples"""
        for browser_type in self.browser_types:
            manager = BrowserManager(
                browser_type=browser_type,
                headless=self.headless,
                viewport=self.viewport
            )
            self.managers.append(manager)

            try:
                page = manager.__enter__()
                yield browser_type, page
            finally:
                # Clean up this browser before moving to next
                manager.__exit__(None, None, None)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager - cleanup all browsers"""
        # Managers clean themselves up in the iterator
        # This is just a safety net
        for manager in self.managers:
            try:
                manager.__exit__(None, None, None)
            except Exception:
                pass

        return False


def navigate_with_retry(
    page: Page,
    url: str,
    max_retries: int = 3,
    wait_until: Literal['load', 'domcontentloaded', 'networkidle'] = 'domcontentloaded'
) -> bool:
    """Navigate to URL with automatic retry on failure

    Args:
        page: Playwright page object
        url: URL to navigate to
        max_retries: Maximum number of retry attempts (default: 3)
        wait_until: Wait condition before returning (default: 'domcontentloaded')

    Returns:
        bool: True if navigation succeeded, False otherwise
    """
    for attempt in range(max_retries):
        try:
            page.goto(url, wait_until=wait_until)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"[!] Navigation failed after {max_retries} attempts: {e}")
                return False
            print(f"[!] Navigation attempt {attempt + 1} failed, retrying...")

    return False


def wait_for_stable_dom(page: Page, timeout: int = 10000, check_interval: int = 100) -> bool:
    """Wait for DOM to become stable (no changes for a period)

    Useful for waiting for dynamic content to finish loading when
    networkidle is not reliable.

    Args:
        page: Playwright page object
        timeout: Maximum time to wait in milliseconds (default: 10000)
        check_interval: How often to check DOM in milliseconds (default: 100)

    Returns:
        bool: True if DOM stabilized, False if timeout
    """
    try:
        page.wait_for_load_state('domcontentloaded', timeout=timeout)

        # Wait for no DOM changes for 500ms
        last_html_length = 0
        stable_count = 0
        max_checks = timeout // check_interval

        for _ in range(max_checks):
            current_html_length = page.evaluate('document.documentElement.outerHTML.length')

            if current_html_length == last_html_length:
                stable_count += 1
                if stable_count >= 5:  # Stable for 5 checks (500ms if check_interval=100)
                    return True
            else:
                stable_count = 0

            last_html_length = current_html_length
            page.wait_for_timeout(check_interval)

        return False
    except Exception:
        return False
