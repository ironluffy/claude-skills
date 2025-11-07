# Changelog

All notable changes to the Universal Claude Skills repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-07

### Added

#### Web App QA Skill 🧪🔍

**NEW SKILL:** Interactive UI/visual QA workflows powered by Microsoft's Playwright MCP for comprehensive web application quality assurance.

- **Test Generation from Exploration**
  - Interactive browser automation via natural language
  - Automatic Playwright test code generation
  - Test templates with best practice selectors
  - Support for complex user flows and scenarios

- **Accessibility Compliance (WCAG 2.1)**
  - AA/AAA level compliance checking using axe-core
  - Automated violation detection across 4 WCAG principles
  - Detailed HTML reports with fix recommendations
  - Issue categorization (Critical/Serious/Moderate/Minor)
  - Code examples for fixing violations
  - Screenshot capture of accessibility issues

- **Visual Regression Testing**
  - Multi-viewport screenshot capture (desktop, tablet, mobile)
  - Pixel-perfect comparison with baseline images
  - Diff visualization with change highlighting
  - Configurable thresholds (1%-10% tolerance)
  - Side-by-side comparison reports
  - Support for dynamic content handling

- **Cross-Browser Compatibility**
  - Test across Chrome (Chromium), Firefox, and WebKit (Safari)
  - Parallel browser execution
  - Compatibility matrix generation
  - Browser-specific issue identification
  - Performance comparison across browsers
  - HTML reports with test results

- **Python Automation Scripts** (4 core + 2 utilities)
  - `generate_tests.py` - AI-powered test generation from exploration
  - `accessibility_audit.py` - WCAG compliance checker with axe-core
  - `visual_regression.py` - Screenshot comparison and diff generation
  - `cross_browser.py` - Multi-browser test orchestration
  - `mcp_helpers.py` - Playwright MCP tool wrappers
  - `report_generator.py` - Professional HTML report utilities

- **Comprehensive Reference Documentation**
  - `wcag-aa-guidelines.md` - Complete WCAG 2.1 AA reference with examples
  - `visual-testing-guide.md` - Visual regression best practices
  - `selector-strategies.md` - Robust selector patterns (test IDs, ARIA, semantic HTML)
  - `playwright-mcp-tools.md` - All 27+ Playwright MCP tools documented

- **Templates & Configuration**
  - `playwright.config.ts` - Multi-browser Playwright configuration
  - `test-template.spec.ts` - Comprehensive test boilerplate
  - `mcp-config.json` - Playwright MCP server setup
  - `package.json` - Node.js dependencies and scripts
  - `.gitignore` - Test artifacts and output exclusions

- **Real-World Examples**
  - `examples/exploratory-testing/` - Interactive test generation workflow
  - `examples/accessibility-audit/` - WCAG compliance audit example
  - `examples/visual-validation/` - Visual regression testing example

#### Microsoft Playwright MCP Integration

**MCP Server:** Integration with official Playwright MCP server providing 27+ browser automation tools.

- **Navigation Tools**
  - `browser_navigate` - Navigate to URLs
  - `browser_navigate_back` - Browser back button

- **Interaction Tools**
  - `browser_click` - Click elements
  - `browser_type` - Type text into fields
  - `browser_fill_form` - Fill multiple form fields
  - `browser_select_option` - Select dropdown options
  - `browser_press_key` - Keyboard inputs (Enter, Escape, Tab, etc.)
  - `browser_hover` - Hover over elements
  - `browser_drag` - Drag and drop

- **Inspection Tools**
  - `browser_snapshot` - Capture accessibility tree (structured page elements)
  - `browser_take_screenshot` - Full page or viewport screenshots
  - `browser_console_messages` - View console logs and errors
  - `browser_network_requests` - Inspect network activity

- **Testing & Assertion Tools** (requires `testing` capability)
  - `browser_verify_element_visible` - Assert element presence
  - `browser_verify_text_visible` - Assert text content
  - `browser_verify_value` - Assert input values
  - `browser_verify_list_visible` - Assert list items
  - `browser_generate_locator` - Generate robust selectors

