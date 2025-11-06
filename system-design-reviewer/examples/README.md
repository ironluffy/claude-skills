# System Design Review Examples

This directory contains example system design reviews demonstrating the skill's capabilities.

## Example: Simple API Service

A basic REST API service review showing:
- Architecture diagram generation (Mermaid + ASCII)
- Security vulnerability detection
- Performance optimization opportunities
- Cost optimization recommendations

### Before Review

- No caching layer
- Single database instance
- No rate limiting
- Hardcoded secrets detected

### After Review

Generated comprehensive report with:
- Multi-format diagrams
- 1 critical security issue identified
- 3 performance optimizations suggested
- 37% cost reduction opportunity identified

### Running the Review

```bash
cd system-design-reviewer/scripts
python3 review_design.py ../examples/sample-api --output ../examples/review-output.md
```

### Expected Output

See `review-output.md` for the complete generated review report with diagrams, findings, and recommendations.

## Adding Your Own Examples

1. Create a project directory with typical structure
2. Run `review_design.py` on it
3. Review the generated report
4. Add any custom metrics or configurations
