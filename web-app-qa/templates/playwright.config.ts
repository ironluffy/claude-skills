import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright Configuration for web-app-qa skill
 * See https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  // Directory where tests are located
  testDir: './tests',

  // Maximum time one test can run
  timeout: 30 * 1000,

  // Test execution settings
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  // Reporter configuration
  reporter: [
    ['html', { outputFolder: 'test-results/html' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list']
  ],

  // Shared settings for all projects
  use: {
    // Base URL for navigation
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Capture trace on first retry
    trace: 'on-first-retry',

    // Video recording
    video: 'retain-on-failure',

    // Accessibility testing
    // https://playwright.dev/docs/accessibility-testing
    // accessibilitySnapshot: true,
  },

  // Projects for different browsers and viewports
  projects: [
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 },
      },
    },

    {
      name: 'firefox-desktop',
      use: {
        ...devices['Desktop Firefox'],
        viewport: { width: 1920, height: 1080 },
      },
    },

    {
      name: 'webkit-desktop',
      use: {
        ...devices['Desktop Safari'],
        viewport: { width: 1920, height: 1080 },
      },
    },

    {
      name: 'tablet',
      use: {
        ...devices['iPad Pro'],
      },
    },

    {
      name: 'mobile',
      use: {
        ...devices['iPhone 13'],
      },
    },

    // Additional device configurations
    // {
    //   name: 'chromium-mobile',
    //   use: {
    //     ...devices['Pixel 5'],
    //   },
    // },
  ],

  // Run local dev server before starting tests
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});