- **Advanced Tools**
  - `browser_evaluate` - Execute JavaScript in page context
  - `browser_wait_for` - Wait for network idle, load states
  - `browser_handle_dialog` - Handle alerts, confirms, prompts
  - `browser_file_upload` - Upload files through inputs
  - `browser_resize` - Change viewport dimensions

#### Features

**Interactive QA Workflows:**
- Natural language test exploration
- Real-time browser interaction
- Automatic test code generation
- AI-powered selector recommendations
- Step-by-step guidance for QA engineers

**Accessibility Testing:**
- WCAG 2.1 AA/AAA compliance
- 4.5:1 color contrast checking
- Alt text validation
- Form label verification
- Keyboard navigation testing
- Screen reader compatibility
- ARIA attribute validation

**Visual Regression:**
- Baseline capture and management
- Pixel-by-pixel comparison
- Change detection with thresholds
- Diff image generation
- Multi-viewport testing
- Dynamic content handling

**Best Practices:**
- Test ID-based selectors (`data-testid`)
- ARIA-first selector strategy
- Semantic HTML preference
- Accessibility-focused testing
- Robust, maintainable test patterns

### Changed

- **Plugin Manifest** - Updated to v1.2.0
  - Added web-app-qa to skills list
  - Added QA & Testing category
  - New keywords: qa, testing, accessibility, visual-regression, cross-browser, playwright, wcag
  - MCP server requirements documented
  - Python dependency requirements specified

### Documentation

- **Comprehensive Skill Documentation**
  - `web-app-qa/SKILL.md` - 435 lines of workflow instructions
  - `web-app-qa/README.md` - Complete setup and usage guide
  - 4 reference guides (WCAG, visual testing, selectors, MCP tools)
  - 3 real-world example workflows
  - 5 template files for quick start

- **MCP Server Setup Guide**
  - Installation instructions for Playwright MCP
  - Configuration examples for Claude Code
  - Capability flags explained (testing, vision, pdf)
  - Troubleshooting common issues
  - Verification steps

### Technical Details

#### Statistics
- **New Skill:** web-app-qa
- **Scripts:** 6 Python files (4 core + 2 utilities)
- **Reference Docs:** 4 comprehensive guides
- **Templates:** 5 starter files
- **Examples:** 3 real-world workflows
- **Total Lines:** ~3500 lines of code and documentation

#### Dependencies

**Python Requirements:**
- `playwright>=1.40.0` - Browser automation
- `axe-core-python>=4.8.0` - Accessibility testing
- `Pillow>=10.0.0` - Image processing
- `numpy>=1.24.0` - Array operations

**MCP Requirements:**
- Microsoft Playwright MCP (`@playwright/mcp@latest`)
- Node.js 18+
- Playwright browsers (chromium, firefox, webkit)

#### File Structure
```
web-app-qa/
├── SKILL.md (435 lines)
├── README.md (456 lines)
├── scripts/ (6 Python files, 1200+ lines)
│   ├── generate_tests.py
│   ├── accessibility_audit.py
│   ├── visual_regression.py
│   ├── cross_browser.py
│   ├── mcp_helpers.py
│   └── report_generator.py
├── references/ (4 guides, 1500+ lines)
│   ├── wcag-aa-guidelines.md
│   ├── visual-testing-guide.md
│   ├── selector-strategies.md
│   └── playwright-mcp-tools.md
├── templates/ (5 files)
│   ├── playwright.config.ts
│   ├── test-template.spec.ts
│   ├── mcp-config.json
│   ├── package.json
│   └── .gitignore
└── examples/ (3 workflows)
    ├── exploratory-testing/
    ├── accessibility-audit/
    └── visual-validation/
```

### Benefits

- **Faster QA Cycles** - Natural language exploration accelerates testing
- **Accessibility Compliance** - Automated WCAG validation reduces manual audits
- **Visual Regression Prevention** - Catch unintended UI changes before production
- **Cross-Browser Coverage** - Verify compatibility across all major browsers
- **Test Generation** - Convert manual exploration into automated tests
- **QA Engineer Friendly** - No coding required for basic workflows

### Migration Guide

This is a new skill with no breaking changes to existing skills.

To start using:

1. **Add Playwright MCP to Claude Code:**
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest", "--caps", "testing,vision", "--headless"]
       }
     }
   }
   ```

2. **Install Python dependencies (for scripts):**
   ```bash
   pip install -r web-app-qa/scripts/requirements.txt
   python -m playwright install
   ```

3. **Start using interactively:**
   ```
   "Navigate to https://example.com and test the login flow"
   ```

---

## [1.1.0] - 2025-11-06

### Added

#### System Design Reviewer Skill 🏗️📊

**NEW SKILL:** Comprehensive system design review and analysis tool with multi-format diagram generation.

- **Multi-Format Diagram Generation**
  - Mermaid diagrams (GitHub/GitLab-renderable)
  - ASCII diagrams (universal terminal compatibility)
  - Architecture diagrams (components, services, databases)
  - Sequence diagrams (API flows, authentication)
  - Database/ER diagrams (schema relationships)
  - Flowcharts (business logic, decision trees)

- **Python Analysis Scripts** (6 total)
  - `review_design.py` - Main orchestrator for complete reviews
  - `generate_diagrams.py` - Multi-format diagram generator
  - `analyze_architecture.py` - Architecture best practices checker
  - `security_analyzer.py` - OWASP Top 10 & vulnerability detector
  - `performance_analyzer.py` - Performance bottleneck finder
  - `cost_optimizer.py` - Cloud cost optimization analyzer

- **Comprehensive Analysis Framework**
  - **Architecture Review**: Scalability, reliability, maintainability
  - **Security Assessment**: OWASP compliance, auth/encryption gaps
  - **Performance Optimization**: Caching, N+1 queries, load balancing
  - **Cost Efficiency**: Right-sizing, serverless, 30-50% savings potential

- **Reference Documentation**
  - `architecture-best-practices.md` - Scalability and reliability patterns
  - `security-checklist.md` - OWASP Top 10 and security headers
  - `performance-patterns.md` - Caching, indexing, optimization
  - `cost-optimization.md` - Cloud cost reduction strategies

- **Templates & Examples**
  - Review report template with structured format
  - Example demonstrations and usage patterns
  - Before/after review scenarios

#### Intelligent Agent/Human Assignment System 🤖👤

**Major Feature:** Automatic detection and assignment of tasks to AI agents or humans based on task characteristics.

- **Assignment Detection Algorithm**
  - Keyword-based analysis of task titles and descriptions
  - Three assignee types: AGENT, HUMAN, EITHER
  - Smart flagging for human review requirements
  - Label-based enhancement for detection accuracy

- **Enhanced task-decomposer**
  - `AssigneeType` enum (AGENT, HUMAN, EITHER)
  - `detect_assignee_type()` function with intelligent keyword matching
  - Visual indicators in output (🤖 agent, 👤 human, ⚠️ review)
  - Linear export with automatic assignment mapping
  - CLI arguments: `--agent-user`, `--human-users`
  - Assignment summary in exports

- **Enhanced issue-manager**
  - `assign` operation - Manual assignment to agent or human
  - `auto-assign` operation - Automatic detection and assignment
  - `reassign` operation - Transfer between agents and humans
  - Smart detection using same keyword logic
  - Assignment rationale tracking

#### Documentation

- **docs/ASSIGNMENT_RULES.md** - Complete assignment guide
  - Detection algorithm explanation
  - Keyword lists for all categories
  - Configuration examples
  - Best practices and troubleshooting
  - Integration with Linear/GitHub
  - Monitoring and analytics guidance

- **examples/task-decomposer/example-assignment-strategy.md**
  - Real-world payment processing system example
  - 11 subtasks with intelligent assignments
  - Assignment rationale for each task
  - Timeline and parallel execution strategy
  - Command examples and expected outputs

### Features

#### Assignment Detection Rules

**Agent Tasks (Automated):**
- Keywords: `implement`, `refactor`, `write test`, `build`, `automate`, `generate`, `update`, `code`, `develop`, `script`, `format`, `lint`, `type check`
- Fully automated technical work
- No human judgment required
- Testable with automated checks

**Human Tasks (Manual):**
- Keywords: `approve`, `decision`, `negotiate`, `prioritize`, `strategic`, `legal`, `compliance`, `stakeholder`, `interview`, `sign off`, `final approval`
- Requires human judgment
- Business decisions and strategy
- Stakeholder management

**Review Required (Agent + Human):**
- Keywords: `security`, `authentication`, `payment`, `financial`, `critical`, `production deploy`, `migration`, `audit`, `vulnerability`
- Agent can implement
- Human expert must review
- High-risk or security-critical

### Changed

- **Plugin Manifest** - Updated to v1.1.0
  - Added system-design-reviewer to skills list
  - Added Architecture category
  - New keywords: system-design, architecture-review, security-analysis, performance-optimization, cost-optimization
  - Comprehensive installation guide created

- **task-decomposer** - Updated to v1.1.0
  - `SubTask` dataclass now includes `assignee_type`, `assignee`, `requires_human_review`
  - `to_markdown()` now shows assignment information with icons
  - `export_to_linear()` enhanced with intelligent assignment mapping
  - New CLI arguments for assignment configuration

- **issue-manager** - Updated to v1.1.0
  - `IssueManager` class expanded with assignment methods
  - New operations: `assign`, `auto_assign`, `reassign`
  - Enhanced CLI argument parsing for assignments

- **README.md** - Updated with assignment features
  - New feature highlights
  - Updated usage examples
  - Visual indicators documented

### Performance

- **2-3x Faster Execution** - Parallel agent/human work streams
- **Clear Ownership** - No ambiguity on task assignments
- **Scalable** - Easy to add more agent capacity
- **Automated Routine Work** - Agents handle repetitive tasks
- **Human Focus on Value** - Humans focus on decisions and strategy

### Migration Guide

Existing scripts continue to work without changes. New assignment features are opt-in:

```bash
# Old (still works)
python task-decomposer/scripts/analyze_task.py "Task description"

# New (with assignments)
python task-decomposer/scripts/analyze_task.py "Task description" \
  --export-linear --team-id TEAM123 \
  --agent-user "agent-bot" \
  --human-users "backend:user-abc,security:user-def"
```

---

## [1.0.0] - 2025-11-06

### Added

#### Skills
- **skill-creator** - Meta-skill for developing and validating new skills
  - `init_skill.py` - Generate skill boilerplate
  - `package_skill.py` - Validate against v1.0 specification
  - Best practices documentation
  - Real-world skill examples

- **task-decomposer** - Break down complex tasks into actionable subtasks
  - Task decomposition with rationale
  - As-is → to-be state analysis
  - Risk assessment matrix
  - Expected outputs per subtask
  - Dependency tracking
  - Linear/GitHub export support

- **issue-manager** - Comprehensive issue management for GitHub/Linear/Jira
  - Block reporting and tracking
  - Issue splitting with multiple strategies
  - Bulk operations with dry-run preview
  - Related issue creation
  - Block analysis and escalation
  - Multi-platform support

- **template-skill** - Minimal starter template
  - Shows proper skill structure
  - Valid YAML frontmatter example
  - Documentation of conventions

#### Foundation
- Apache 2.0 license
- Agent Skills v1.0 specification
- Claude Code plugin configuration
- Comprehensive README documentation
- Git repository initialization

#### Documentation
- Complete skill documentation for each skill
- Reference guides (best practices, workflows, frameworks)
- Usage examples and templates
- Contributing guidelines
- Platform integration guides

#### Scripts
- Python automation scripts with proper error handling
- Validation tooling
- Analysis utilities
- Platform integration helpers

### Features

#### skill-creator
- ✓ Generate valid skill boilerplate
- ✓ Validate YAML frontmatter
- ✓ Check naming conventions
- ✓ Verify file references
- ✓ Detect writing style issues
- ✓ Comprehensive validation reporting

#### task-decomposer
- ✓ Decomposition with rationale
- ✓ State analysis (as-is/to-be/gap)
- ✓ Actionable 1-4h subtasks
- ✓ Testing criteria per subtask
- ✓ Risk assessment and mitigation
- ✓ Dependency graph generation
- ✓ Multiple output formats (Markdown, JSON, YAML)
- ✓ Linear/GitHub export ready

#### issue-manager
- ✓ Report blockers with context
- ✓ Auto-escalate stale blocks
- ✓ Split issues with multiple strategies
- ✓ Bulk operations with dry-run
- ✓ Create related issues with linking
- ✓ Query and filter issues
- ✓ Merge duplicate issues
- ✓ Multi-platform support (Linear, GitHub, Jira)

### Technical Details

#### File Structure
```
claude-skills/
├── .claude-plugin/
├── template-skill/
├── skill-creator/
│   ├── scripts/ (2 Python scripts)
│   └── references/ (2 guides)
├── task-decomposer/
│   ├── scripts/ (1 Python script)
│   └── references/ (2 guides)
└── issue-manager/
    ├── scripts/ (2 Python scripts)
    └── references/ (1 guide)
```

#### Statistics
- 4 production-ready skills
- 5 Python automation scripts
- 7 reference documentation files
- 5 comprehensive guides
- ~7000 lines of code and documentation
- Apache 2.0 licensed

### Platform Support
- ✓ Claude Code (via plugin)
- ✓ Claude.ai (manual upload)
- ✓ Claude API (programmatic)

### Integration Support
- ✓ Linear API
- ✓ GitHub API
- ✓ Jira API

---

## [Unreleased]

### Planned Features

#### New Skills
- [ ] code-reviewer - Automated code review with best practices
- [ ] test-generator - Generate comprehensive test suites
- [ ] api-docs - Generate API documentation from code
- [ ] migration-planner - Plan and execute migrations
- [ ] performance-analyzer - Analyze and optimize performance

#### Enhancements
- [ ] Enhanced Linear integration with full API support
- [ ] GitHub Actions for automated validation
- [ ] Interactive CLI for skill management
- [ ] VS Code extension integration
- [ ] Skill templates library
- [ ] AI-powered task analysis
- [ ] Team collaboration features

#### Documentation
- [ ] Video tutorials
- [ ] Interactive examples
- [ ] API reference documentation
- [ ] Integration guides for additional platforms

---

## Release Notes

### v1.0.0 - Initial Release

First stable release of Universal Claude Skills! 🎉

This release includes 4 production-ready skills focused on development workflows and project management. All skills follow the official Agent Skills v1.0 specification and include comprehensive documentation, automation scripts, and real-world examples.

**Highlights:**
- Complete skill development toolkit (skill-creator)
- Advanced task decomposition with risk assessment
- Full-featured issue management across platforms
- Ready for Claude Code plugin installation

**Getting Started:**
```bash
/plugin marketplace add ironluffy/claude-skills
/plugin install universal-claude-skills
```

---

## Version History

- **1.2.0** (2025-11-07) - Web App QA skill with Playwright MCP integration
- **1.1.0** (2025-11-06) - Intelligent agent/human assignment system
- **1.0.0** (2025-11-06) - Initial release with 4 skills

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- **Issues**: [GitHub Issues](https://github.com/ironluffy/claude-skills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ironluffy/claude-skills/discussions)
- **Documentation**: [README.md](README.md)
